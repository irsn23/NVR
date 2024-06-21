import requests
import re
from data import StreamerList, UidList
import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QTableWidgetItem, QTableWidget, QComboBox, QLineEdit,
                             QMainWindow, QPushButton, QVBoxLayout, QWidget, QStyledItemDelegate)
from functools import partial


kv = {'user-agent': 'Mozilla/5.0'}


class NVRWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NVR")
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.setWindowIcon(QIcon("NVR.png"))
        self._createDisplay()
        self._createTable()
        self._createButton()

    def _createDisplay(self):
        layout = QHBoxLayout()
        self.upperCorner = {"type": QComboBox(), "depth": QLineEdit()}
        self.upperCorner["type"].addItem("请选择类型")
        self.upperCorner["type"].addItem("1")
        self.upperCorner["type"].addItem("2")
        layout.addWidget(self.upperCorner["type"])
        layout.addWidget(self.upperCorner["depth"])
        self.generalLayout.addLayout(layout)

    def _createTable(self):
        container = QVBoxLayout()
        table = QTableWidget()
        self.table = table
        container.addWidget(table)
        self.generalLayout.addLayout(container)

    def _createButton(self):
        container = QHBoxLayout()
        button = QPushButton("生成")
        self.button = button
        container.addWidget(button)
        self.generalLayout.addLayout(container)

    def _getParams(self):
        type = self.upperCorner["type"].currentText()
        if type not in ["1", "2"]:
            type = "1"
        depth = self.upperCorner["depth"].text()
        if len(depth) == 0:
            return type, 200
        elif depth.isdigit():
            idepth = int(depth)
            if idepth <= 0:
                return "", "DEPTH should be positive integer"
            else:
                return type, idepth
        else:
            return "", "DEPTH should be a positive integer."


class HyperlinkDelegate(QStyledItemDelegate):
    def editorEvent(self, event, model, option, index):
        if event.type() == event.Type.MouseButtonRelease:  # and event.button() == Qt.MouseButton.LeftButton
            url = index.data(Qt.ItemDataRole.DisplayRole)
            if url.startswith("http://") or url.startswith("https://"):
                QDesktopServices.openUrl(QUrl(url))
                return True
        return super().editorEvent(event, model, option, index)


import asyncio


class NVREvaluate:
    def __init__(self, StreamerList, Type, Depth):
        self.StreamerList = StreamerList
        self.Type = Type
        self.Depth = Depth

    def setStreamerList(self, index):
        self.StreamerList = StreamerList[index]

    def setType(self, Type):
        self.Type = Type

    def setDepth(self, Depth):
        self.Depth = Depth

    def generateInfoList(self, LiveList, ReplayList):
        if self.Type == "2":
            for streamer in self.StreamerList:
                try:
                    isRoomIdStream(streamer, LiveList, ReplayList)
                except:
                    return "ERROR"
        else:
            HTMLList = generateHTMLList([5, 9], self.Depth)
            asyncio.run(parseList(LiveList, HTMLList))


async def parseURL(url, LiveList):
    html = getHTMLList(url)
    if 0 < len(html) < 100:
        return None
    parsePage(html, LiveList, UidList)


def generateHTMLList(areaList, depth):
    list = ["bilibili"]
    for i in areaList:
        for j in range(1, depth + 1):
            list.append(
                f'https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id={i}&area_id=0&sort_type=sort_type_291&page={j}')
    return list


class NVRCore:
    def __init__(self, view):
        self._view = view
        self._connectButtonAndSlots()

    def DisplayTable(self, button):
        if hasattr(self, '_core'):
            core = self._core
        else:
            type, depth = self._view._getParams()
            self._core = NVREvaluate(StreamerList, type, depth)
            core = self._core
        lList1 = []
        rList = []
        core.generateInfoList(lList1, rList)
        lList = []
        for ll in lList1:
            if ll not in lList:
                lList.append(ll)
        if len(lList) != 0:
            table = self._view.table
            table.clearContents()
            table.setColumnCount(5)
            hyperlink_delagate = HyperlinkDelegate(table)
            table.setItemDelegateForColumn(4, hyperlink_delagate)
            table.setRowCount(len(lList))
            table.setHorizontalHeaderLabels(["名字", "标题", "UID", "直播间号", "直播间地址"])
            hyperlink = "https://live.bilibili.com/"
            for row in range(len(lList)):
                for col in range(4):
                    item = QTableWidgetItem(str(lList[row][col]))
                    item.setFlags(item.flags() and ~Qt.ItemFlag.ItemIsEditable)
                    table.setItem(row, col, item)
                table.setItem(row, 4, QTableWidgetItem(hyperlink + str(lList[row][3])))
        button.setText("生成完成，点击可以进行下一次生成")

    def _connectButtonAndSlots(self):
        self._view.button.clicked.connect(partial(self.DisplayTable, self._view.button))

        # self._view.upperCorner["button"].clicked.connect(partial(self.DisplayTable))


