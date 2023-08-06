
def getSimilarity(nlp, subsDialogue, scriptDialogue):
    subtitleNLP = nlp(subsDialogue)
    scriptNLP = nlp(scriptDialogue)
    similarity = subtitleNLP.similarity(scriptNLP)
    return similarity

def getSameLemmaCount(subsLemma, scriptLemma):
    count = 0
    for scriptLemma in scriptLemma:
        for subsLemma in subsLemma:
            count += 1 if subsLemma == scriptLemma else 0
    return count

def getAvgLength(subsDialogue, scriptDialogue):
    avgLength = (
        len(scriptDialogue)
        + len(subsDialogue)
    ) / 2
    return avgLength

def traverseScript(nlp, subtitle, scriptIndex, scriptWithTimestamp):
    traversedDialogue = {}
    currBestSimilarity = {
        "index": scriptIndex,
        "similarity": 0
    } 
    while scriptIndex < len(scriptWithTimestamp) and "timestamp" in scriptWithTimestamp:
        scriptIndex+=1
    while scriptIndex < len(scriptWithTimestamp):
        dialogue = scriptWithTimestamp[scriptIndex]["dialogue"]
        if "timestamp" not in scriptWithTimestamp[scriptIndex] or "modified" in scriptWithTimestamp[scriptIndex]:
            if len(dialogue) == 0 or dialogue in traversedDialogue:
                scriptIndex += 1
                continue

            similarity = getSimilarity(nlp, subtitle["content"].lower(), dialogue.lower())
            count = getSameLemmaCount(subtitle["lemma"], scriptWithTimestamp[scriptIndex]["lemma"])
            avgLength = getAvgLength(subtitle["lemma"], scriptWithTimestamp[scriptIndex]["lemma"])

            if similarity > currBestSimilarity["similarity"] or avgLength - count < 2:
                currBestSimilarity = {
                    "index": scriptIndex,
                    "similarity": similarity
                }
            scriptIndex += 1
        else:
            break

    if currBestSimilarity["similarity"] > 0.9:
        scriptWithTimestamp[currBestSimilarity["index"]]["timestamp"]= [subtitle["start"], subtitle["end"]]
        scriptWithTimestamp[currBestSimilarity["index"]]["TOTBOY"]= subtitle["content"]
        traversedDialogue[currBestSimilarity["index"]] = True

    return scriptIndex

import spacy

def furtherSyncScript(nlp, subsWithTimestamp, scriptWithTimestamp):
    nlp = spacy.load('en_vectors_web_lg')
    subIndex = 0
    scriptIndex = 0
    initialScriptIndex = scriptIndex
    while subIndex < len(subsWithTimestamp):
        dsubtitle = subsWithTimestamp[subIndex]
        if "unique" not in subsWithTimestamp[subIndex]:
            scriptIndex = initialScriptIndex
            scriptIndex = traverseScript(nlp, subsWithTimestamp[subIndex] , scriptIndex, scriptWithTimestamp)
        else:
            initialScriptIndex = scriptIndex
        subIndex += 1
    return scriptWithTimestamp