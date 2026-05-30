import gzip
from pathlib import Path


def find_mane_transcripts(gtf_path: Path, genes: set[str]) -> dict[str, str]:
    result = {}

    with gzip.open(gtf_path, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue

            if 'tag "MANE_Select"' not in line:
                continue

            fields = line.rstrip().split("\t")

            if len(fields) != 9:
                continue

            if fields[2] != "transcript":
                continue

            attrs = fields[8]

            gene_marker = 'gene_name "'
            tx_marker = 'transcript_id "'

            if gene_marker not in attrs:
                continue

            gene = attrs.split(gene_marker, 1)[1].split('"', 1)[0].upper()

            if gene not in genes:
                continue

            transcript_id = attrs.split(tx_marker, 1)[1].split('"', 1)[0]

            result[gene] = transcript_id

    return result
