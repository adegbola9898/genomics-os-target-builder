Interval = tuple[str, int, int, str, str]


def sort_intervals(intervals: list[Interval]) -> list[Interval]:
    return sorted(intervals, key=lambda row: (row[0], row[1], row[2], row[3], row[4]))


def merge_intervals_per_gene(intervals: list[Interval]) -> list[Interval]:
    sorted_rows = sorted(intervals, key=lambda row: (row[3], row[4], row[0], row[1], row[2]))

    merged: list[Interval] = []

    for chrom, start, end, gene, transcript_id in sorted_rows:
        if not merged:
            merged.append((chrom, start, end, gene, transcript_id))
            continue

        last_chrom, last_start, last_end, last_gene, last_tx = merged[-1]

        same_group = (
            chrom == last_chrom
            and gene == last_gene
            and transcript_id == last_tx
        )

        if same_group and start <= last_end:
            merged[-1] = (
                last_chrom,
                last_start,
                max(last_end, end),
                last_gene,
                last_tx,
            )
        else:
            merged.append((chrom, start, end, gene, transcript_id))

    return sort_intervals(merged)


def load_fai_lengths(fai_path) -> dict[str, int]:
    lengths: dict[str, int] = {}

    with open(fai_path, "rt") as fh:
        for line in fh:
            fields = line.rstrip().split("\t")
            if len(fields) < 2:
                continue
            lengths[fields[0]] = int(fields[1])

    return lengths


def pad_intervals(
    intervals: list[Interval],
    contig_lengths: dict[str, int],
    padding_bp: int,
) -> list[Interval]:
    padded: list[Interval] = []

    for chrom, start, end, gene, transcript_id in intervals:
        if chrom not in contig_lengths:
            raise ValueError(f"Unknown contig in FAI: {chrom}")

        padded_start = max(0, start - padding_bp)
        padded_end = min(contig_lengths[chrom], end + padding_bp)

        padded.append((chrom, padded_start, padded_end, gene, transcript_id))

    return padded


def make_panel_union(intervals: list[Interval]) -> list[tuple[str, int, int, str]]:
    rows = sorted((chrom, start, end) for chrom, start, end, _gene, _tx in intervals)

    merged: list[tuple[str, int, int, str]] = []

    for chrom, start, end in rows:
        if not merged:
            merged.append((chrom, start, end, "PANEL_UNION"))
            continue

        last_chrom, last_start, last_end, label = merged[-1]

        if chrom == last_chrom and start <= last_end:
            merged[-1] = (last_chrom, last_start, max(last_end, end), label)
        else:
            merged.append((chrom, start, end, "PANEL_UNION"))

    return merged
