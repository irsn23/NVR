from app import StreamerList, isRoomIdStream, getHTMLList, parsePage, UidList


def printInfoList(info):
    for inf in info:
        print(inf)


if __name__ == "__main__":
    lList = []
    rList = []
    TYPE = "1.1"
    if TYPE == "3":
        for jj in range(len(StreamerList)):
            try:
                isRoomIdStream(StreamerList[jj], lList, rList)
            except:
                print("")
    elif TYPE == "1.1":
        j = 1
        while True:
            # url = ("https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=9"
            #        "&area_id=0&sort_type=sort_type_291&page=") + str(j)
            url = ("https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=5"
                   "&area_id=0&sort_type=sort_type_225&page=")+str(j)
            html = getHTMLList(url)
            if 0 < len(html) < 100:
                break
            else:
                j += 1
            parsePage(html, lList, UidList)
    printInfoList(lList)
