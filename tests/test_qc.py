from target_builder.qc import build_qc_summary, count_genes, total_bases


def test_total_bases():
    intervals = [
        ("1", 10, 20, "A", "TX1"),
        ("1", 30, 50, "B", "TX2"),
    ]
    assert total_bases(intervals) == 30


def test_count_genes():
    intervals = [
        ("1", 10, 20, "A", "TX1"),
        ("1", 30, 50, "A", "TX1"),
        ("1", 60, 70, "B", "TX2"),
    ]
    assert count_genes(intervals) == 2


def test_build_qc_summary():
    intervals = [
        ("1", 10, 20, "A", "TX1"),
        ("1", 30, 50, "B", "TX2"),
    ]
    union = [
        ("1", 10, 20, "PANEL_UNION"),
        ("1", 30, 50, "PANEL_UNION"),
    ]

    qc = build_qc_summary(
        requested_genes=["A", "B"],
        resolved_genes=["A", "B"],
        transcripts={"A": "TX1", "B": "TX2"},
        gene_labeled_intervals=intervals,
        panel_union_intervals=union,
    )

    assert qc["requested_gene_count"] == 2
    assert qc["mane_transcript_count"] == 2
    assert qc["gene_labeled_total_bases"] == 30
    assert qc["panel_union_total_bases"] == 30
