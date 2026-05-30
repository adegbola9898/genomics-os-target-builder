import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def build_sha256s(paths: list[Path]) -> dict[str, str]:
    return {path.name: sha256_file(path) for path in paths}


def write_sha256s(path: Path, checksums: dict[str, str]) -> None:
    with path.open("wt") as out:
        for filename, checksum in sorted(checksums.items()):
            out.write(f"{checksum}  {filename}\n")
