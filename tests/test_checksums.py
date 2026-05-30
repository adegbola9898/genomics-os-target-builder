from pathlib import Path

from target_builder.checksums import build_sha256s, sha256_file, write_sha256s


def test_sha256_file(tmp_path: Path):
    p = tmp_path / "example.txt"
    p.write_text("hello\n")

    assert sha256_file(p) == "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03"


def test_build_and_write_sha256s(tmp_path: Path):
    p = tmp_path / "a.txt"
    p.write_text("a")

    checksums = build_sha256s([p])

    out = tmp_path / "SHA256SUMS.txt"
    write_sha256s(out, checksums)

    assert "a.txt" in out.read_text()
    assert checksums["a.txt"] in out.read_text()
