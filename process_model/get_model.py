import spacy
from process_model.patterns import patterns
from spacy.pipeline import EntityRuler
from spacy.util import compile_infix_regex

reg = '(?<=[0-9])[+\\-\\*^](?=[0-9-])'

def my_nlp(model):
    nlp = spacy.load(model)
    list_infixes_defaults = list(nlp.Defaults.infixes)
    if reg in list_infixes_defaults:
        list_infixes_defaults.remove(reg)
    # modify tokenizer infix patterns(dd-dd-dd)
    infixes = (list_infixes_defaults + [r"(?<=[0-9])[\+\*^](?=[0-9-])"])
    infix_re = compile_infix_regex(infixes)

    nlp.tokenizer.infix_finditer = infix_re.finditer
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler, before='ner')
    return nlp
