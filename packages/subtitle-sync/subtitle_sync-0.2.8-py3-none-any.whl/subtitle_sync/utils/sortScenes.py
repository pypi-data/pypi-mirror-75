import heapq


def sortScenes(pureScript):
    heap_elts = []
    for item in pureScript:
        if "timestamp" in item:
            alreadyExists = False
            for stuff in heap_elts:
                if stuff[0] == item["timestamp"][0]:
                    alreadyExists = True
                    break
            if not alreadyExists:
                heapq.heappush(heap_elts, (item["timestamp"][0], item))

    prevTime = -99
    for el in heap_elts:
        if prevTime > el[0]:
            print("previous > current:")
            print(el)
            print("---")
        prevTime = el[0]

    prevTime = -99
    # for el in heap_elts:
    #     if el[1]["sceneNumber"] - prevTime > 1:
    #         print("skipped scene:")
    #         print(el)
    #         print("---")
    #     prevTime = el[1]["sceneNumber"]

    heap_elts = list(map(lambda x: x[1], heap_elts))

    order = 0
    for el in heap_elts:
        el["sceneOrder"] = order
        order += 1

    return heap_elts
