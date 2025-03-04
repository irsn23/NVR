from app import generateHTMLList, AreaId, asyncio, parseList, StreamerList, isRoomIdStream, getHTMLList, parsePage, \
    UidList

areaList = AreaId
Depth = 200


def printInfoList(info):
    for inf in info:
        print(inf)


if __name__ == "__main__":
    LiveList = []
    ReplayList = []
    Type = "并行"
    if Type == "并行":
        HTMLList = generateHTMLList(areaList, Depth)
        asyncio.run(parseList(LiveList, HTMLList))
    elif Type == "穷举":
        for streamer in StreamerList:
            try:
                isRoomIdStream(streamer, LiveList, ReplayList)
            except:
                print("ERROR")
    else:
        HTMLList = generateHTMLList(areaList, Depth)
        for ind in range(len(areaList)):
            j = 0
            while True:
                url = HTMLList[j + ind * Depth]
                html = getHTMLList(url)
                if 0 < len(html) < 100:
                    break
                else:
                    j += 1
                parsePage(html, LiveList, UidList)
    printInfoList(LiveList)
