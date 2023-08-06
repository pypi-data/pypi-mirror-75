# add prevLine and nextLine fields in subHelp and scriptHelp

import heapq


def getUniqueWordsSubs(subsLemma):
    uniqueWords = {}
    for index, subtitle in enumerate(subsLemma):
        if len(subtitle["lemma"]) <= 2:
            continue
        for lemmaWord in subtitle["lemma"]:
            if (
                lemmaWord in uniqueWords
                and "content" in uniqueWords[lemmaWord]
                and len(uniqueWords[lemmaWord]["content"])
                and uniqueWords[lemmaWord]["content"][-1]["dialogue"]
                == subtitle["content"]
            ):
                continue
            uniqueWords.setdefault(
                lemmaWord, {"count": 0, "content": []},
            )
            uniqueWords[lemmaWord]["count"] += 1
            uniqueWords[lemmaWord]["content"].append(
                {
                    "lemma": subtitle["lemma"],
                    "dialogue": subtitle["content"],
                    "timestamp": (subtitle["start"], subtitle["end"]),
                    "index": index,
                }
            )
    subsCountOfOne = {}
    subsCountOfTwo = {}
    subsCountOfThree = {}
    subsCountOfFour = {}
    subsCountOfFive = {}

    for k, v in uniqueWords.items():
        if v["count"] == 1:
            subsCountOfOne[k] = v
        elif v["count"] == 2:
            subsCountOfTwo[k] = v
        elif v["count"] == 3:
            subsCountOfThree[k] = v
        elif v["count"] == 4:
            subsCountOfFour[k] = v
        elif v["count"] == 5:
            subsCountOfFive[k] = v

    return [
        subsCountOfOne,
        subsCountOfTwo,
        subsCountOfThree,
        subsCountOfFour,
        subsCountOfFive,
    ]


def getUniqueWordsScript(scriptLemma):
    uniqueWords = {}
    for index, section in enumerate(scriptLemma):
        if len(section["lemma"]) <= 2:
            continue
        for lemmaWord in section["lemma"]:
            if (
                lemmaWord in uniqueWords
                and "scenes" in uniqueWords[lemmaWord]
                and len(uniqueWords[lemmaWord]["scenes"])
                and section["sceneNumber"] in uniqueWords[lemmaWord]["scenes"]
            ):
                x = filter(
                    lambda y: y["index"] == index,
                    uniqueWords[lemmaWord]["scenes"][section["sceneNumber"]]["content"],
                )
                if len(list(x)):
                    continue
            uniqueWords.setdefault(lemmaWord, {"count": 0, "scenes": {}})
            uniqueWords[lemmaWord]["scenes"].setdefault(
                section["sceneNumber"], {"content": []}
            )
            uniqueWords[lemmaWord]["count"] += 1
            uniqueWords[lemmaWord]["scenes"][section["sceneNumber"]]["content"].append(
                {
                    "lemma": section["lemma"],
                    "dialogue": section["dialogue"],
                    "index": index,
                }
            )

    scriptCountOfOne = {}
    scriptCountOfTwo = {}
    scriptCountOfThree = {}
    scriptCountOfFour = {}
    scriptCountOfFive = {}

    for k, v in uniqueWords.items():
        if v["count"] == 1:
            scriptCountOfOne.setdefault(k, {})
            scriptCountOfOne[k] = v["scenes"]
        elif v["count"] == 2:
            scriptCountOfTwo.setdefault(k, {})
            scriptCountOfTwo[k] = v["scenes"]
        elif v["count"] == 3:
            scriptCountOfThree.setdefault(k, {})
            scriptCountOfThree[k] = v["scenes"]
        elif v["count"] == 4:
            scriptCountOfFour.setdefault(k, {})
            scriptCountOfFour[k] = v["scenes"]
        elif v["count"] == 5:
            scriptCountOfFive.setdefault(k, {})
            scriptCountOfFive[k] = v["scenes"]

    return [
        scriptCountOfOne,
        scriptCountOfTwo,
        scriptCountOfThree,
        scriptCountOfFour,
        scriptCountOfFive,
    ]
