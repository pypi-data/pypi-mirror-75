import re
import collections
import string
import copy

from utils.getMatchingDistinctWords.getMaxSimilarity import getMaxSimilarity

PASSING_SIMILARITY_SCORE = 0.71
FAILING_SIMILARITY_SCORE = 0.38


def isGoodEnough(
    nlp, scriptContent, subsContent, subsWord, subs, scripts,
):
    # minimum dialogue length between script line and subtitle
    minDialogue = subsContent
    maxDialogue = scriptContent
    minSorted = subs
    maxSorted = scripts
    if len(scriptContent["lemma"]) < len(subsContent["lemma"]):
        minDialogue = scriptContent
        maxDialogue = subsContent
        minSorted = scripts
        maxSorted = subs

    if len(minDialogue["lemma"]) == len(maxDialogue["lemma"]) and collections.Counter(
        minDialogue["lemma"]
    ) == collections.Counter(maxDialogue["lemma"]):
        maxSimilarity = 0.99
        maxIndex = 0
    else:
        maxSimilarity, maxIndex = getMaxSimilarity(
            nlp, maxDialogue, minDialogue, subsWord, minSorted, maxSorted
        )

    return (
        maxSimilarity >= PASSING_SIMILARITY_SCORE,
        maxSimilarity,
        maxIndex,
    )


def addToMatchingUniqueWords(
    matchingUniqueWords, takenScript, subsWord, subsValue, scriptValue
):
    for part in takenScript.items():
        sceneNumber = part[1]["scene"]
        if (
            sceneNumber not in matchingUniqueWords
            or subsWord not in matchingUniqueWords[sceneNumber]
        ):
            matchingUniqueWords.setdefault(sceneNumber, {})
            matchingUniqueWords[sceneNumber][subsWord] = [
                {
                    "timestamp": subsValue["content"][part[1]["subs"]]["timestamp"],
                    "index": scriptValue[sceneNumber]["content"][part[0]]["index"],
                    "sceneNumber": sceneNumber,
                    "subsDialogue": subsValue["content"][part[1]["subs"]]["dialogue"],
                }
            ]
        else:
            matchingUniqueWords[sceneNumber][subsWord].append(
                {
                    "timestamp": subsValue["content"][part[1]["subs"]]["timestamp"],
                    "index": scriptValue[sceneNumber]["content"][part[0]]["index"],
                    "scene": sceneNumber,
                    "subsDialogue": subsValue["content"][part[1]["subs"]]["dialogue"],
                }
            )
    return matchingUniqueWords


def getMatchingDistinctWords(
    nlp, scriptUnique, subsUnique, script, subs, previousMatches
):
    """
    - traverses subsUnique and scriptUnique until there's a matching unique word.
    - if similar enough, push to matchUniqueWords
    - else, remove
    """
    matchingUniqueWords = previousMatches

    indicesMatched = {}

    for subsWord, subsValue in subsUnique.items():
        for scriptWord, scriptValue in scriptUnique.items():
            if subsWord == scriptWord:
                print("---")
                takenScript = {}
                takenSubs = {}

                for sceneNumber, scriptInstances in scriptValue.items():
                    for scriptIndex, scriptContent in enumerate(
                        scriptInstances["content"]
                    ):
                        if scriptContent["index"] in indicesMatched:
                            continue

                        for subsIndex, subsContent in enumerate(subsValue["content"]):
                            # TODO: parentheticals shouldn't be ignored, or don't forget to seperate sentences
                            (goodEnough, maxSimilarity, maxIndex) = isGoodEnough(
                                nlp, scriptContent, subsContent, subsWord, subs, script,
                            )
                            if goodEnough:
                                indicesMatched[scriptContent["index"]] = True

                            # if match already made for current subtitle OR current script, then
                            # don't bother considering current script<->subtitle match
                            existingTakenSubsBetter = (
                                subsIndex in takenSubs
                                and takenSubs[subsIndex]["similarity"] >= maxSimilarity
                            )

                            existingTakenScriptsFromSubsBetter = (
                                subsIndex in takenSubs
                                and (
                                    takenScript[takenSubs[subsIndex]["script"]][
                                        "similarity"
                                    ]
                                    >= maxSimilarity
                                )
                            )

                            existingTakenScriptsBetter = (
                                scriptIndex in takenScript
                                and takenScript[scriptIndex]["similarity"]
                                >= maxSimilarity
                            )

                            existingTakenSubsFromScriptsBetter = (
                                scriptIndex in takenScript
                                and (
                                    takenSubs[takenScript[scriptIndex]["subs"]][
                                        "similarity"
                                    ]
                                    >= maxSimilarity
                                )
                            )

                            if (
                                existingTakenSubsBetter
                                and existingTakenScriptsFromSubsBetter
                            ):
                                continue

                            if (
                                existingTakenScriptsBetter
                                and existingTakenSubsFromScriptsBetter
                            ):
                                continue

                            if (
                                scriptIndex in takenScript
                                and not existingTakenSubsFromScriptsBetter
                            ):
                                del takenSubs[takenScript[scriptIndex]["subs"]]
                                del takenScript[scriptIndex]

                            if (
                                subsIndex in takenSubs
                                and not existingTakenScriptsFromSubsBetter
                            ):
                                del takenScript[takenSubs[subsIndex]["script"]]
                                del takenSubs[subsIndex]

                            if goodEnough:
                                takenSubs[subsIndex] = {
                                    "similarity": maxSimilarity,
                                    "script": scriptIndex,
                                }
                                takenScript[scriptIndex] = {
                                    "similarity": maxSimilarity,
                                    "subs": subsIndex,
                                    "scene": sceneNumber,
                                }

                matchingUniqueWords = addToMatchingUniqueWords(
                    matchingUniqueWords, takenScript, subsWord, subsValue, scriptValue,
                )

    return matchingUniqueWords
