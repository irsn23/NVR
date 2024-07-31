class Streamer:
    def __init__(self, name, uid, roomid):
        self.roomid = roomid
        self.name = name
        self.uid = uid


def getRoomid(List):
    return [si.roomid for si in List]


def getName(List):
    return [si.name for si in List]


def getUid(List):
    return [si.uid for si in List]


def getPrintInfo(List, info):
    print(f'{info}List=[')
    for si in List:
        print(f'"{si}",')
    print("]")


NameList = [
    "艾因Eine",
    "琉绮Ruki",
    "七海Nana7mi",
    "中单光一",
    "一果Ichigo",
    "无理Muri",
    "羽音Hanon",
    "有加plus",
    "喵月nyatsuki",
    "惑姬Waku",
    "弥希Miki",
    "星弥Hoshimi",
    "真绯瑠mahiru",
    "阿萨Aza",
    "八木迪之",
    "度人Tabibito",
    "罗伊_Roi",
    "星也seiya",
    "沙夜_Saya",
    "雪绘Yukie",
    "花留Karu",
    "紫纪Shiki",
    "帕克丝Pax",
    "萨麦尔_Samael",
    "御水Mimoi",
    "千春_Chiharu",
    "卡欧斯_Chaos",
    "清良Kiyora",
    "瑞芙Reve",
    "星宸Sirius",
    "悠亚Yua",
    "勺Shaun",
    "田野柴Tanoshiba",
    "茉里Mari",
    "千幽Chiyuu",
    "伊深Imi",
    "勾檀Mayumi",
    "犬童Kendou",
    "九十九_Tsukumo",
    "蕾米Remi",
    "桃星Tocci",
    "轴伊Joi_Channel",
    "吉吉Kiti",
    "绮楼Qilou",
    "恋诗夜Koxia",
    "库伽Hakuja",
    "未羽Miyu",
    "夜宫Yomiya",
    "瑞娅_Rhea",
    "尤格Yog",
    "克克_Keke",
    "暴食Hunger",
    "友夏Uka",
    "希维Sybil",
    "雾深Girimi",
    "狩砂Karisa",
    "希侑Kiyuu",
    "莱恩Leo",
    "江乱Era",
    "岁己SUI",
    "伊舞Eve",
    "欧珀Opal",
    "栞栞Shiori",
    "哎小呜Awu",
    "初濑Hatsuse",
    "未知夜Michiya",
    "雨纪_Ameki",
    "月沢Garu",
    "入福步Ayumi",
    "弥月Mizuki",
    "离枝Richi",
    "库拉乌Kurau",
    "蜜言Mikoto",
    "漆羽Urushiha",
    "晴一Hajime",
    "帕可Pako",
    "米汀Nagisa",
    "向阳Hihi",
    "雪烛Yukisyo",
    "阿命Inochi",
    "鬼间Kima",
    "花礼Harei",
    "点酥Susu",
    "桃代Momoka",
    "樱樱火Official",
    "菜菜子Nanako",
    "祖娅纳惜",
    "幽乐咩Ureme",
    "安堂いなり_official",
    "蜜球兔",
    "阿梓从小就很可爱",
    "小可学妹",
    "鹤森Mori",
    "宫园凛RinMiyazono",
    "舒三妈Susam",
    "糯依Noi",
    "诺莺Nox",
]

UidList = [
    "421267475",
    "420049427",
    "434334701",
    "434401868",
    "434341786",
    "455916618",
    "455965041",
    "472845978",
    "472821519",
    "472877684",
    "477317922",
    "477342747",
    "477306079",
    "480680646",
    "480675481",
    "474369808",
    "480745939",
    "319870877",
    "490331391",
    "56748733",
    "370687588",
    "370687372",
    "370688671",
    "370689210",
    "370689338",
    "558070433",
    "628292881",
    "558070436",
    "666726802",
    "666726800",
    "666726799",
    "666726801",
    "690608706",
    "690608686",
    "690608691",
    "690608694",
    "690608693",
    "690608701",
    "690608702",
    "690608687",
    "690608704",
    "61639371",
    "690608688",
    "690608696",
    "690608690",
    "690608695",
    "690608692",
    "690608689",
    "690608698",
    "690608709",
    "690608711",
    "690608710",
    "690608712",
    "1405589619",
    "1484169431",
    "690608714",
    "1155425566",
    "1116072703",
    "1739085910",
    "1954091502",
    "1542516095",
    "1827139579",
    "1609526545",
    "1567394869",
    "1711724633",
    "1296515170",
    "1932862336",
    "1944489788",
    "1297910179",
    "1789460279",
    "2080519347",
    "1466298310",
    "1609795310",
    "2057377595",
    "1616183604",
    "1978590132",
    "2124647716",
    "1694351351",
    "2039332008",
    "1526446007",
    "1570525137",
    "1048135385",
    "1323355750",
    "2040984069",
    "425642",
    "595407557",
    "3046429",
    "1481781085",
    "392505232",
    "1750561",
    "7706705",
    "14387072",
    "558070435",
    "12485637",
    "6853766",
    "176836079",
    "529249",
]

