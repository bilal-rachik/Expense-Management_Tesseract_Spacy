from spacy.lang.fr import French
from spacy.util import compile_infix_regex
def clean_text(txt):
    nlp = French()
    listcode = [x + 45 for x in range(99)]
    postalcod = lambda dd, liscode: str(int(dd) * 1000) if dd in liscode else dd
    customize_remove_PUNCT = ['%']
    for w in customize_remove_PUNCT:
        nlp.vocab[w].is_punct = False
    customize_add_PUNCT = ['>', '=', '$', '™', 'eee', 'ee', 'e', "EE", "EEE", "E",":"]
    for w in customize_add_PUNCT:
        nlp.vocab[w].is_punct = True
    reg = '(?<=[0-9])[+\\-\\*^](?=[0-9-])'
    list_infixes_defaults = list(nlp.Defaults.infixes)
    if reg in list_infixes_defaults:
        list_infixes_defaults.remove(reg)
    # modify process_text infix patterns(dd-dd-dd)
    infixes = (list_infixes_defaults + [r"(?<=[0-9])[\+\*^](?=[0-9-])"])
    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer
    doc = nlp(txt)
    tokens = [postalcod(w.text.lower(), listcode) for w in doc if
          w.text != 'n' and not w.is_punct and not w.is_space and not (w.like_num and len(w.text) > 5)
          and not len(w.text) > 11 and not w.is_quote]
    listToStr = ' '.join(map(str, tokens))

    return listToStr

