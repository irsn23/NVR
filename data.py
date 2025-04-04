import csv
import sys
import os


class Streamer:
    def __init__(self, name, uid, roomid):
        self.roomid = roomid
        self.name = name
        self.uid = uid


if getattr(sys, 'frozen', False):
    # 如果是打包后的应用程序
    base_path = sys._MEIPASS
else:
    # 如果是直接运行的脚本
    base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

file_path = os.path.join(base_path, 'data.csv')
with open(file_path, 'r', encoding='gbk') as file:
    reader = csv.reader(file)
    rows = list(reader)
    header = rows[0]
    num_columns = len(header)
    StreamerList = []
    NameList = []
    UidList = []
    RoomIdList = []
    for row in rows[1:]:
        if all(row):
            name, uid, roomid = row
            StreamerList.append(Streamer(name, uid, roomid))
            NameList.append(name)
            UidList.append(uid)
            RoomIdList.append(roomid)
