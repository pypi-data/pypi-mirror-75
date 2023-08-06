import re
import json
import copy

import numpy as np

from subtitle_sync.utils.traverseDialogue import traverseDialogue
from subtitle_sync.utils.extractLemmas import (
    extractLemmaScript,
    extractLemmaSubs,
)
from subtitle_sync.utils.getUniqueWords import getUniqueWordsScript, getUniqueWordsSubs
from subtitle_sync.utils.getMatchingDistinctWords.index import getMatchingDistinctWords
from subtitle_sync.utils.helper import merge
from subtitle_sync.utils.removeTimestampOutlierFromScenes import removeTimestampOutliersFromScenes

def getDistinctWordsTimestampScript(script, matchingDistinct):
    for sceneNumber, sceneContent in matchingDistinct.items():
        for _, matchingWordInstance in sceneContent.items():
            for content in matchingWordInstance:
                if (
                    "timestamp" in script[content["index"]]
                    and max(
                        script[content["index"]]["timestamp"][0],
                        content["timestamp"][0],
                    )
                    - min(
                        script[content["index"]]["timestamp"][1],
                        content["timestamp"][1],
                    )
                    < 20
                ):
                    startTime = min(
                        script[content["index"]]["timestamp"][0],
                        content["timestamp"][0],
                    )
                    endTime = max(
                        script[content["index"]]["timestamp"][1],
                        content["timestamp"][1],
                    )
                    script[content["index"]]["timestamp"] = [startTime, endTime]
                    script[content["index"]]["scene_number"] = sceneNumber
                else:
                    script[content["index"]]["timestamp"] = content["timestamp"]
                    script[content["index"]]["scene_number"] = sceneNumber
                script[content["index"]]["distinct"] = content
    return script


def getDistinctWordsTimestampSubs(subsLemma, subsUnique):
    for subtitle in subsLemma:
        for word in subtitle["lemma"]:
            if word in subsUnique:
                if "distinct" in subtitle:
                    subtitle["distinct"].append(word)
                else:
                    subtitle["distinct"] = [word]
    return subsLemma


def markScriptWithRareWordsTimestamp(nlp, script, subs):
    """
    1. remove stopwords from subtitles, then get unique words from them. same thing for script
    3. get word matches of unique script/sub words. separate matches with count of  1, 2, and 3
    4. tag timestamps of unique words into the script
    """

    subsLemma = extractLemmaSubs(nlp, subs)
    scriptLemma = extractLemmaScript(nlp, script)
    file0 = open("subsLemma.json", "w+")
    json.dump(script, file0, indent=4, ensure_ascii=False)

    subsUnique = getUniqueWordsSubs(subsLemma)
    scriptUnique = getUniqueWordsScript(scriptLemma)

    match1 = getMatchingDistinctWords(
        nlp, scriptUnique[0], subsUnique[0], script, subs, {}
    )
    file0 = open("matchingDistinctOne.json", "w+")
    json.dump(match1, file0, indent=4)
    # file0 = open("matchingDistinctOne.json", "r")
    # match1 = json.load(file0)

    match2 = getMatchingDistinctWords(
        nlp, scriptUnique[1], subsUnique[1], script, subs, {}
    )
    file0 = open("matchingDistinctTwo.json", "w+")
    json.dump(match2, file0, indent=4)
    # file0 = open("matchingDistinctTwo.json", "rb")
    # match2 = json.load(file0)

    match3 = getMatchingDistinctWords(
        nlp, scriptUnique[2], subsUnique[2], script, subs, {}
    )
    file0 = open("matchingDistinctThree.json", "w+")
    json.dump(match3, file0, indent=4)
    # # file0 = open("matchingDistinctThree.json", "rb")
    # # match3 = json.load(file0)

    match4 = getMatchingDistinctWords(
        nlp, scriptUnique[3], subsUnique[3], script, subs, {}
    )
    file0 = open("matchingDistinctFour.json", "w+")
    json.dump(match4, file0, indent=4)
    # # file0 = open("matchingDistinctFour.json", "rb")
    # # match4 = json.load(file0)

    match5 = getMatchingDistinctWords(
        nlp, scriptUnique[4], subsUnique[4], script, subs, {}
    )
    file0 = open("matchingDistinctFive.json", "w+")
    json.dump(match5, file0, indent=4)
    # # file0 = open("matchingDistinctFive.json", "rb")
    # # match5 = json.load(file0)

    matchingDistinct = merge(match1, match2)
    matchingDistinct = merge(matchingDistinct, match3)
    matchingDistinct = merge(matchingDistinct, match4)
    matchingDistinct = merge(matchingDistinct, match5)

    scriptUniqueTimestamp = getDistinctWordsTimestampScript(
        scriptLemma, matchingDistinct
    )

    # print("one:", len(match1))
    # print("two:", len(match2))
    # print("three:", len(match3))
    # print("four:", len(match4))
    # print("five:", len(match5))

    file0 = open("subHelp.json", "w+")
    json.dump(subsUnique, file0, indent=4)

    file0 = open("scriptLemma.json", "w+")
    json.dump(scriptLemma, file0, indent=4)

    file0 = open("scriptHelp.json", "w+")
    json.dump(scriptUnique, file0, indent=4)

    file0 = open("matchingHelp.json", "w+")
    json.dump(matchingDistinct, file0, indent=4)

    file0 = open("test.json", "w+")
    json.dump(scriptUniqueTimestamp, file0, indent=4)

    # file0 = open("test.json", "rb")
    # scriptUniqueTimestamp = json.load(file0)
    scriptUniqueTimestamp = removeTimestampOutliersFromScenes(scriptUniqueTimestamp)
    return (
        script,
        scriptUniqueTimestamp,
    )
