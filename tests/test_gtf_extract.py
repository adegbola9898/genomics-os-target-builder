from pathlib import Path

from target_builder.gtf_extract import extract_attr, iter_cds_intervals_for_transcripts
from target_builder.transcript_selector import find_mane_transcripts


def test_extract_attr():
    attrs = 'gene_id "ENSG00000012048"; gene_name "BRCA1"; transcript_id "ENST00000357654";'
    assert extract_attr(attrs, "gene_name") == "BRCA1"
    assert extract_attr(attrs, "transcript_id") == "ENST00000357654"


def test_extract_attr_missing():
    attrs = 'gene_id "ENSG00000012048";'
    assert extract_attr(attrs, "gene_name") is None


def test_extract_brca1_brca2_mane_cds_intervals():
    gtf = Path("references/grch38/Homo_sapiens.GRCh38.115.gtf.gz")
    transcripts = find_mane_transcripts(gtf, {"BRCA1", "BRCA2"})

    intervals = list(iter_cds_intervals_for_transcripts(gtf, transcripts))

    assert len(intervals) > 0
    assert {row[3] for row in intervals} == {"BRCA1", "BRCA2"}

    for chrom, start, end, gene, transcript_id in intervals:
        assert chrom in {"13", "17"}
        assert start >= 0
        assert end > start
        assert gene in {"BRCA1", "BRCA2"}
        assert transcript_id.startswith("ENST")
