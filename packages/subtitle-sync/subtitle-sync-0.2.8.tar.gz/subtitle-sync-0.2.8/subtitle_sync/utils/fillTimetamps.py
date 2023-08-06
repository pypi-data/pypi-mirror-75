import copy
import math

# final is the number of divisions of the scene. when curr == final, scene is finished
def getScenesToBeTagged(scriptWithTimestamp):
    scenesToBeTagged = {}

    for page in scriptWithTimestamp:
        for content in page["content"]:
            if "scene_info" in content:
                scenesToBeTagged[content["scene_number"]] = True
    return scenesToBeTagged


def isCountCondition(scene):
    return scene["type"] != "ACTION" or (
        len(scene["content"]) > 1
        or (
            len(scene["content"]) == 1
            and "CONTINUED" not in scene["content"][0]["text"]
        )
    )


def isTransition(scene):
    return scene["type"] == "TRANSITION" and "CONTINUED" not in scene["content"]["text"]


# get the next scene after current scene
# TODO: last case, potentially miss one scene
def getNextScene(scriptWithTimestamp, currTagScenes, latestTimestamp):
    currSceneIsMin = False
    minSceneGroup = None
    minSettings = {"index": [], "timestamp": None, "scene_number": 0}
    currSettings = {"index": [0, 0], "scene_number": 0}
    GOOD_ENOUGH_DIFFERENCE = 20
    sceneGroup = []
    sceneHasGoodEnoughDifference = False
    # pagePadding = scriptWithTimestamp[0]["page"]
    pagePadding = 0

    for pageIndex, page in enumerate(scriptWithTimestamp):
        for contentIndex, content in enumerate(page["content"]):
            if (
                "scene_info" in content
                and currTagScenes[content["scene_number"]] == True
            ):
                for _, scene in enumerate(content["scene"]):
                    if currSettings["scene_number"] != content["scene_number"]:
                        if sceneHasGoodEnoughDifference:
                            return (
                                sceneGroup,
                                minSettings,
                                currSettings["index"],
                            )
                        elif currSceneIsMin:
                            minSceneGroup = (
                                copy.copy(sceneGroup),
                                minSettings,
                                currSettings["index"],
                            )
                            currSceneIsMin = False
                        minSettings = {
                            "timestamp": minSettings["timestamp"],
                            "scene_number": content["scene_number"],
                            "index": [pageIndex + pagePadding, contentIndex],
                        }
                        sceneGroup = []
                    if content["scene_number"] == 0:
                        sceneHasGoodEnoughDifference = True
                    elif "timestamp" in scene:
                        if (
                            scene["timestamp"][0] - latestTimestamp[0]
                            <= GOOD_ENOUGH_DIFFERENCE
                        ):
                            if not sceneHasGoodEnoughDifference:
                                minSettings["timestamp"] = scene["timestamp"]
                            sceneHasGoodEnoughDifference = True
                        if (
                            minSettings["timestamp"] is None
                            or scene["timestamp"][0] < minSettings["timestamp"][0]
                        ):
                            minSettings["timestamp"] = scene["timestamp"]
                            currSceneIsMin = True
                    currSettings = {
                        "scene_number": content["scene_number"],
                        "index": [pageIndex + pagePadding, contentIndex],
                    }
                    sceneGroup.append(scene)
    return minSceneGroup


# TODO: normalize timestamp so that the minimum fill in 1, (with exception of 0)
def generateFill(line, lastScene, positionsLength, positions):
    transitionsInBetween = len(list(filter(lambda x: x[1] == "transition", positions)))
    fill = round(line["timestamp"][0] - lastScene["timestamp"][1], 2)
    if fill < 0 and not (
        line["timestamp"][0] == lastScene["timestamp"][0]
        or line["timestamp"][1] == lastScene["timestamp"][1]
    ):
        del line["timestamp"]
    elif fill - transitionsInBetween > 0:
        fill = (
            (round(((fill - transitionsInBetween) / positionsLength) * 2) / 2)
            if len(positions)
            else 0
        )
    return fill


def fillInBetweenSceneLines(currScene, lastScene, positions):
    sceneIndex = 0
    TRANSITION = "transition"
    OTHER = "other"
    lastScene = copy.copy(lastScene)

    while sceneIndex < len(currScene[0]):
        line = currScene[0][sceneIndex]

        # defining fill timespan spread
        # TODO: mingle fill timestamp
        fill = (
            generateFill(line, lastScene, len(positions), positions)
            if "timestamp" in line
            else None
        )
        # at last, fill in timestamps
        if fill != None and fill > 0:
            # if fill < 1, try to mingle e.g. 0,1,0,1 so that react extension have less bugs
            if fill < 1:
                fill = generateFill(
                    line, lastScene, math.ceil(len(positions) / 2), positions
                )
                timestampRef = lastScene["timestamp"][1]
                mingle = True
                for position in positions:
                    if mingle:
                        if position[1] == TRANSITION:
                            position[0]["timestamp"] = [
                                timestampRef,
                                timestampRef,
                            ]
                        elif position[1] == OTHER:
                            position[0]["timestamp"] = [
                                timestampRef,
                                round(timestampRef + fill, 2),
                            ]
                            timestampRef = round(timestampRef + fill, 2)
                        mingle = False
                    else:
                        position[0]["timestamp"] = [
                            timestampRef,
                            timestampRef,
                        ]
                        mingle = True
                positions = []
                lastScene = {
                    "scene_number": currScene[1]["scene_number"],
                    "timestamp": line["timestamp"],
                    "scene": currScene[0],
                }
            if True:
                # at last,fill in timestamps
                timestampRef = lastScene["timestamp"][1]
                for position in positions:
                    if position[1] == TRANSITION:
                        position[0]["timestamp"] = [
                            timestampRef,
                            timestampRef + 0.5,
                        ]
                        timestampRef += 0.5
                    elif position[1] == OTHER:
                        position[0]["timestamp"] = [
                            timestampRef,
                            round(timestampRef + fill, 2),
                        ]
                        timestampRef = round(timestampRef + fill, 2)

                positions = []
                lastScene = {
                    "scene_number": currScene[1]["scene_number"],
                    "timestamp": line["timestamp"],
                    "scene": currScene[0],
                }
        elif isTransition(line):
            positions.append((line, TRANSITION))
        elif isCountCondition(line):
            positions.append((line, OTHER))
        sceneIndex += 1

    return (lastScene, positions)


