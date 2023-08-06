# split dialogue by whitespace, and remove remaining punctuations
splitDialogue = lambda sentence: sentence.translate(
    str.maketrans(dict.fromkeys(";-", " "))
).split()


def merge(dictToCopy, dictToAdd):
    for sceneNumberDictToAdd, _ in dictToAdd.items():
        if sceneNumberDictToAdd in dictToCopy:
            for wordDictToCopy, wordInstancesDictToCopy in dictToCopy[
                sceneNumberDictToAdd
            ].items():
                if wordDictToCopy in dictToAdd[sceneNumberDictToAdd]:
                    dictToAdd[sceneNumberDictToAdd][
                        wordDictToCopy
                    ] += wordInstancesDictToCopy

                    # indicesAdded = {}
                    # for instances in dictToAdd[sceneNumberDictToAdd][wordDictToCopy]:
                    #     if instances["index"] in indicesAdded:
                    #         del instances
                    #     else:
                    #         indicesAdded[instances["index"]] = True
                else:
                    dictToAdd[sceneNumberDictToAdd][
                        wordDictToCopy
                    ] = wordInstancesDictToCopy

    return {**dictToCopy, **dictToAdd}

