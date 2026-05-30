ALIASES = {
    "FAM175A": "ABRAXAS1",
    "MRE11A": "MRE11",
}


def resolve_gene_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    return ALIASES.get(symbol, symbol)