def getPureScene(scriptWithTimestamp, sceneNumber):
    lines = []
    scenes = []
    firstPageIndex = None
    firstContentIndex = None

    for pageIndex, page in enumerate(scriptWithTimestamp):
        for contentIndex, content in enumerate(page["content"]):
            if "scene_info" in content and content["scene_number"] == sceneNumber:
                for _, scene in enumerate(content["scene"]):
                    if "timestamp" in scene:
                        return []
                    firstPageIndex = pageIndex
                    firstContentIndex = contentIndex
                    lines.append((scene, "other"))

    scenes.append(
        {
            "scene": lines,
            "index": [firstPageIndex, firstContentIndex],
            "scene_number": sceneNumber,
        }
    )
    return scenes


def getInBetweenScenes(scriptWithTimestamp, currTagScenes, prevScene, currentScene):
    if len(prevScene) == 0:
        return []
    currSceneInBetween = prevScene[1]["scene_number"] + 1
    inBetweenScenes = []
    while currSceneInBetween < currentScene[1]["scene_number"]:
        pureScene = getPureScene(scriptWithTimestamp, currSceneInBetween)
        if len(pureScene) and currTagScenes[currSceneInBetween] == True:
            inBetweenScenes += pureScene
        else:
            break
        currSceneInBetween += 1
    return inBetweenScenes


def fillTimestamps(scriptWithTimestamp):
    positions = []
    currTagScenes = getScenesToBeTagged(scriptWithTimestamp)
    currentScene = getNextScene(scriptWithTimestamp, currTagScenes, [0, 0])
    lastScene = {"scene_number": 0, "timestamp": [0, 0]}
    prevScene = []

    # should increment initial scene right from the start
    currTagScenes[currentScene[1]["scene_number"]] = False

    while currentScene:

        # # if next scene(s) after timestamp scene are empty, then:
        inBetweenScenes = getInBetweenScenes(
            scriptWithTimestamp, currTagScenes, prevScene, currentScene
        )
        totalInBetweenLines = 0
        for content in inBetweenScenes:
            for scene in content["scene"]:
                if scene[0]["type"] != "TRANSITION":
                    totalInBetweenLines += 1

        # # if fill between last and curr are big enough to fill empty scenes, fill empties after last
        if (
            lastScene is not None
            and currentScene[1]["timestamp"] is not None
            and currentScene[1]["timestamp"][0] - lastScene["timestamp"][1]
            >= totalInBetweenLines
        ):
            if len(prevScene) > 0 and len(inBetweenScenes):
                scriptWithTimestamp[prevScene[2][0]]["content"][prevScene[2][1]][
                    "next_scene"
                ] = inBetweenScenes[0]["index"]

            for contentIndex, content in enumerate(inBetweenScenes):
                currTagScenes[content["scene_number"]] = False
                for scene in content["scene"]:
                    positions.append(scene)
                if contentIndex + 1 < len(inBetweenScenes):
                    scriptWithTimestamp[content["index"][0]]["content"][
                        content["index"][1]
                    ]["next_scene"] = inBetweenScenes[contentIndex + 1]["index"]
                else:
                    scriptWithTimestamp[content["index"][0]]["content"][
                        content["index"][1]
                    ]["next_scene"] = currentScene[1]["index"]

        # TODO: else, fill to curr right away, skip the inbetweens
        # however, scenes with timestamp also check empty scenes before it
        # so the empties could still be picked up

        # fill timestamps between previous lines till there is a line with timestamps.
        # otherwise keep adding the list of lines to fill later

        (lastScene, positions) = fillInBetweenSceneLines(
            currentScene, lastScene, positions
        )

        # if all scenes have been covered, then quit
        done = True
        for key, val in currTagScenes.items():
            if val == True:
                done = False
                break
        if done:
            break

        prevScene = copy.copy(currentScene)

        # grab next scene
        currentScene = getNextScene(
            scriptWithTimestamp,
            currTagScenes,
            currentScene["timestamp"] if "timestamp" in currentScene else [0, 0],
        )

        if currentScene is None:
            break

        scriptWithTimestamp[prevScene[2][0]]["content"][prevScene[2][1]][
            "next_scene"
        ] = currentScene[1]["index"]

        # increment scene's curr property in currTagScenes
        currTagScenes[currentScene[1]["scene_number"]] = False
    return scriptWithTimestamp
