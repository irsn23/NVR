
from app import StreamerList, isRoomIdStream, generateHTMLList, UidList, getHTMLList,parsePage,kv,parseList


def printInfoList(info):
    for inf in info:
        print(inf)

import asyncio

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
    elif TYPE == "1":
        liList = []
        asyncio.run(parseList(liList,generateHTMLList([5, 9], 200)))
        for ji in liList:
            if ji in lList:
                continue
            else:
                lList.append(ji)
        # for area in [5]:
        #     while True:
        #         url = f'https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id={area}&area_id=0&sort_type=sort_type_291&page={j}'
        #         html = getHTMLList(url)
        #         if 0 < len(html) < 100:
        #             break
        #         else:
        #             j += 1
        #         parsePage(html, lList, UidList)

    printInfoList(lList)
