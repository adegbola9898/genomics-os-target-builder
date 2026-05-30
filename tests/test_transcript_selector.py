from pathlib import Path

from target_builder.transcript_selector import find_mane_transcripts


def test_find_brca_mane_transcripts():
    gtf = Path("references/grch38/Homo_sapiens.GRCh38.115.gtf.gz")

    result = find_mane_transcripts(
        gtf,
        {"BRCA1", "BRCA2"},
    )

    assert "BRCA1" in result
    assert "BRCA2" in result

    assert result["BRCA1"].startswith("ENST")
    assert result["BRCA2"].startswith("ENST")
