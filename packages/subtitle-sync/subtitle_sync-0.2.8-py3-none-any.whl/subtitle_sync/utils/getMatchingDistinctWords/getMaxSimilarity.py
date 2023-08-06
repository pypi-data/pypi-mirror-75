from subtitle_sync.constants import PASSING_SIMILARITY_SCORE, FAILING_SIMILARITY_SCORE
from subtitle_sync.utils.getMatchingDistinctWords.searchAlgorithms import (
    logSearch,
    expansionSearch,
)
from subtitle_sync.utils.getMatchingDistinctWords.getSimilarity import getSimilarity
from subtitle_sync.utils.helper import splitDialogue


def trimSentence(nlp, maxDialogueTokens, minDialogueTokens):
    maxLemma = nlp(" ".join(maxDialogueTokens))
    startIndex = None
    minIndex = 0
    while startIndex == None and minIndex < len(minDialogueTokens):
        minLemma = nlp(minDialogueTokens[minIndex])[0]
        minLemma = minLemma.text if minLemma.lemma_ == "-PRON-" else minLemma.lemma_
        index = 0
        for token in maxLemma:
            token = token.text if token.lemma_ == "-PRON-" else token.lemma_
            if not token.isalnum():
                continue
            if token == minLemma:
                startIndex = index
                break
            index += 1
        minIndex += 1

    endIndex = None
    minIndex = len(minDialogueTokens) - 1
    while (
        (startIndex is None or minIndex < startIndex)
        and endIndex == None
        and minIndex >= 0
    ):
        minLemma = nlp(minDialogueTokens[minIndex])[0]
        minLemma = minLemma.text if minLemma.lemma_ == "-PRON-" else minLemma.lemma_
        index = len(maxLemma) - 1
        for token in reversed(maxLemma):
            token = token.text if token.lemma_ == "-PRON-" else token.lemma_
            if not token.isalnum():
                continue
            if token == minLemma:
                endIndex = index
                break
            index -= 1
        minIndex -= 1
    return [
        startIndex if startIndex else 0,
        endIndex if endIndex else len(maxDialogueTokens) - 1,
    ]


def getMaxSimilarity(nlp, maxDialogue, minDialogue, subsWord, minSorted, maxSorted):
    index = 0
    maxSimilarity = 0
    maxIndex = 0

    maxDialogueTokens = splitDialogue(maxDialogue["dialogue"])
    minDialogueTokens = splitDialogue(minDialogue["dialogue"])

    # if they have the same length, then compare once.
    # TODO: may need to revisit. doesn't make sense if we go with the "linked list" approach
    if len(minDialogue["dialogue"]) >= len(maxDialogue["dialogue"]):
        maxSimilarity = getSimilarity(
            nlp, maxDialogueTokens, minDialogueTokens, index, None,
        )
        maxIndex = index
    else:
        (maxSimilarity, maxIndex) = expansionSearch.expansionSearch(
            nlp, maxDialogue, minDialogue, minSorted, maxSorted,
        )
        if (
            maxSimilarity >= PASSING_SIMILARITY_SCORE
            or maxSimilarity <= FAILING_SIMILARITY_SCORE
        ):
            return (round(maxSimilarity, 3), maxIndex)
        else:
            startEndIndex = trimSentence(nlp, maxDialogueTokens, minDialogueTokens)
            if len(maxDialogueTokens) <= 260:
                (logMaxSimilarity, logMaxIndex, pairDone) = logSearch.logSearch(
                    nlp,
                    minDialogueTokens,
                    maxDialogueTokens,
                    startEndIndex[0],
                    startEndIndex[1],
                    maxSimilarity,
                    0,
                    {},
                    subsWord,
                )
                if logMaxSimilarity > maxSimilarity:
                    maxSimilarity = logMaxSimilarity
                    maxIndex = logMaxIndex

    maxSimilarity = round(maxSimilarity, 3)
    if maxSimilarity >= 1 and len(minDialogue["dialogue"]) != len(
        maxDialogue["dialogue"]
    ):
        maxSimilarity = 0.99
    return (maxSimilarity, maxIndex)

    93
