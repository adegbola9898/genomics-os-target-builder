from target_builder.bed_ops import (
    make_panel_union,
    merge_intervals_per_gene,
    pad_intervals,
    sort_intervals,
)


def test_sort_intervals():
    intervals = [
        ("17", 20, 30, "BRCA1", "TX1"),
        ("13", 10, 20, "BRCA2", "TX2"),
    ]

    assert sort_intervals(intervals)[0][0] == "13"


def test_merge_intervals_per_gene():
    intervals = [
        ("17", 10, 20, "BRCA1", "TX1"),
        ("17", 18, 30, "BRCA1", "TX1"),
        ("17", 18, 30, "BRCA1", "TX2"),
    ]

    merged = merge_intervals_per_gene(intervals)

    assert ("17", 10, 30, "BRCA1", "TX1") in merged
    assert ("17", 18, 30, "BRCA1", "TX2") in merged


def test_pad_intervals_respects_bounds():
    intervals = [
        ("1", 5, 10, "GENE1", "TX1"),
        ("1", 95, 100, "GENE2", "TX2"),
    ]

    padded = pad_intervals(intervals, {"1": 100}, padding_bp=10)

    assert padded[0] == ("1", 0, 20, "GENE1", "TX1")
    assert padded[1] == ("1", 85, 100, "GENE2", "TX2")


def test_make_panel_union():
    intervals = [
        ("1", 10, 20, "GENE1", "TX1"),
        ("1", 18, 30, "GENE2", "TX2"),
        ("1", 40, 50, "GENE3", "TX3"),
    ]

    union = make_panel_union(intervals)

    assert union == [
        ("1", 10, 30, "PANEL_UNION"),
        ("1", 40, 50, "PANEL_UNION"),
    ]
