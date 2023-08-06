from __future__ import unicode_literals, print_function
import json
import re
import argparse
import copy

import srt
import spacy
from pysbd.utils import PySBDFactory

from subtitle_sync.formatText import formatSubs, formatScript
from subtitle_sync.markScriptWithRareWordsTimestamp import (
    markScriptWithRareWordsTimestamp,
)
from subtitle_sync.utils.nlpSetup import nlpSetup
from subtitle_sync.utils.furtherSyncScript import furtherSyncScript
from subtitle_sync.utils.traverseDialogue import traverseDialogue
from subtitle_sync.utils.tagTimestampToScript import tagTimestampToScript
from subtitle_sync.utils.fillTimetamps import fillTimestamps
from subtitle_sync.utils.minify import minify
from subtitle_sync.utils.sortScenes import sortScenes


def sync(moviePath, subsPath):
    subtitle = open(subsPath, "r")
    subtitle = list(srt.parse(subtitle.read()))

    script = open(moviePath, "rb")
    script = json.load(script)
    pureScript = copy.copy(script)

    # explicitly adding component to pipeline
    # (recommended - makes it more readable to tell what's going on)
    nlpSentence = spacy.blank("en")
    nlpSentence.add_pipe(PySBDFactory(nlpSentence))
    subtitle = formatSubs(nlpSentence, subtitle)
    script = formatScript(nlpSentence, script)

    # file0 = open("scriptFormat.json", "w+")
    # json.dump(script, file0, indent=4, ensure_ascii=False)
    # file0 = open("scriptFormat.json", "rb")
    # script = json.load(file0)

    nlp = nlpSetup()
    (
        script,
        scriptWithTimestamp,
        # subsWithTimestamp,
    ) = markScriptWithRareWordsTimestamp(nlp, script, subtitle)
    scriptWithTimestamp = sortScenes(scriptWithTimestamp)
    scriptWithTimestamp = tagTimestampToScript(pureScript, scriptWithTimestamp)

    try:
        file0 = open("timestampToFill.json", "w+")
        json.dump(scriptWithTimestamp, file0, indent=4, ensure_ascii=False)
    except:
        file0 = open("timestampToFill.json", "w+")
        json.dump(scriptWithTimestamp, file0, indent=4, ensure_ascii=True)

    # file0 = open("timestampToFill.json", "r")
    # scriptWithTimestamp = json.load(file0)
    pureScript = fillTimestamps(scriptWithTimestamp)
    pureScript = minify(pureScript)

    return pureScript


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Screenplay PDF into JSON")

    parser.add_argument(
        "-m",
        metavar="screenplay",
        type=str,
        help="screenplay json path",
        required=True,
    )

    parser.add_argument(
        "-s", metavar="subs", type=str, help="subtitle json path", required=True,
    )

    # start from skipPage set up by user.  default to 0
    args = parser.parse_args()
    moviePath = args.m
    subsPath = args.s
    scriptWithTimestamp = sync(moviePath, subsPath)
    file0 = open("timestamped.json", "w+", encoding="utf-8")
    json.dump(scriptWithTimestamp, file0, indent=4, ensure_ascii=False)
    file0.close()
