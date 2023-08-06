from subtitle_sync.constants import PASSING_SIMILARITY_SCORE, FAILING_SIMILARITY_SCORE
from subtitle_sync.utils.helper import splitDialogue
from subtitle_sync.utils.getMatchingDistinctWords.getSimilarity import getSimilarity


# TODO: MAKE UP ARTIST dual dialogue problem
# TODO: for search, avoid two words, since it's too general. easy to get false positives
def expansionSearch(nlp, maxDialogue, minDialogue, minSorted, maxSorted):
    # subs and scripts has different property name for dialogues
    MIN_DIALOGUE_PROPERTY = "dialogue" if "sceneNumber" in minSorted[0] else "content"

    def combineSentences(sentences):
        newSentence = []
        for sentence in sentences:
            newSentence += splitDialogue(sentence[MIN_DIALOGUE_PROPERTY])
        return newSentence

    left = []
    right = []
    maxSimilarity = 0
    maxIndex = -1

    maxDialogueTokens = splitDialogue(maxDialogue["dialogue"])
    minDialogueTokens = splitDialogue(minDialogue["dialogue"])

    similarity = getSimilarity(nlp, maxDialogueTokens, minDialogueTokens, 0, None,)

    if ("?" in maxDialogue["dialogue"] and "?" not in minDialogue["dialogue"]) or (
        "?" in minDialogue["dialogue"] and "?" not in maxDialogue["dialogue"]
    ):
        similarity -= 0.03
    MAX_ITERATION = 5
    iterations = 0
    while (
        similarity == None or similarity >= maxSimilarity
    ) and iterations < MAX_ITERATION:
        if similarity is not None and similarity > maxSimilarity:
            maxSimilarity = similarity
            maxIndex = minDialogue["index"]
        if similarity is not None and (
            # if at one point, it's decreased, then the current maxSimilarity is probably
            # really the max similarity
            (maxSimilarity >= PASSING_SIMILARITY_SCORE and similarity < maxSimilarity)
            or similarity <= FAILING_SIMILARITY_SCORE
        ):
            return (maxSimilarity, maxIndex)
        else:
            leftIndex = minDialogue["index"] - (len(left) + 1)
            leftSimilarity = 0
            if leftIndex > 0:
                left.append(minSorted[leftIndex])
                leftSimilarity = getSimilarity(
                    nlp,
                    maxDialogueTokens,
                    combineSentences(left) + minDialogueTokens,
                    0,
                    None,
                )
                if leftSimilarity >= PASSING_SIMILARITY_SCORE:
                    return (leftSimilarity, left[0]["index"])

            rightIndex = minDialogue["index"] + (len(right) + 1)
            rightSimilarity = 0
            if len(minSorted) > rightIndex:
                right.append(minSorted[rightIndex])
                rightSimilarity = getSimilarity(
                    nlp,
                    maxDialogueTokens,
                    minDialogueTokens + combineSentences(right),
                    0,
                    None,
                )
            if rightSimilarity >= leftSimilarity and rightSimilarity > maxSimilarity:
                maxSimilarity = rightSimilarity
            elif leftSimilarity > rightSimilarity and leftSimilarity > maxSimilarity:
                maxSimilarity = leftSimilarity
                maxIndex = left[0]["index"]

        similarity = getSimilarity(
            nlp,
            maxDialogueTokens,
            combineSentences(left) + minDialogueTokens + combineSentences(right),
            0,
            None,
        )
        iterations += 1

    return (maxSimilarity, maxIndex)
