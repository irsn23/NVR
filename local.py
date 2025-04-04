from app import TimeFormation, UidList, kv, requests, hyperlink
from datetime import datetime

if __name__ == "__main__":
    url = 'https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids'
    params = {
        'uids[]': UidList,
    }
    response = requests.get(url, params=params, headers=kv)
    current_time = datetime.now()
    display_time = current_time.strftime("%H:%M:%S")

    if response.status_code == 200:
        json_data = response.json()['data']
        print(f"\n于 {display_time} 生成完成\n")
        for uid in UidList:
            if uid in json_data and json_data[uid]['live_status'] == 1:
                name, title, time, address = [json_data[uid][key] for key in
                                              ['uname', 'title', 'live_time', 'room_id']]
                given_time = datetime.fromtimestamp(time)
                time_difference = TimeFormation(current_time - given_time)

                print([name, title, time_difference, hyperlink + str(address)])

    else:
        print(f"于 {display_time} 生成失败，错误代码 {response.status_code}，请检查网络或者进行下一次生成。")
