import copy


def removeTimestampOutliersFromScenes(script):
    sceneNumber = None
    timestampsRangesClaimed = []
    prevScene = {}
    startTimestampRange = None

    for index, line in enumerate(script):
        if sceneNumber != line["sceneNumber"]:
            endTimestampRange = (
                prevScene["timestamp"][1] if "timestamp" in prevScene else None
            )
            if endTimestampRange and startTimestampRange:
                timestampsRangesClaimed.append([startTimestampRange, endTimestampRange])

            startTimestampRange = None
            sceneNumber = line["sceneNumber"]
            prevScene = {}
            prevSceneIndex = -1
            prevPrevScene = {}
            prevPrevSceneIndex = -1
        if "timestamp" in line:
            if (
                "timestamp" in prevScene
                and line["timestamp"][0] < prevScene["timestamp"][1]
            ):
                # if they're close enough, just swap them
                if (
                    prevScene["timestamp"][0] == line["timestamp"][0]
                    and prevScene["timestamp"][1] == line["timestamp"][1]
                ):
                    mid = round(
                        (prevScene["timestamp"][1] + prevScene["timestamp"][0]) / 2, 2,
                    )
                    prevScene["timestamp"] = [prevScene["timestamp"][0], mid]
                    line["timestamp"] = [
                        mid,
                        line["timestamp"][1],
                    ]
                    prevPrevScene = copy.copy(prevScene)
                    prevPrevSceneIndex = prevSceneIndex
                    prevScene = line
                    prevSceneIndex = index
                elif prevScene["timestamp"][1] - line["timestamp"][0] <= 55:
                    temp = prevScene["timestamp"]
                    prevScene["timestamp"] = line["timestamp"]
                    line["timestamp"] = temp

                    prevPrevScene = copy.copy(prevScene)
                    prevPrevSceneIndex = prevSceneIndex
                    prevScene = line
                    prevSceneIndex = index
                else:
                    if "timestamp" not in prevPrevScene:
                        prevPrevScene = copy.copy(prevScene)
                        prevPrevSceneIndex = prevSceneIndex
                        prevScene = line
                        prevSceneIndex = index

                        # edge case: there's only prevPrevScene and prevScene timestamps
                        # in the ENTIRE scene AND prevprevScene > prevScene
                        if prevPrevScene["timestamp"][1] > prevScene["timestamp"][0]:
                            # delete prevprev or prevscene??? this is pwetty hawd
                            poppedPrev = False
                            poppedPrevPrev = False
                            for range in timestampsRangesClaimed:
                                if (
                                    prevScene["timestamp"][0] >= range[0]
                                    and prevScene["timestamp"][0] < range[1]
                                    and not poppedPrev
                                ):
                                    script.pop(prevSceneIndex)
                                    poppedPrev = True
                                elif (
                                    prevPrevScene["timestamp"][0] >= range[0]
                                    and prevPrevScene["timestamp"][0] < range[1]
                                    and not poppedPrevPrev
                                ):
                                    script.pop(prevPrevSceneIndex)
                                    poppedPrevPrev = True
                            if not poppedPrev and not poppedPrevPrev:
                                if abs(
                                    prevScene["timestamp"][0]
                                    - timestampsRangesClaimed[-1][1]
                                ) < abs(
                                    prevPrevScene["timestamp"][0]
                                    - timestampsRangesClaimed[-1][1]
                                ):
                                    script.pop(prevPrevSceneIndex)
                                else:
                                    script.pop(prevSceneIndex)
                    elif prevPrevScene["timestamp"][1] < line["timestamp"][0]:
                        script.pop(prevSceneIndex)
                        prevScene = line
                        prevSceneIndex = index

                    else:
                        script.pop(index)
            else:
                prevPrevScene = copy.copy(prevScene)
                prevPrevSceneIndex = prevSceneIndex
                prevScene = line
                prevSceneIndex = index

            if startTimestampRange == None and len(prevPrevScene) > 0:
                startTimestampRange = prevPrevScene["timestamp"][0]
    return script
