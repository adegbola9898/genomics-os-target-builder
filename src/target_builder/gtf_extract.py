import gzip
from pathlib import Path


def extract_attr(attributes: str, key: str) -> str | None:
    marker = f'{key} "'
    if marker not in attributes:
        return None
    return attributes.split(marker, 1)[1].split('"', 1)[0]


def iter_cds_intervals_for_transcripts(
    gtf_path: Path,
    transcript_by_gene: dict[str, str],
):
    wanted_transcripts = set(transcript_by_gene.values())

    with gzip.open(gtf_path, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue

            fields = line.rstrip().split("\t")
            if len(fields) != 9:
                continue

            chrom, _source, feature_type, start, end, _score, _strand, _phase, attributes = fields

            if feature_type != "CDS":
                continue

            transcript_id = extract_attr(attributes, "transcript_id")
            if transcript_id not in wanted_transcripts:
                continue

            gene_name = extract_attr(attributes, "gene_name")
            if gene_name is None:
                continue

            # GTF: 1-based inclusive. BED: 0-based half-open.
            yield (
                chrom,
                int(start) - 1,
                int(end),
                gene_name.upper(),
                transcript_id,
            )
