
def traverseDialogue(script, dialogueFunction):
    for page in script:
        for content in page["content"]:
            if "scene_info" in content:
                for scene in content["scene"]:
                    if scene["type"] == "CHARACTER":
                        scene["content"] = dialogueFunction(scene["content"])
    return script