def getHTMLList(url):
    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text.split("\"list\"")[1]
    except:
        Exception("ERROR1")
        return ""


def parsePage(html, info_list, uid_list):
    try:
        name = re.findall(r'\"uname\":\".*?\"', html)
        title = re.findall(r'\"title\":\".*?\"', html)
        uid = re.findall(r'\"uid\":\d*', html)
        roomid = re.findall(r'\"roomid\":\d*', html)
        for i in range(len(name)):
            uid_str = uid[i].split(':')[1]
            if uid_str in uid_list:
                name_str = eval(name[i].split(':')[1])
                title_str = eval(title[i].split(':')[1])
                roomid_str = eval(roomid[i].split(':')[1])
                info_list.append([name_str, title_str, uid_str, roomid_str])
    except:
        return None


def isRoomIdStream(streamer, live_streamer_list, replay_streamer_list):
    url = "https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo?room_id=" + str(
        streamer.roomid) + "&protocol=0,1&format=0,1,2&codec=0,1&qn=0&platform=web&ptype=8&dolby=5&panorama=1"
    html = getHTMLList(url)
    islive = re.findall(r'\"live_status\":\d*', html)
    islive_str = islive[0][-1]
    if islive_str == "1":
        live_streamer_list.append([streamer.name, "", streamer.uid, streamer.roomid])
    elif islive_str == "2":
        replay_streamer_list.append([streamer.name, "", streamer.uid, streamer.roomid])


class Crawler:
    def __init__(self, client, urls, uidlist, lList, workers=10, limit=25, delay=0.1):
        self.client = client
        self.UidList = uidlist
        self.delay = delay

        self.start_urls = set(urls)
        self.todo = asyncio.Queue()
        self.seen = set()
        self.done = set()

        self.num_workers = workers
        self.limit = limit
        self.total = 0

        self.infoList = lList

    async def run(self):
        await self.on_found_links(self.start_urls)
        workers = [asyncio.create_task(self.worker()) for _ in range(self.num_workers)]
        await self.todo.join()
        for worker in workers:
            worker.cancel()

    async def worker(self):
        while True:
            try:
                await self.process_one()
            except asyncio.CancelledError:
                return

    async def process_one(self):
        url = await self.todo.get()
        try:
            await self.crawl(url)
        except Exception as exc:
            pass
        finally:
            self.todo.task_done()

    async def crawl(self, url):
        await asyncio.sleep(self.delay)
        response = await self.client.get(url, headers=kv)
        text = response.text
        parseText(text, self.UidList, self.infoList)
        self.done.add(url)
        await self.on_found_links(url)
        self.done.add(url)

    async def on_found_links(self, urls):
        new = urls - self.seen
        self.seen.update(new)

        for url in new:
            await self.put_todo(url)

    async def put_todo(self, url):
        if self.total >= self.limit:
            return
        self.total += 1
        await self.todo.put(url)


def parseText(text, uid_list, info_list):
    html = text.split("\"list\"")[1]
    if 0 < len(html) < 100:
        return
    name = re.findall(r'\"uname\":\".*?\"', html)
    title = re.findall(r'\"title\":\".*?\"', html)
    uid = re.findall(r'\"uid\":\d*', html)
    roomid = re.findall(r'\"roomid\":\d*', html)
    for i in range(len(name)):
        uid_str = uid[i].split(':')[1]
        if uid_str in uid_list:
            name_str = eval(name[i].split(':')[1])
            title_str = eval(title[i].split(':')[1])
            roomid_str = eval(roomid[i].split(':')[1])
            info_list.append([name_str, title_str, uid_str, roomid_str])


import httpx


async def parseList(lList, urls):
    async with httpx.AsyncClient() as client:
        crawler = Crawler(client=client, urls=urls, uidlist=UidList, lList=lList, workers=10, limit=400, delay=0.1)
        await crawler.run()


if __name__ == "__main__":
    nvrApp = QApplication([])
    nvrWindow = NVRWindow()
    nvrWindow.show()
    NVRCore(nvrWindow)
    sys.exit(nvrApp.exec())
