from target_builder.bed_ops import Interval


def total_bases(intervals: list[Interval]) -> int:
    return sum(end - start for _chrom, start, end, _gene, _tx in intervals)


def count_genes(intervals: list[Interval]) -> int:
    return len({gene for _chrom, _start, _end, gene, _tx in intervals})


def build_qc_summary(
    requested_genes: list[str],
    resolved_genes: list[str],
    transcripts: dict[str, str],
    gene_labeled_intervals: list[Interval],
    panel_union_intervals: list[tuple[str, int, int, str]],
) -> dict:
    return {
        "requested_gene_count": len(requested_genes),
        "resolved_gene_count": len(set(resolved_genes)),
        "mane_transcript_count": len(transcripts),
        "gene_labeled_interval_count": len(gene_labeled_intervals),
        "panel_union_interval_count": len(panel_union_intervals),
        "gene_labeled_total_bases": total_bases(gene_labeled_intervals),
        "panel_union_total_bases": sum(
            end - start for _chrom, start, end, _label in panel_union_intervals
        ),
        "genes_with_mane_transcripts": sorted(transcripts.keys()),
    }
