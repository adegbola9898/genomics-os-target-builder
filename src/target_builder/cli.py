import argparse
import json
from pathlib import Path

from target_builder.bed_ops import (
    load_fai_lengths,
    make_panel_union,
    merge_intervals_per_gene,
    pad_intervals,
)
from target_builder.gtf_extract import iter_cds_intervals_for_transcripts
from target_builder.manifest import build_manifest
from target_builder.qc import build_qc_summary
from target_builder.resolver import resolve_gene_symbol
from target_builder.transcript_selector import find_mane_transcripts


DEFAULT_GTF = Path("references/grch38/Homo_sapiens.GRCh38.115.gtf.gz")
DEFAULT_FAI = Path("references/grch38/genome.fa.fai")


def read_genes(path: Path) -> list[str]:
    genes = []
    with path.open("rt") as fh:
        for line in fh:
            value = line.strip()
            if not value or value.startswith("#"):
                continue
            genes.append(value)
    return genes


def write_gene_labeled_bed(path: Path, intervals) -> None:
    with path.open("wt") as out:
        for chrom, start, end, gene, transcript_id in intervals:
            out.write(f"{chrom}\t{start}\t{end}\t{gene}|{transcript_id}\n")


def write_panel_union_bed(path: Path, intervals) -> None:
    with path.open("wt") as out:
        for chrom, start, end, label in intervals:
            out.write(f"{chrom}\t{start}\t{end}\t{label}\n")


def write_gene_symbol_mapping(
    path: Path,
    requested_genes: list[str],
    resolved_genes: list[str],
    transcripts: dict[str, str],
) -> None:
    with path.open("wt") as out:
        out.write("requested_gene\tresolved_gene\ttranscript_id\n")
        for requested, resolved in zip(requested_genes, resolved_genes, strict=True):
            transcript_id = transcripts.get(resolved, "")
            out.write(f"{requested}\t{resolved}\t{transcript_id}\n")


def build(args) -> None:
    genes_path = Path(args.genes)
    outdir = Path(args.outdir)
    gtf = Path(args.gtf)
    fai = Path(args.fai)

    outdir.mkdir(parents=True, exist_ok=True)

    requested_genes = read_genes(genes_path)
    resolved_genes = [resolve_gene_symbol(gene) for gene in requested_genes]

    transcripts = find_mane_transcripts(gtf, set(resolved_genes))

    missing = sorted(set(resolved_genes) - set(transcripts.keys()))
    if missing:
        raise SystemExit(f"Missing MANE transcripts for genes: {', '.join(missing)}")

    cds_intervals = list(iter_cds_intervals_for_transcripts(gtf, transcripts))
    merged = merge_intervals_per_gene(cds_intervals)

    contig_lengths = load_fai_lengths(fai)
    padded = pad_intervals(merged, contig_lengths, args.padding)
    padded_merged = merge_intervals_per_gene(padded)

    panel_union = make_panel_union(padded_merged)

    gene_labeled_path = outdir / "targets.mane_cds.gene_labeled.bed"
    panel_union_path = outdir / "targets.mane_cds.panel_union.bed"
    qc_path = outdir / "target_qc.json"
    manifest_path = outdir / "target_manifest.json"
    mapping_path = outdir / "gene_symbol_mapping.tsv"

    write_gene_labeled_bed(gene_labeled_path, padded_merged)
    write_panel_union_bed(panel_union_path, panel_union)
    write_gene_symbol_mapping(mapping_path, requested_genes, resolved_genes, transcripts)

    qc = build_qc_summary(
        requested_genes=requested_genes,
        resolved_genes=resolved_genes,
        transcripts=transcripts,
        gene_labeled_intervals=padded_merged,
        panel_union_intervals=panel_union,
    )

    manifest = build_manifest(
        requested_genes=requested_genes,
        resolved_genes=resolved_genes,
        transcripts=transcripts,
        padding_bp=args.padding,
        gtf_path=gtf,
        fai_path=fai,
        gene_labeled_bed=gene_labeled_path,
        panel_union_bed=panel_union_path,
        qc=qc,
    )

    qc_path.write_text(json.dumps(qc, indent=2) + "\n")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    print("Target build complete")
    print(f"Requested genes: {qc['requested_gene_count']}")
    print(f"Resolved genes: {qc['resolved_gene_count']}")
    print(f"MANE transcripts: {qc['mane_transcript_count']}")
    print(f"Gene-labeled intervals: {qc['gene_labeled_interval_count']}")
    print(f"Panel-union intervals: {qc['panel_union_interval_count']}")
    print(f"Gene-labeled total bases: {qc['gene_labeled_total_bases']}")
    print(f"Panel-union total bases: {qc['panel_union_total_bases']}")
    print(f"Wrote: {gene_labeled_path}")
    print(f"Wrote: {panel_union_path}")
    print(f"Wrote: {qc_path}")
    print(f"Wrote: {manifest_path}")
    print(f"Wrote: {mapping_path}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="target-builder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--genes", required=True)
    build_parser.add_argument("--outdir", required=True)
    build_parser.add_argument("--padding", type=int, default=10)
    build_parser.add_argument("--gtf", default=str(DEFAULT_GTF))
    build_parser.add_argument("--fai", default=str(DEFAULT_FAI))
    build_parser.set_defaults(func=build)

    args = parser.parse_args()
    args.func(args)
