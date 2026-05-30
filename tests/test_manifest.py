from pathlib import Path

from target_builder.manifest import build_manifest


def test_build_manifest():
    manifest = build_manifest(
        requested_genes=["BRCA1"],
        resolved_genes=["BRCA1"],
        transcripts={"BRCA1": "ENST00000357654"},
        padding_bp=10,
        gtf_path=Path("ref.gtf.gz"),
        fai_path=Path("genome.fa.fai"),
        gene_labeled_bed=Path("targets.gene_labeled.bed"),
        panel_union_bed=Path("targets.panel_union.bed"),
        qc={"requested_gene_count": 1},
    )

    assert manifest["schema_version"] == "target_manifest.v1"
    assert manifest["genome"]["build"] == "GRCh38"
    assert manifest["annotation"]["release"] == "115"
    assert manifest["target_definition"]["transcript_policy"] == "MANE_SELECT"
    assert manifest["genes"]["transcripts"]["BRCA1"] == "ENST00000357654"
    assert manifest["qc"]["requested_gene_count"] == 1
