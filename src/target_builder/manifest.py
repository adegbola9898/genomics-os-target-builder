from datetime import UTC, datetime
from pathlib import Path


def build_manifest(
    *,
    requested_genes: list[str],
    resolved_genes: list[str],
    transcripts: dict[str, str],
    padding_bp: int,
    gtf_path: Path,
    fai_path: Path,
    gene_labeled_bed: Path,
    panel_union_bed: Path,
    qc: dict,
) -> dict:
    return {
        "schema_version": "target_manifest.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "generator": {
            "name": "genomics-os-target-builder",
            "version": "0.1.0",
        },
        "genome": {
            "build": "GRCh38",
            "fai_path": str(fai_path),
        },
        "annotation": {
            "source": "Ensembl",
            "release": "115",
            "gtf_path": str(gtf_path),
        },
        "target_definition": {
            "target_type": "CDS",
            "transcript_policy": "MANE_SELECT",
            "padding_bp": padding_bp,
        },
        "genes": {
            "requested": requested_genes,
            "resolved": resolved_genes,
            "transcripts": transcripts,
        },
        "outputs": {
            "gene_labeled_bed": str(gene_labeled_bed),
            "panel_union_bed": str(panel_union_bed),
        },
        "qc": qc,
    }
