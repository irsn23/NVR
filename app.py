import requests
import re
from data import StreamerList, UidList
import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices,QIcon
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QTableWidgetItem, QTableWidget, QComboBox, QLineEdit,
                             QMainWindow, QPushButton, QVBoxLayout, QWidget, QStyledItemDelegate)
from functools import partial
import datetime

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
        self.upperCorner["type"].addItem("1.1")
        self.upperCorner["type"].addItem("1.2")
        self.upperCorner["type"].addItem("2")
        self.upperCorner["type"].addItem("3")
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
        container = QVBoxLayout()
        button = QPushButton("生成")
        self.button = button
        container.addWidget(button)
        self.generalLayout.addLayout(container)

    def _getParams(self):
        type = self.upperCorner["type"].currentText()
        if type not in ["1.1", "1.2", "2", "3"]:
            type = "2"
        depth = self.upperCorner["depth"].text()
        if len(depth) == 0:
            return type, 50
        elif depth.isdigit():
            idepth = int(depth)
            if idepth > 0:
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
        if self.Type == "3":
            for streamer in self.StreamerList:
                try:
                    isRoomIdStream(streamer, LiveList, ReplayList)
                except:
                    return "ERROR"
        else:
            url1set = [
                "https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=9&area_id=0&sort_type=sort_type_291&page=",
                "https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=5&area_id=0&sort_type=sort_type_225&page="]
            if self.Type == "1.1":
                # 虚拟主播区
                index = [0]
            elif self.Type == "1.2":
                # 电台区
                index = [1]
            else:
                # self.Type == "2":
                index = [0, 1]
            for url1 in [url1set[ind] for ind in index]:
                j = 1
                while True:
                    url = url1 + str(j)
                    html = getHTMLList(url)
                    if 0 < len(html) < 100:
                        break
                    else:
                        j += 1
                    parsePage(html, LiveList, UidList)


class NVRCore:
    def __init__(self, view):
        self._view = view
        self._connectButtonAndSlots()

    def DisplayTable(self, button):
        type, depth = self._view._getParams()
        if hasattr(self, '_core'):
            core = self._core
            core.setType(type)
            core.setDepth(depth)
        else:
            self._core = NVREvaluate(StreamerList, type, depth)
            core = self._core
        lList1 = []
        rList = []
        core.generateInfoList(lList1, rList)
        lList = []
        for ll in lList1:
            if ll not in lList:
                lList.append(ll)
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
        button.setText("于 "+datetime.datetime.now().time().strftime("%H:%M:%S")+" 生成完成，点击可以进行下一次生成")

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


def getElementSingle(streamer, type):
    if type == "uid":
        return streamer.uid
    elif type == "roomid":
        return streamer.roomid


def getElementArray(streamer, type):
    list = [getElementSingle(streamer[i], type) for i in range(len(streamer))]
    return list


def parsePage(html, info_list, uid_list):
    try:
        name = re.findall(r'\"uname\":\".*?\"', html)
        title = re.findall(r'\"title\":\".*?\"', html)
        uid = re.findall(r'\"uid\":\d*', html)
        roomid = re.findall(r'\"roomid\":\d*', html)
        for i in range(len(name)):
            uid_str = eval(uid[i].split(':')[1])
            if uid_str in uid_list:
                name_str = eval(name[i].split(':')[1])
                title_str = eval(title[i].split(':')[1])
                roomid_str = eval(roomid[i].split(':')[1])
                info_list.append([name_str, title_str, uid_str, roomid_str])
    except:
        print("")


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


if __name__ == "__main__":
    nvrApp = QApplication([])
    nvrWindow = NVRWindow()
    nvrWindow.show()
    NVRCore(nvrWindow)
    sys.exit(nvrApp.exec())
