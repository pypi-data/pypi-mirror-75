from subtitle_sync.constants import PASSING_SIMILARITY_SCORE, FAILING_SIMILARITY_SCORE
from subtitle_sync.utils.getMatchingDistinctWords.getSimilarity import getSimilarity


def logSearch(
    nlp,
    minDialogueTokens,
    maxDialogueTokens,
    low,
    high,
    maxSimilarity,
    maxIndex,
    pairDone,
    subsWord,
):
    # if high >= low is classic condition. high - low >= 3 because it makes less sense to compare something that
    # only has two words in it
    if high >= low and high - low >= 2 and "{} {}".format(low, high) not in pairDone:
        # mid = (high + low) // 2
        similarity = (
            0
            if maxSimilarity == 0
            else getSimilarity(nlp, maxDialogueTokens, minDialogueTokens, low, high,)
        )
        print("low", low)
        print("high", high)

        if similarity > maxSimilarity:
            maxSimilarity = similarity
            maxIndex = low
        if (
            similarity >= PASSING_SIMILARITY_SCORE
            or similarity <= FAILING_SIMILARITY_SCORE
        ):
            pairDone["{} {}".format(low, high)] = True
            return (maxSimilarity, maxIndex, pairDone)

        searchLeftMax = None
        searchRightMax = None
        searchBothMax = None
        searchLeftIndex = None
        searchRightIndex = None
        searchBothIndex = None

        # gotta go faaast
        nextHigh = high - 2

        maxWordSnippet = (
            " ".join(maxDialogueTokens[low : nextHigh + 1])
            if high
            else " ".join(maxDialogueTokens[low:])
        )
        if subsWord in maxWordSnippet:
            (searchLeftMax, searchLeftIndex, pairDone) = logSearch(
                nlp,
                minDialogueTokens,
                maxDialogueTokens,
                low,
                nextHigh,
                maxSimilarity,
                maxIndex,
                pairDone,
                subsWord,
            )
            pairDone["{} {}".format(low, nextHigh)] = True
            if (
                searchLeftMax >= PASSING_SIMILARITY_SCORE
                or searchLeftMax <= FAILING_SIMILARITY_SCORE
            ):
                return (searchLeftMax, searchLeftIndex, pairDone)

        nextLow = low + 2
        maxWordSnippet = (
            " ".join(maxDialogueTokens[nextLow : high + 1])
            if high
            else " ".join(maxDialogueTokens[low:])
        )
        if subsWord in maxWordSnippet:
            (searchRightMax, searchRightIndex, pairDone) = logSearch(
                nlp,
                minDialogueTokens,
                maxDialogueTokens,
                nextLow,
                high,
                maxSimilarity,
                maxIndex,
                pairDone,
                subsWord,
            )
            pairDone["{} {}".format(nextLow, high)] = True

        maxWordSnippet = (
            " ".join(maxDialogueTokens[nextLow : nextHigh + 1])
            if high
            else " ".join(maxDialogueTokens[low:])
        )
        if subsWord in maxWordSnippet:
            (searchRightMax, searchRightIndex, pairDone) = logSearch(
                nlp,
                minDialogueTokens,
                maxDialogueTokens,
                nextLow,
                nextHigh,
                maxSimilarity,
                maxIndex,
                pairDone,
                subsWord,
            )
            pairDone["{} {}".format(nextLow, nextHigh)] = True

        finalList = [
            (searchLeftMax, searchLeftIndex),
            (searchRightMax, searchRightIndex),
            (searchBothMax, searchBothIndex),
        ]
        ultimateMaxSimilarity = None
        ultimateMaxIndex = None
        for el in finalList:
            if ultimateMaxSimilarity is None or (
                el[0] is not None and el[0] > ultimateMaxSimilarity
            ):
                ultimateMaxSimilarity = el[0]
                ultimateMaxIndex = el[1]
        if ultimateMaxSimilarity is not None:
            return (ultimateMaxSimilarity, ultimateMaxIndex, pairDone)
        pairDone["{} {}".format(low, high)] = True
        return (maxSimilarity, maxIndex, pairDone)
    else:
        # Element is not present in the array
        pairDone["{} {}".format(low, high)] = True
        return (maxSimilarity, maxIndex, pairDone)
