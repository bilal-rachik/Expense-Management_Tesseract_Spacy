patterns = [
    # DATE
    {"label": "Date",
     "pattern": [{"TEXT": {"REGEX": "^\s*(3[01]|[12][0-9]|0?[1-9])[./-](1[012]|0?[1-9])[./-](\d)\s*"}}]},

    {"label": "Date",
     "pattern": [{"TEXT": {"REGEX": "\s*(\d)\s*[./-](1[012]|0?[1-9])[/.-](3[01]|[12][0-9]|0?[1-9])\s*"}}]},

    {"label": "Date", "pattern": [{"TEXT": {
        "REGEX": "^\s*(3[01]|[12][0-9]|0?[1-9])\s*[ ./-](?:janvier|janv|février|fevrier|févr|fevr|mars|avril|avr|mai|maï|juin|juillet|juil|juill|aout|août|septemre|sept|octobre|oct|novembre|nov|décemebre|decemebre|dec|déc)\s*[ ./-](\d)\s*"}}]},
    {"label": "Date", "pattern": [{"TEXT": {"REGEX": "(3[01]|[12][0-9]|0?[1-9])"}},
                                  {"TEXT": {
                                      "REGEX": "(?:janvier|janv|février|fevrier|févr|fevr|mars|avril|avr|mai|maï|juin|juillet|juil|juill|aout|août|septemre|sept|octobre|oct|novembre|nov|décemebre|decemebre|dec|déc)"}},
                                  {"TEXT": {"REGEX": "(3[01]|[12][0-9]|0?[1-9])"}}]}

    # TOTALE
    #{"label": "TTC", "pattern": [{"LOWER": "total"}, {"LIKE_NUM": True}]},
    #{"label": "TTC", "pattern": [{"LOWER": "MONTANT"}, {"LIKE_NUM": True}]}
]


