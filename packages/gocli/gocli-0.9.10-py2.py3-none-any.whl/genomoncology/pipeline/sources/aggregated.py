import copy
from cytoolz.curried import curry, assoc
from cytoolz import reduceby

from genomoncology.parse import DocType, __TYPE__, __CHILD__
from .base import LazyFileSource
from .delimited import do_split, DelimitedFileSource


def dict_seq_reducer(seq, dict_key, value_keys, add_kv_dict=None):
    """
    Reduce a sequence of dicts to single dict of dicts,
    optionally adding additional k,v pairs
    """
    reduced_dict = dict()
    for element in seq:
        if len(element["REF"]) > 1400 or len(element["ALT"]) >= 1400:
            continue
        reduced_dict[element[dict_key]] = dict()
        for key in value_keys:
            reduced_dict[element[dict_key]][key] = element[key]
        if add_kv_dict:
            for k, v in add_kv_dict.items():
                reduced_dict[element[dict_key]][k] = v
    return reduced_dict


@curry
class AggregatedFileSource(LazyFileSource):
    def __init__(
        self,
        filename,
        aggregate_key,
        backup_key=None,
        delimiter="\t",
        include_header=True,
        **meta,
    ):
        self.delimiter = delimiter
        self.aggregate_key = aggregate_key
        self.backup_key = backup_key
        self.include_header = include_header
        self.meta = meta

        if __TYPE__ not in meta:
            self.meta = assoc(self.meta, __TYPE__, DocType.AGGREGATE.value)

        super().__init__(filename)

    def __iter__(self):
        # noinspection PyUnresolvedReferences
        iterator = super(AggregatedFileSource.func, self).__iter__()

        self.columns = next(iterator).strip().split(self.delimiter)

        if self.include_header:
            yield self.create_header()

        aggregated_d = reduceby(
            self.get_key_value, self.get_aggregate_value, iterator, dict
        )

        for key, value in aggregated_d.items():
            value["key"] = key
            value["__type__"] = DocType.AGGREGATE.value
            yield value

    def create_header(self):
        return {
            __TYPE__: DocType.HEADER.value,
            __CHILD__: self.meta.get(__TYPE__),
            "columns": self.columns,
            "meta": self.meta,
            "file_path": self.name,
        }

    def get_key_value(self, x):
        column_index = self.columns.index(self.aggregate_key)
        elements = do_split(self.delimiter, x.replace("\n", ""))
        if column_index < len(elements) and elements[column_index] != "":
            key = elements[column_index]
        else:
            key = elements[self.columns.index(self.backup_key)].split(", ")[0]
        return key

    def get_aggregate_value(self, acc, x):
        hold_d = copy.deepcopy(acc)
        value_l = do_split(self.delimiter, x.replace("\n", ""))
        for i in range(len(value_l)):
            value = value_l[i] if value_l[i] != "" else "None"
            if self.columns[i] in hold_d:
                hold_d[self.columns[i]] = hold_d[self.columns[i]] + [value]
            else:
                hold_d[self.columns[i]] = [value]
        return hold_d


