from target_builder.resolver import resolve_gene_symbol


def test_resolves_known_aliases():
    assert resolve_gene_symbol("FAM175A") == "ABRAXAS1"
    assert resolve_gene_symbol("MRE11A") == "MRE11"


def test_normalizes_case_and_whitespace():
    assert resolve_gene_symbol(" brca1 ") == "BRCA1"


def test_preserves_unknown_symbol_as_uppercase():
    assert resolve_gene_symbol("tp53") == "TP53"
