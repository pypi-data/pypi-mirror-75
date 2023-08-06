import re

from num2words import num2words
from unidecode import unidecode


def convertNumToWords(newContent):
    m = re.finditer(r"(\d+)", newContent)
    for _, num in enumerate(m):
        section = num.groups()[0]
        number = num2words(section)
        if num.start() > 0 and newContent[num.start() - 1] == "$":
            number += " dollars"
            newContent = newContent.replace("$", "")
        newContent = newContent.replace(section, number)
    return newContent


def formatSubs(nlp, subtitles):
    formattedSubtitles = []
    hasPunctuationAtEnd = True
    hasEllipsesAtEnd = False
    for subtitle in subtitles:
        newContent = subtitle.content
        newContent = convertNumToWords(newContent)
        newContent = newContent.encode("ascii", "ignore").decode()
        newContent = unidecode(newContent)

        TAG_RE = re.compile(r"([a-zA-Z]+:\n?)?<[^>]+>")
        newContent = TAG_RE.sub("", newContent.lower())

        if newContent == "":
            continue

        if ("[" in newContent[0] or "[" in newContent[1]) and "]" in newContent[-1]:
            continue

        newContent = re.sub(r"[\[].*?[\]]", "", newContent).strip()
        newContent = newContent[2:] if "--" == newContent[0:2] else newContent
        newContent = newContent.replace(" --", ".")
        newContent = newContent.replace("--", ".")

        if "-" not in newContent[0] and "\n-" not in newContent:
            newContent = newContent.replace("\n", " ")

        # hasPunctuationBeforeLine = (
        #     any(newContent[newContent.index("\n") - 1] == x for x in [".", "!", "?"])
        #     if "\n" in newContent
        #     else False
        # )

        if not hasPunctuationAtEnd:
            formattedSubtitles[-1]["content"] += " " + newContent.replace("...", "")
            formattedSubtitles[-1]["end"] = subtitle.end
        else:
            if hasEllipsesAtEnd:
                if newContent[0:3] == "...":
                    newContent = newContent.replace(
                        "...", formattedSubtitles[-1]["content"] + " "
                    )
                else:
                    newContent = formattedSubtitles[-1]["content"] + " " + newContent

            if "-" in newContent[0]:
                newContent = newContent[1:]
            if "\n-" in newContent:
                newContent = newContent.replace("\n-", " ")
            if "\n" in newContent:
                newContent = newContent.replace("\n", " ")

            newContent = re.sub(" \s+", " ", newContent)
            doc = nlp(newContent)
            sentences = [sent.string.strip() for sent in doc.sents]

            for sentence in sentences:
                if hasEllipsesAtEnd:
                    formattedSubtitles[-1]["content"] = newContent
                else:
                    formattedSubtitles.append(
                        {
                            "content": sentence.replace("...", ""),
                            "start": subtitle.start,
                            "end": subtitle.end,
                            "index": subtitle.index,
                        }
                    )
        hasPunctuationAtEnd = any(
            newContent[-1] == x for x in [".", "!", "?", '"', "♪"]
        )
        hasEllipsesAtEnd = newContent[-3:] == "..."

    return formattedSubtitles


def formatScript(nlp, script):
    newScript = []

    for pageIndex, page in enumerate(script):
        for sceneIndex, content in enumerate(page["content"]):
            if "scene_info" in content and content["scene_info"] != None:
                for sectionIndex, scene in enumerate(content["scene"]):
                    if scene["type"] == "CHARACTER" or scene["type"] == "DUAL_DIALOGUE":
                        dialogues = ""

                        filterParentheticals = lambda dialogueList: list(
                            map(
                                lambda y: y.strip(),
                                filter(lambda x: "(" != x[0], dialogueList),
                            )
                        )

                        def decoupleDialogue(dialogueList):
                            dialogue = " ".join(filterParentheticals(dialogueList))
                            return dialogue

                        if scene["type"] == "CHARACTER":
                            dialogues = decoupleDialogue(scene["content"]["dialogue"])
                        else:
                            dialogues = decoupleDialogue(
                                scene["content"]["character1"]["dialogue"]
                            )
                            dialogues += " " + decoupleDialogue(
                                scene["content"]["character2"]["dialogue"]
                            )

                        # remove interrupt(ed) dialogues "--"
                        if "--" == dialogues[0:2]:
                            dialogues = dialogues[2:]
                        if "--" == dialogues[-2:]:
                            dialogues = dialogues[0:-2] + "."
                        dialogues = convertNumToWords(dialogues)
                        dialogues = dialogues.encode("ascii", "ignore").decode()
                        dialogues = unidecode(dialogues)

                        doc = nlp(dialogues)
                        sentences = [sent.text.strip() for sent in doc.sents]
                        for sentence in sentences:
                            newScript.append(
                                {
                                    "dialogue": sentence.strip().lower(),
                                    "index": {
                                        "page": pageIndex,
                                        "scene": sceneIndex,
                                        "section": sectionIndex,
                                    },
                                    "sceneNumber": content["scene_number"],
                                }
                            )
    return newScript
