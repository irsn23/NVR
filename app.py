import requests
import datetime
import sys
from data import UidList
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QTableWidgetItem, QTableWidget,
                             QMainWindow, QPushButton, QVBoxLayout, QWidget, QStyledItemDelegate)

from functools import partial

kv = {'user-agent': 'Mozilla/5.0'}
hyperlink = "https://live.bilibili.com/"


class NVRWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        self.setWindowTitle("NVR")
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.setWindowIcon(QIcon("NVR.png"))
        self._createTable()
        self._createButton()

    def _createTable(self):
        container = QVBoxLayout()
        table = QTableWidget()
        table.setSortingEnabled(True)
        self.table = table

        container.addWidget(table)
        self.generalLayout.addLayout(container)

    def _createButton(self):
        container = QHBoxLayout()
        button = QPushButton("生成")
        self.button = button
        container.addWidget(button)
        self.generalLayout.addLayout(container)


class HyperlinkDelegate(QStyledItemDelegate):
    def editorEvent(self, event, model, option, index):
        if event.type() == event.Type.MouseButtonRelease:  # and event.button() == Qt.MouseButton.LeftButton
            url = index.data(Qt.ItemDataRole.DisplayRole)
            if url.startswith("http://") or url.startswith("https://"):
                QDesktopServices.openUrl(QUrl(url))
                return True
        return super().editorEvent(event, model, option, index)


def TimeFormation(time_difference):
    days = time_difference.days
    total_seconds = time_difference.seconds + days * 24 * 3600

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    formatted_hours = str(hours)
    formatted_minutes = "{:02d}".format(minutes)
    formatted_seconds = "{:02d}".format(seconds)

    return f"{formatted_hours}小时{formatted_minutes}分钟{formatted_seconds}秒"


class NVRCore:
    def __init__(self, view):
        self._view = view
        self._connectButtonAndSlots()
        self._init_data()

    def _init_data(self):
        self._list = []
        self._time = datetime.datetime.now()
        self._success = False

    def _update_ui(self, llist):
        ColumnCount = 4
        ColumnCountM1 = ColumnCount - 1
        table = self._view.table
        table.clearContents()
        table.setColumnCount(ColumnCount)
        hyperlink_delegate = HyperlinkDelegate(table)
        table.setItemDelegateForColumn(ColumnCountM1, hyperlink_delegate)
        table.setRowCount(len(llist))
        table.setHorizontalHeaderLabels(["名字", "标题", "直播时长", "直播间地址"])

        for row in range(len(llist)):
            for col in range(ColumnCountM1):
                item = QTableWidgetItem(str(llist[row][col]))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                table.setItem(row, col, item)
            table.setItem(row, ColumnCountM1, QTableWidgetItem(hyperlink + str(llist[row][ColumnCountM1])))
        table.resizeColumnsToContents()

    def _handle_data_ready(self):
        display_time = self._time.strftime("%H:%M:%S")

        if self._success:
            self._update_ui(self._list)
            self._view.button.setText(f"于 {display_time} 生成完成，点击可以进行下一次生成")
            self._view.button.setEnabled(True)
        else:
            self._view.button.setText(
                f"于 {display_time} 生成失败，错误代码 {self._list}，请检查网络或者点击以进行下一次生成。")
        self._init_data()

    def DisplayTable(self, button):
        button.setText("正在生成数据，请稍候...")
        button.setEnabled(False)
        self._get_data()
        self._handle_data_ready()

    def _get_data(self):
        url = 'https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids'
        params = {
            'uids[]': UidList,
        }
        response = requests.get(url, params=params, headers=kv)
        if response.status_code == 200:
            self._success = True
            current_time = datetime.datetime.now()
            self._time = current_time
            json_data = response.json()['data']
            templist = []
            for uid in UidList:
                if uid in json_data and json_data[uid]['live_status'] == 1:
                    name, title, time, address = [json_data[uid][key] for key in
                                                  ['uname', 'title', 'live_time', 'room_id']]
                    given_time = datetime.datetime.fromtimestamp(time)
                    time_difference = TimeFormation(current_time - given_time)

                    templist.append([name, title, time_difference, address])
            self._list = templist

        else:
            self._list = response.status_code

    def _connectButtonAndSlots(self):
        self._view.button.clicked.connect(partial(self.DisplayTable, self._view.button))


if __name__ == "__main__":
    nvrApp = QApplication([])
    nvrWindow = NVRWindow()
    nvrWindow.show()
    NVRCore(nvrWindow)
    sys.exit(nvrApp.exec())
