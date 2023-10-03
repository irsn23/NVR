import requests
import re
from data import StreamerList,UidList
import sys

kv = {'user-agent': 'Mozilla/5.0'}

from PyQt6.QtCore import Qt,QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (QApplication, QHBoxLayout,QGridLayout,QTableWidgetItem,QTableWidget,QComboBox,QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget,QLabel,QStyledItemDelegate)
from functools import partial
class NVRWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NVR")
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
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
        if type not in ["1.1","1.2","2","3"]:
            type = "1.1"
        depth = self.upperCorner["depth"].text()
        if len(depth) == 0:
            return type, 50
        elif depth.isdigit():
            idepth = int(depth)
            if idepth > 0:
                return "","DEPTH should be positive integer"
            else:
                return type, idepth
        else:
            return "","DEPTH should be a positive integer."

class HyperlinkDelegate(QStyledItemDelegate):
    def editorEvent(self, event, model, option, index):
        if event.type() == event.Type.MouseButtonRelease: # and event.button() == Qt.MouseButton.LeftButton
            url = index.data(Qt.ItemDataRole.DisplayRole)
            if url.startswith("http://") or url.startswith("https://"):
                QDesktopServices.openUrl(QUrl(url))
                return True
        return super().editorEvent(event,model,option,index)


class NVREvaluate:
    def __init__(self,StreamerList,Type,Depth):
        self.StreamerList = StreamerList
        self.Type = Type
        self.Depth = Depth
    def setStreamerList(self,index):
        self.StreamerList = StreamerList[index]

    def setType(self,Type):
        self.Type = Type

    def setDepth(self,Depth):
        self.Depth = Depth
    def generateInfoList(self,LiveList,ReplayList):
        if self.Type == "3":
            for streamer in self.StreamerList:
                try:
                    isRoomIdStream(streamer, LiveList, ReplayList)
                except:
                    return "ERROR"
        else:
            url1set = ["https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=9&area_id=0&sort_type=sort_type_291&page=","https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=5&area_id=0&sort_type=sort_type_225&page="]
            if self.Type == "1.1":
                # 虚拟主播区
                index = [0]
            elif self.Type == "1.2":
                # 电台区
                index = [1]
            else:
                # self.Type == "2":
                index = [0,1]
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
    def DisplayTable(self,button):
        if hasattr(self,'_core'):
            core = self._core
        else:
            type,depth = self._view._getParams()
            self._core = NVREvaluate(StreamerList,type,depth)
            core = self._core
            print(depth)
        lList = []
        rList = []
        core.generateInfoList(lList,rList)
        lList = list(set(lList))
        if len(lList) != 0:
            table = self._view.table
            table.clearContents()
            table.setColumnCount(5)
            hyperlink_delagate = HyperlinkDelegate(table)
            table.setItemDelegateForColumn(4,hyperlink_delagate)
            table.setRowCount(len(lList))
            table.setHorizontalHeaderLabels(["名字","标题","UID","直播间号","直播间地址"])
            hyperlink = "https://live.bilibili.com/"
            for row in range(len(lList)):
                for col in range(4):
                    item = QTableWidgetItem(str(lList[row][col]))
                    item.setFlags(item.flags() and ~Qt.ItemFlag.ItemIsEditable)
                    table.setItem(row,col,item)
                table.setItem(row,4,QTableWidgetItem(hyperlink+str(lList[row][3])))
        button.setText("生成完成，点击可以进行下一次生成")

    def _test(self,p=1):
        p = 2
        print(p)
    def _connectButtonAndSlots(self):
        self._view.button.clicked.connect(partial(self.DisplayTable,self._view.button))

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

def whatisthis():
    print(1)

def parsePage(html, info_list, uid_list):
    try:
        name = re.findall(r'\"uname\"\:\".*?\"', html)
        title = re.findall(r'\"title\"\:\".*?\"', html)
        uid = re.findall(r'\"uid\"\:\d*', html)
        roomid = re.findall(r'\"roomid\"\:\d*', html)
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
    islive = re.findall(r'\"live_status\"\:\d*', html)
    islive_str = islive[0][-1]
    if islive_str == "1":
        live_streamer_list.append([streamer.name,"",streamer.uid,streamer.roomid])
    elif islive_str == "2":
        replay_streamer_list.append([streamer.name,"",streamer.uid,streamer.roomid])

def printInfoList(info):
    for inf in info:
        print(inf)

def main():
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
            url = ("https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=9"
                   "&area_id=0&sort_type=sort_type_291&page=") + str(j)
            html = getHTMLList(url)
            if 0 < len(html) < 100:
                break
            else:
                j += 1
            parsePage(html, lList, UidList)
    printInfoList(lList)



ERROR_MSG = "ERROR"
WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40


class PyCalcWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()

        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]
        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)

        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText("")


def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result


class PyCalc:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C"}:
                button.clicked.connect(partial(self._buildExpression, keySymbol))
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)


def main1():
    pycalcApp = QApplication([])
    pycalcWindow = PyCalcWindow()
    pycalcWindow.show()
    PyCalc(model=evaluateExpression, view=pycalcWindow)
    sys.exit(pycalcApp.exec())

def main2():
    nvrApp = QApplication([])
    nvrWindow = NVRWindow()
    nvrWindow.show()
    NVRCore(nvrWindow)
    sys.exit(nvrApp.exec())

# main()
# main()
# main1()
main2()