import spacy


def nlpSetup():
    try:
        nlp = spacy.load("en_core_web_lg")
    except OSError:
        from spacy.cli import download

        download("en_core_web_lg")
        nlp = spacy.load("en_core_web_lg")

    custom_lookup = {"til": "until", "\u2019sides": "besides"}

    def change_lemma_property(doc):
        for token in doc:
            if token.text in custom_lookup:
                token.lemma_ = custom_lookup[token.text]
        return doc

    nlp.add_pipe(change_lemma_property, first=True)

    specialCase = {
        # do
        "don't": [
            {"ORTH": "do", "LEMMA": "do"},
            {"ORTH": "n't", "LEMMA": "not", "NORM": "not", "TAG": "RB"},
        ],
        "doesn't": [
            {"ORTH": "does", "LEMMA": "do"},
            {"ORTH": "n't", "LEMMA": "not", "NORM": "not", "TAG": "RB"},
        ],
        "didn't": [
            {"ORTH": "did", "LEMMA": "do"},
            {"ORTH": "n't", "LEMMA": "not", "NORM": "not", "TAG": "RB"},
        ],
        # can
        "can't": [
            {"ORTH": "ca", "LEMMA": "can"},
            {"ORTH": "n't", "LEMMA": "not", "NORM": "not", "TAG": "RB"},
        ],
        "couldn't": [
            {"ORTH": "could", "LEMMA": "can"},
            {"ORTH": "n't", "LEMMA": "not", "NORM": "not", "TAG": "RB"},
        ],
        # have
        "I've'": [
            {"ORTH": "I", "LEMMA": "I"},
            {"ORTH": "'ve'", "LEMMA": "have", "NORM": "have", "TAG": "VERB"},
        ],
        "haven't": [
            {"ORTH": "have", "LEMMA": "have"},
            {"ORTH": "n't", "LEMMA": "not", "NORM": "not", "TAG": "RB"},
        ],
        "hasn't": [
            {"ORTH": "has", "LEMMA": "have"},
            {"ORTH": "n't", "LEMMA": "not", "NORM": "not", "TAG": "RB"},
        ],
        "hadn't": [
            {"ORTH": "had", "LEMMA": "have"},
            {"ORTH": "n't", "LEMMA": "not", "NORM": "not", "TAG": "RB"},
        ],
        # will/shall will be replaced by will
        "I'll'": [
            {"ORTH": "I", "LEMMA": "I"},
            {"ORTH": "'ll'", "LEMMA": "will", "NORM": "will", "TAG": "VERB"},
        ],
        "he'll'": [
            {"ORTH": "he", "LEMMA": "he"},
            {"ORTH": "'ll'", "LEMMA": "will", "NORM": "will", "TAG": "VERB"},
        ],
        "she'll'": [
            {"ORTH": "she", "LEMMA": "she"},
            {"ORTH": "'ll'", "LEMMA": "will", "NORM": "will", "TAG": "VERB"},
        ],
        "it'll'": [
            {"ORTH": "it", "LEMMA": "it"},
            {"ORTH": "'ll'", "LEMMA": "will", "NORM": "will", "TAG": "VERB"},
        ],
        "won't": [
            {"ORTH": "wo", "LEMMA": "will"},
            {"ORTH": "n't", "LEMMA": "not", "NORM": "not", "TAG": "RB"},
        ],
        "wouldn't": [
            {"ORTH": "would", "LEMMA": "will"},
            {"ORTH": "n't", "LEMMA": "not", "NORM": "not", "TAG": "RB"},
        ],
        # be
        "I'm'": [
            {"ORTH": "I", "LEMMA": "I"},
            {"ORTH": "'m'", "LEMMA": "be", "NORM": "am", "TAG": "VERB"},
        ],
    }

    for word in specialCase.items():
        nlp.tokenizer.add_special_case(word[0], word[1])

    return nlp
