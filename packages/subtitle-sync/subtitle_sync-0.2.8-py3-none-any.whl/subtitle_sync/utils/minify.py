def minify(script):
    for pageIndex, page in enumerate(script):
        for sceneIndex, content in enumerate(page["content"]):
            if "scene_info" in content:
                for sectionIndex, scene in enumerate(content["scene"]):
                    if "timestamp" in scene:
                        scene["ts"] = scene.pop("timestamp")

                    if scene["type"] == "CHARACTER":
                        scene["content"]["ch"] = scene["content"].pop("character")
                        if "modifier" in scene["content"]:
                            scene["content"]["m"] = scene["content"].pop("modifier")
                        scene["content"]["d"] = scene["content"].pop("dialogue")
                        scene["c"] = scene.pop("content")
                    if scene["type"] == "ACTION":
                        scene["content"] = [x["text"] for x in scene["content"]]
                        scene["c"] = scene.pop("content")
                    if scene["type"] == "DUAL_DIALOGUE":
                        scene["c"] = scene.pop("content")
                    if scene["type"] == "TRANSITION":
                        scene["c"] = scene["content"]["text"]
                        del scene["content"]
                    scene["t"] = scene.pop("type")
                if content["scene_info"] != None:
                    if isinstance(content["scene_info"], str):
                        content["si"] = content["scene_info"]
                    else:
                        content["si"] = {
                            "r": content["scene_info"]["region"],
                            "l": content["scene_info"]["location"],
                            "t": content["scene_info"]["time"],
                        }
                del content["scene_info"]
                content["s"] = content.pop("scene")
                content["sn"] = content.pop("scene_number")
                if "next_scene" in content:
                    content["ns"] = content.pop("next_scene")
        page["c"] = page.pop("content")
        page["pg"] = page.pop("page")
    return script