RoomidList = [
    "21403601",
    "21403609",
    "21452505",
    "21457197",
    "21571739",
    "21571739",
    "21669084",
    "21613353",
    "21615277",
    "21613356",
    "21672023",
    "21672022",
    "21672024",
    "21696950",
    "21696929",
    "21696957",
    "21696953",
    "21763337",
    "21763344",
    "21756924",
    "22111428",
    "22111414",
    "22111450",
    "22111450",
    "22389314",
    "22389319",
    "22389314",
    "22389323",
    "22470204",
    "22470210",
    "22470216",
    "22470208",
    "22605469",
    "22605463",
    "22605464",
    "22605466",
    "22778610",
    "22778617",
    "22778627",
    "22778596",
    "23017349",
    "21484828",
    "23017343",
    "23017349",
    "23260932",
    "23260979",
    "23260965",
    "23260856",
    "23260993",
    "23550749",
    "23550784",
    "23550773",
    "23550793",
    "23805059",
    "23805029",
    "23805078",
    "23805066",
    "25788858",
    "25788830",
    "25788785",
    "26966452",
    "25762103",
    "26966466",
    "27627985",
    "27628009",
    "27628030",
    "27628019",
    "30655185",
    "30655179",
    "30655190",
    "30655172",
    "30655205",
    "30655198",
    "30655213",
    "30655203",
    "31368686",
    "31368705",
    "31368680",
    "31368697",
    "32638818",
    "32638817",
    "1820703922",
    "1766907940",
    "1766909591",
    "11367",
    "22359795",
    "938957",
    "24102587",
    "21224291",
    "8721033",
    "510",
    "605",
    "22459095",
    "784734",
    "3032130",
    "6068126",
    "282208",
]