@curry
class AggregatedCOSMICSources(LazyFileSource):
    def __init__(self, filename, cosmic_tsv, include_header=True, **meta):
        self.cosmic_vcf = filename
        self.cosmic_tsv = cosmic_tsv
        self.include_header = include_header
        self.meta = meta

        if __TYPE__ not in meta:
            self.meta = assoc(self.meta, __TYPE__, DocType.AGGREGATE.value)

        super().__init__(filename)

    def __iter__(self):
        # noinspection PyUnresolvedReferences
        if self.include_header:
            yield self.create_header()

        # iterate through the VCF, creating one value per row
        vcf_file_source = DelimitedFileSource(
            filename=self.cosmic_vcf,
            columns=[
                "#CHROM",
                "POS",
                "ID",
                "REF",
                "ALT",
                "QUAL",
                "FILTER",
                "INFO",
            ],
            delimiter="\t",
            skip_comment=True,
            comment_char="##",
            include_header=False,
        )

        # This is a list of dictionaries.
        cosmic_vcf_records = self.parse_vcf_file(vcf_file_source)

        # Read in the TSV source
        cosmic_tsv_source = DelimitedFileSource(
            filename=self.cosmic_tsv,
            columns=COSMIC_TSV_COLUMNS,
            delimiter="\t",
            include_header=False,
        )

        # Aggregate TSV records together that have the same
        # MUTATION_ID value. The result is a dict of dicts.
        # The key of the top-level dict is the MUTATION_ID.
        # The values are dictionaries containing the gene value,
        # GENOMIC_MUTATION_ID (COSV ID), LEGACY_MUTATION_ID,
        # and tissue/resistance mutation counts.
        cosmic_tsv_dict = reduceby(
            key=self.cosmic_key_value,
            binop=self.cosmic_aggregate_value,
            # skip rows without a genomic mutation ID
            seq=[
                row
                for row in cosmic_tsv_source
                if row.get("GENOMIC_MUTATION_ID")
                not in ["", None, "GENOMIC_MUTATION_ID"]
            ],
            init={
                "CNT": 0,
                "TISSUES": {},
                "TISSUES_FREQ": {},
                "RESISTANCE_MUTATION": {},
            },
        )

        # add tissue frequency
        cosmic_tsv_dict = self.process_tissue_freqs(cosmic_tsv_dict)

        # Group the aggregated TSV records by GENOMIC_MUTATION_ID.
        # This is basically just done to speed up performance in the
        # merge step following this. Multiple mutation_ids can have
        # the same genomic mutation id, so this dictionary will have a
        # key that's a particular genomic id and the value is a list
        # of the aggregated TSV dictionaries that have that g_m_id.
        g_m_id_to_tsv_records = self.group_tsv_by_g_m_id(cosmic_tsv_dict)

        # Merge VCF rows with its corresponding aggregated TSV record.
        merged_records = self.merge_vcf_tsv(
            cosmic_vcf_records, g_m_id_to_tsv_records
        )

        # At this point, we have a list of dictionaries, one per VCF line.
        # Each VCF line has been matched to a particular aggregated TSV
        # grouping based on MUTATION_ID. Now, we need to do one final
        # merge step where we merge these merged records together
        # if they have the same CSRA. For the fields other than
        # CHROM, POS, REF, and ALT, the field values will be lists
        # with the data striped across.
        csra_merged_records = reduceby(
            key=self.merge_key_value,
            binop=self.merge_aggregate_value,
            seq=merged_records,
            init={},
        )

        # yield these merged records
        for _, value in csra_merged_records.items():
            if value.get("#CHROM"):
                value["__type__"] = DocType.AGGREGATE.value
                yield value

    def create_header(self):
        return {
            __TYPE__: DocType.HEADER.value,
            __CHILD__: self.meta.get(__TYPE__),
            # "columns": self.columns,
            "meta": self.meta,
            "file_path": self.name,
        }

    def cosmic_key_value(self, element):
        return element["MUTATION_ID"]

    def group_tsv_by_g_m_id(self, cosmic_tsv_dict):
        g_m_id_to_tsv_map = {}
        for mut_id, tsv_record_info in cosmic_tsv_dict.items():
            g_m_id = tsv_record_info.get("GENOMIC_MUTATION_ID")
            record_copy = copy.deepcopy(tsv_record_info)
            record_copy["MUTATION_ID"] = mut_id
            g_m_id_to_tsv_map.setdefault(g_m_id, []).append(record_copy)
        return g_m_id_to_tsv_map

    def merge_vcf_tsv(self, vcf_records, g_m_id_to_tsvs):  # pragma: no mccabe
        # For each row in the VCF file, find a matching TSV
        # record. To "match", the GENE/Gene name values need to match,
        # the GENOMIC_MUTATION_ID/ID (COSV) values need to match,
        # and the LEGACY_MUTATION_ID/LEGACY_ID values need to match.

        merged_records = []
        vcf_with_no_tsv_match = []
        for vcf_record in vcf_records:
            g_m_id = vcf_record.get("ID")
            gene = vcf_record.get("GENE")
            legacy_id = vcf_record.get("LEGACY_ID")

            # get the list of the TSV records that have
            # this genomic_mutation_id
            tsv_records_with_g_m_id = g_m_id_to_tsvs.get(g_m_id, [])
            matching_tsv = None
            for tsv_record in tsv_records_with_g_m_id:
                if gene == tsv_record.get(
                    "Gene name"
                ) and legacy_id == tsv_record.get("LEGACY_MUTATION_ID"):
                    # this is a match!
                    matching_tsv = tsv_record
                    break

            if matching_tsv is None:
                vcf_with_no_tsv_match.append(vcf_record)
                continue

            # If we made it down here, we have a matching TSV record!
            # Remove this particular record from tsv_records_with_g_m_id
            # because this has matched a VCF line and will not match any
            # other VCF lines.
            _ = tsv_records_with_g_m_id.remove(matching_tsv)

            # Now, merge the matching_tsv record with the vcf line.
            # Note: for any shared fields (there shouldn't be any),
            # the VCF record will overwrite the TSV.
            matching_tsv.update(vcf_record)
            merged_records.append(matching_tsv)

        # at this point, we've combined all of the records that matched.
        # If there are any records that have not matched, throw an error
        # and print them out here.
        tsv_with_no_vcf_match = []
        for g_m_id, tsvs_with_g_m_id in g_m_id_to_tsvs.items():
            if len(tsvs_with_g_m_id) > 0:
                tsv_with_no_vcf_match.extend(tsvs_with_g_m_id)

        if len(tsv_with_no_vcf_match) > 0 or len(vcf_with_no_tsv_match) > 0:
            tsv_records_no_match = ", ".join(
                [str(v) for v in tsv_with_no_vcf_match]
            )
            vcf_records_no_match = ", ".join(
                [str(v) for v in vcf_with_no_tsv_match]
            )
            exception_text = (
                f"\nTSV records with no match: {tsv_records_no_match}."
            )
            exception_text += (
                f"\nVCF records with no match: {vcf_records_no_match}"
            )
            raise Exception(exception_text)

        # if all values have a match, then return the merged records
        return merged_records

    def cosmic_aggregate_value(self, acc, x):  # pragma: no mccabe
        hold_d = copy.deepcopy(acc)

        # add gene name to the aggregated dict
        gene_name = x.get("Gene name")
        if "Gene name" not in hold_d:
            hold_d["Gene name"] = gene_name
        else:
            # throw exception if the gene name for this row
            # does not match the gene name previously found
            # for this mutation ID
            if gene_name != hold_d["Gene name"]:
                raise Exception(
                    f"TSV data error. Mutation ID {x.get('MUTATION_ID')} "
                    f"contains more than one value for Gene name. Values "
                    f"found are: {hold_d['Gene name']} and {gene_name}."
                )

        # add GENOMIC_MUTATION_ID to the aggregated dict
        g_m_id = x.get("GENOMIC_MUTATION_ID")
        if "GENOMIC_MUTATION_ID" not in hold_d:
            hold_d["GENOMIC_MUTATION_ID"] = g_m_id
        else:
            # throw exception if the g_m_id for this row
            # does not match the g_m_id previously found
            # for this mutation ID
            if g_m_id != hold_d["GENOMIC_MUTATION_ID"]:
                raise Exception(
                    f"TSV data error. Mutation ID {x.get('MUTATION_ID')} "
                    f"contains more than one value for GENOMIC_MUTATION_ID. "
                    f"Values found are: {hold_d['GENOMIC_MUTATION_ID']} "
                    f"and {g_m_id}."
                )

        # add LEGACY_MUTATION_ID to the aggregated dict
        l_m_id = x.get("LEGACY_MUTATION_ID")
        if "LEGACY_MUTATION_ID" not in hold_d:
            hold_d["LEGACY_MUTATION_ID"] = l_m_id
        else:
            # throw exception if the l_m_id for this row
            # does not match the l_m_id previously found
            # for this mutation ID
            if l_m_id != hold_d["LEGACY_MUTATION_ID"]:
                raise Exception(
                    f"TSV data error. Mutation ID {x.get('MUTATION_ID')} "
                    f"contains more than one value for LEGACY_MUTATION_ID. "
                    f"Values found are: {hold_d['LEGACY_MUTATION_ID']} "
                    f"and {l_m_id}."
                )

        # update the counts for the tissue sites and resistance mutations
        hold_d["CNT"] += 1
        if x.get("Primary site") in hold_d["TISSUES"]:
            hold_d["TISSUES"][x.get("Primary site")] += 1
        else:
            hold_d["TISSUES"][x.get("Primary site")] = 1
        if x.get("Resistance Mutation") in hold_d["RESISTANCE_MUTATION"]:
            hold_d["RESISTANCE_MUTATION"][x.get("Resistance Mutation")] += 1
        else:
            hold_d["RESISTANCE_MUTATION"][x.get("Resistance Mutation")] = 1
        return hold_d

    def process_tissue_freqs(self, cosmic_dict):
        for ck, cv in cosmic_dict.items():
            for k, v in cv["TISSUES"].items():
                cosmic_dict[ck]["TISSUES_FREQ"][k] = float(v) / cv["CNT"]
        return cosmic_dict

    def parse_vcf_file(self, vcf_file_iter):
        # create a list of dictionaries (one per VCF line)
        vcf_records = []
        for row in vcf_file_iter:
            # do not include header
            if row["#CHROM"] == "#CHROM":
                continue

            # skip over too long REF/ALTs
            if len(row["REF"]) > 1400 or len(row["ALT"]) >= 1400:
                continue

            # get all of the values from this row
            row_dict = {}
            for col_name in ["#CHROM", "POS", "REF", "ALT", "ID", "INFO"]:
                row_dict[col_name] = row[col_name]

            # process vcf info
            self.process_vcf_info(row_dict)

            vcf_records.append(row_dict)
        return vcf_records

    def process_vcf_info(self, v):
        if v.get("#CHROM") == "#CHROM":
            return
        # add values from INFO column to the dictionary
        if "CDS" in v["INFO"]:
            v["CDS"] = [x for x in v["INFO"].split(";") if x[:3] == "CDS"][
                0
            ].split("=", 1)[1]
        else:
            v["CDS"] = "None"

        if "AA" in v["INFO"]:
            v["AA"] = [x for x in v["INFO"].split(";") if x[:2] == "AA"][
                0
            ].split("=", 1)[1]
        else:
            v["AA"] = "None"

        if "LEGACY_ID" in v["INFO"]:
            v["LEGACY_ID"] = [
                x for x in v["INFO"].split(";") if x[:9] == "LEGACY_ID"
            ][0].split("=", 1)[1]
        else:
            v["LEGACY_ID"] = "None"

        if "GENE" in v["INFO"]:
            v["GENE"] = [x for x in v["INFO"].split(";") if x[:4] == "GENE"][
                0
            ].split("=", 1)[1]
        else:
            v["Gene"] = "None"

    def merge_key_value(self, element):
        return "-".join(
            [element["#CHROM"], element["POS"], element["REF"], element["ALT"]]
        )

    def merge_aggregate_value(self, acc, x):
        hold_d = copy.deepcopy(acc)
        # these fields are single_valued
        for key in ["#CHROM", "POS", "REF", "ALT"]:
            if key not in hold_d:
                hold_d[key] = x[key]
        # these fields will all be striped across the
        for key in [
            "GENE",
            "CNT",
            "MUTATION_ID",
            "ID",  # this is the same as GENOMIC_MUTATION_ID in TSV
            "TISSUES",
            "TISSUES_FREQ",
            "RESISTANCE_MUTATION",
            "CDS",
            "AA",
            "LEGACY_ID",  # this is the same as LEGACY_MUTATION_ID in TSV
        ]:
            if key not in hold_d:
                hold_d[key] = [x[key]]
            else:
                hold_d[key] = hold_d[key] + [x[key]]
        return hold_d


COSMIC_TSV_COLUMNS = [
    "Gene name",
    "Accession Number",
    "Gene CDS length",
    "HGNC ID",
    "Sample name",
    "ID_sample",
    "ID_tumour",
    "Primary site",
    "Site subtype 1",
    "Site subtype 2",
    "Site subtype 3",
    "Primary histology",
    "Histology subtype 1",
    "Histology subtype 2",
    "Histology subtype 3",
    "Genome-wide screen",
    "GENOMIC_MUTATION_ID",
    "LEGACY_MUTATION_ID",
    "MUTATION_ID",
    "Mutation CDS",
    "Mutation AA",
    "Mutation Description",
    "Mutation zygosity",
    "LOH",
    "GRCh",
    "Mutation genome position",
    "Mutation strand",
    "SNP",
    "Resistance Mutation",
    "FATHMM prediction",
    "FATHMM score",
    "Mutation somatic status",
    "Pubmed_PMID",
    "ID_STUDY",
    "Sample Type",
    "Tumour origin",
    "Age",
    "HGVSP",
    "HGVSC",
    "HGVSG",
]
