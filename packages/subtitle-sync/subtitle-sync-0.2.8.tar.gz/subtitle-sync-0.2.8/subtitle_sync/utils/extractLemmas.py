import copy
import re


def extractLemmaSubs(nlp, subtitle):
    subsLemma = []
    for line in subtitle:
        doc = nlp(line["content"])
        tokens = [
            re.sub(
                "(?<=[0-9])(?:st|nd|rd|th)", "", token.lemma_
            )  # remove ordinal indicators
            for token in doc
            if not token.is_punct
        ]
        subsLemma.append(
            {
                "lemma": tokens,
                "content": line["content"],
                "start": line["start"].seconds,
                "end": line["end"].seconds,
            }
        )

    return subsLemma


def extractLemmaScript(nlp, script):
    def returnLemma(dialogue):
        screenplayWithoutStopWords = []

        # extract lemma from dialogue
        doc = nlp(dialogue.lower())
        tokens = [
            re.sub(
                "(?<=[0-9])(?:st|nd|rd|th)", "", token.lemma_.replace("--", "")
            )  # remove ordinal indicators
            for token in doc
            if not token.is_punct
        ]
        screenplayWithoutStopWords += tokens
        return screenplayWithoutStopWords

    scriptLemma = []
    for content in script:
        scriptLemma.append(copy.copy(content))
        scriptLemma[-1]["lemma"] = returnLemma(content["dialogue"])
    return scriptLemma