StreamerList = [Streamer("艾因Eine", 421267475, 21403601),
                Streamer("琉绮Ruki", 420049427, 21403609),
                Streamer("七海Nana7mi", 434334701, 21452505),
                Streamer("中单光一", 434401868, 21457197),
                Streamer("一果Ichigo", 434341786, 21571739),
                Streamer("无理Muri", 455916618, 21571739),
                Streamer("羽音Hanon", 455965041, 21669084),
                Streamer("有加plus", 472845978, 21613353),
                Streamer("喵月nyatsuki", 472821519, 21615277),
                Streamer("惑姬Waku", 472877684, 21613356),
                Streamer("弥希Miki", 477317922, 21672023),
                Streamer("星弥Hoshimi", 477342747, 21672022),
                Streamer("真绯瑠mahiru", 477306079, 21672024),
                Streamer("阿萨Aza", 480680646, 21696950),
                Streamer("八木迪之", 480675481, 21696929),
                Streamer("度人Tabibito", 474369808, 21696957),
                Streamer("罗伊_Roi", 480745939, 21696953),
                Streamer("星也seiya", 319870877, 21763337),
                Streamer("沙夜_Saya", 490331391, 21763344),
                Streamer("雪绘Yukie", 56748733, 21756924),
                Streamer("花留Karu", 370687588, 22111428),
                Streamer("紫纪Shiki", 370687372, 22111414),
                Streamer("帕克丝Pax", 370688671, 22111450),
                Streamer("萨麦尔_Samael", 370689210, 22111450),
                Streamer("御水Mimoi", 370689338, 22389314),
                Streamer("千春_Chiharu", 558070433, 22389319),
                Streamer("卡欧斯_Chaos", 628292881, 22389314),
                Streamer("清良Kiyora", 558070436, 22389323),
                Streamer("瑞芙Reve", 666726802, 22470204),
                Streamer("星宸Sirius", 666726800, 22470210),
                Streamer("悠亚Yua", 666726799, 22470216),
                Streamer("勺Shaun", 666726801, 22470208),
                Streamer("田野柴Tanoshiba", 690608706, 22605469),
                Streamer("茉里Mari", 690608686, 22605463),
                Streamer("千幽Chiyuu", 690608691, 22605464),
                Streamer("伊深Imi", 690608694, 22605466),
                Streamer("勾檀Mayumi", 690608693, 22778610),
                Streamer("犬童Kendou", 690608701, 22778617),
                Streamer("九十九_Tsukumo", 690608702, 22778627),
                Streamer("蕾米Remi", 690608687, 22778596),
                Streamer("桃星Tocci", 690608704, 23017349),
                Streamer("轴伊Joi_Channel", 61639371, 21484828),
                Streamer("吉吉Kiti", 690608688, 23017343),
                Streamer("绮楼Qilou", 690608696, 23017349),
                Streamer("恋诗夜Koxia", 690608690, 23260932),
                Streamer("库伽Hakuja", 690608695, 23260979),
                Streamer("未羽Miyu", 690608692, 23260965),
                Streamer("夜宫Yomiya", 690608689, 23260856),
                Streamer("瑞娅_Rhea", 690608698, 23260993),
                Streamer("尤格Yog", 690608709, 23550749),
                Streamer("克克_Keke", 690608711, 23550784),
                Streamer("暴食Hunger", 690608710, 23550773),
                Streamer("友夏Uka", 690608712, 23550793),
                Streamer("希维Sybil", 1405589619, 23805059),
                Streamer("雾深Girimi", 1484169431, 23805029),
                Streamer("狩砂Karisa", 690608714, 23805078),
                Streamer("希侑Kiyuu", 1155425566, 23805066),
                Streamer("莱恩Leo", 1116072703, 25788858),
                Streamer("江乱Era", 1739085910, 25788830),
                Streamer("岁己SUI", 1954091502, 25788785),
                Streamer("伊舞Eve", 1542516095, 26966452),
                Streamer("欧珀Opal", 1827139579, 25762103),
                Streamer("栞栞Shiori", 1609526545, 26966466),
                Streamer("哎小呜Awu", 1567394869, 27627985),
                Streamer("初濑Hatsuse", 1711724633, 27628009),
                Streamer("未知夜Michiya", 1296515170, 27628030),
                Streamer("雨纪_Ameki", 1932862336, 27628019),
                Streamer("月沢Garu", 1944489788, 30655185),
                Streamer("入福步Ayumi", 1297910179, 30655179),
                Streamer("弥月Mizuki", 1789460279, 30655190),
                Streamer("离枝Richi", 2080519347, 30655172),
                Streamer("库拉乌Kurau", 1466298310, 30655205),
                Streamer("蜜言Mikoto", 1609795310, 30655198),
                Streamer("漆羽Urushiha", 2057377595, 30655213),
                Streamer("晴一Hajime", 1616183604, 30655203),
                Streamer("帕可Pako", 1978590132, 31368686),
                Streamer("米汀Nagisa", 2124647716, 31368705),
                Streamer("向阳Hihi", 1694351351, 31368680),
                Streamer("雪烛Yukisyo", 2039332008, 31368697),
                Streamer("阿命Inochi", 1526446007, 32638818),
                Streamer("鬼间Kima", 1570525137, 32638817),
                Streamer("花礼Harei", 1048135385, 1820703922),
                Streamer("点酥Susu", 1323355750, 1766907940),
                Streamer("桃代Momoka", 2040984069, 1766909591),
                Streamer("樱樱火Official", 425642, 11367),
                Streamer("菜菜子Nanako", 595407557, 22359795),
                Streamer("祖娅纳惜", 3046429, 938957),
                Streamer("幽乐咩Ureme", 1481781085, 24102587),
                Streamer("安堂いなり_official", 392505232, 21224291),
                Streamer("蜜球兔", 1750561, 8721033),
                Streamer("阿梓从小就很可爱", 7706705, 510),
                Streamer("小可学妹", 14387072, 605),
                Streamer("鹤森Mori", 558070435, 22459095),
                Streamer("宫园凛RinMiyazono", 12485637, 784734),
                Streamer("舒三妈Susam", 6853766, 3032130),
                Streamer("糯依Noi", 176836079, 6068126),
                Streamer("诺莺Nox", 529249, 282208),
                ]
import datetime

# https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=9&area_id=0&sort_type=sort_type_291&page=1
# https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=9&area_id=0&sort_type=sort_type_291&page=1
if __name__ == "__main__":
    getPrintInfo(getName(StreamerList), "Name")
    getPrintInfo(getUid(StreamerList), "Uid")
    getPrintInfo(getRoomid(StreamerList), "Roomid")
