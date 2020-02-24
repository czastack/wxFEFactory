from lib.utils import split_value_label


VERSIONS = ('1.0', '1.1')
DIFFICULTY = ('简单', '困难')
DEAN_SONYA_EVENT = ('未击败', '击败索尼娅', '击败迪恩')

ITEMS = {
    0x00: "无",
    0x03: "铁剑",
    0x04: "钢剑",
    0x05: "银剑",
    0x06: "勇者之剑",
    0x07: "黑暗之剑",
    0x08: "雷之剑",
    0x09: "圣剑",
    0x0A: "王族之剑",
    0x0B: "法尔西昂",
    0x0C: "流星",
    0x0D: "黄金短剑",
    0x0E: "双手大剑",
    0x0F: "淑女剑",
    0x10: "墨丘利剑",
    0x11: "索菲亚宝剑",
    0x12: "伊鲁威",
    0x13: "刺剑",
    0xEE: "毒剑",
    0xF7: "七剑",
    0x35: "生锈的剑1",
    0x36: "生锈的剑2",
    0x37: "生锈的剑3",
    0x38: "生锈的剑4",
    0x39: "生锈的剑5",
    0x3A: "生锈的剑6",
    0x15: "铁枪",
    0x16: "钢枪",
    0x17: "银枪",
    0x18: "投枪",
    0x19: "骑士杀手",
    0x1A: "圣枪",
    0x1B: "古拉迪乌斯",
    0x1C: "太阳",
    0x1D: "多玛枪",
    0x1E: "皇帝枪",
    0x1F: "克里姆希尔特",
    0x20: "罗姆菲亚",
    0x21: "撒乌尼昂",
    0xEF: "毒枪",
    0x3B: "生锈的枪1",
    0x3C: "生锈的枪2",
    0x3D: "生锈的枪3",
    0x3E: "生锈的枪4",
    0x23: "劈柴斧",
    0x24: "恶魔之斧",
    0xF1: "毒斧",
    0x46: "生锈的斧",
    0x26: "铁弓",
    0x27: "钢弓",
    0x28: "银弓",
    0x29: "圣弓",
    0x2A: "月光",
    0x2B: "帕提亚",
    0x2C: "米拉弓",
    0x2D: "长弓",
    0x2E: "必杀弓",
    0x2F: "光之弓",
    0xF0: "毒弓",
    0x3F: "生锈的弓1",
    0x40: "生锈的弓2",
    0x41: "生锈的弓3",
    0x42: "生锈的弓4",
    0x81: "革盾",
    0x82: "铁盾",
    0x83: "钢盾",
    0x84: "利昂家之盾",
    0x85: "福格家之盾",
    0x86: "银盾",
    0x87: "圣盾",
    0x88: "龙盾",
    0x89: "封魔盾",
    0x8A: "皇帝盾",
    0x8B: "多玛盾",
    0x8C: "王族之盾",
    0x43: "生锈的盾1",
    0x44: "生锈的盾2",
    0x45: "生锈的盾3",
    0xF2: "贤者之盾",
    0xF8: "十一盾",
    0x8E: "神圣戒指",
    0x8F: "天使戒指",
    0x90: "速度戒指",
    0x91: "魔道戒指",
    0x92: "祈祷戒指",
    0x93: "魔法书",
    0x94: "珊瑚戒指",
    0x95: "米拉戒指",
    0x96: "怨念戒指",
    0x97: "恶魔戒指",
    0x98: "遗物戒指",
    0x47: "生锈的戒指1",
    0x48: "生锈的戒指2",
    0xF4: "生锈的戒指3",
    0xF3: "靴子",
    0x8D: "银盘",
    0x99: "纪念品人偶",
    0x9A: "透明须",
    0x9B: "龙的鳞片",
    0x9C: "利马一族的手环",
    0x9D: "儿子的日记",
    0x9E: "木雕熊",
    0x9F: "木雕米拉",
    0xA0: "木雕多玛",
    0xA1: "珊瑚碎片",
    0xA2: "黑珍珠",
    0xA3: "石像鬼的耳朵",
    0xA4: "骷髅油",
    0xA5: "红色三角帽",
    0xA6: "可疑的面具",
    0xA7: "多玛的头盔",
    0xA8: "米拉的发饰",
    0xA9: "麦酒",
    0xAA: "喝剩的麦酒",
    0xAB: "汤",
    0xAC: "冷掉的汤",
    0xAD: "葡萄酒",
    0xAE: "大蒜",
    0xAF: "拉姆的葡萄酒",
    0xB0: "饮用水",
    0xB1: "多玛的青苔",
    0xB2: "鲱鱼",
    0xB3: "大衮鱼片",
    0xB4: "发酵乳",
    0xB5: "药草糖浆",
    0xB6: "柳橙",
    0xB7: "异国香料",
    0xB8: "香肠",
    0xB9: "带鱼干",
    0xBA: "胡萝卜",
    0xBB: "奶油",
    0xBC: "蜂蜜",
    0xBD: "火腿",
    0xBE: "面包",
    0xBF: "咬了一口的面包",
    0xC0: "小片面包",
    0xC1: "硬梆梆的面包",
    0xC2: "肉干",
    0xC3: "生肉",
    0xC4: "仙灵草",
    0xC5: "面粉",
    0xC6: "有洞的乳酪",
    0xC7: "青霉乳酪",
    0xC8: "香甜饼干",
    0xC9: "圣兽乳酪(速度+2)",
    0xCA: "琼浆玉液(幸运+2)",
    0xCB: "生命树果(HP+2)",
    0xCC: "仙馕(防御+2)",
    0xCD: "黄金苹果(等级+1)",
    0xCE: "苏摩(力量+2)",
    0xCF: "冥府石榴(技术+2)",
    0xD0: "霸者金币",
    0xD1: "一袋金币",
    0xD2: "银币",
    0xD3: "一袋银币",
    0xD4: "中袋银币",
    0xD5: "大袋银币",
    0xF9: "鸡肉沙拉",
    0xFA: "汤种吐司",
    0xFB: "美味辣炸鸡",
    0xFC: "千层蛋糕",
    0xFD: "黑色炸鸡",
    0xFE: "纯蜂蜜",
    0xD6: "监牢钥匙",
}

ITEM_VALUES, ITEM_LABELS = split_value_label(ITEMS)

B = bytes.fromhex

CHARID_ALM = B("CDE7C2253782C205")
CHARID_CELICA = B("C7D28D28D9CA2207")

CHARACTERS = {
    B("CDE7C2253782C205"): "阿鲁姆",
    B("07EF94FDE3950E05"): "卢卡",
    B("174B5327C9CF8706"): "格莱",
    B("BB31AC11BD5EDDFB"): "罗宾",
    B("365C7326A87A1A06"): "艾菲",
    B("A5A73627F7B07906"): "克里夫",
    B("60741B289A70EA06"): "希尔科",
    B("24B2362746B87906"): "克莱尔",
    B("3B907DB3F728EC4E"): "克雷贝",
    B("5772CA7B27137033"): "弗鲁斯",
    B("624F88176AC0935F"): "帕伊宋",
    B("AF47959C9B2644CE"): "鲁特",
    B("07B0D5DE8F5CDA10"): "玛蒂尔达",
    B("6974020975121F44"): "迪优特",
    B("867D31856A31A019"): "缇塔",
    B("E7D93A282DACFA06"): "吉克",
    B("E5AE9CDB35BB440F"): "迈森",
    B("C7D28D28D9CA2207"): "赛莉卡",
    B("86B994FD52700E05"): "梅伊",
    B("C05B402C46FAF508"): "波依",
    B("F071A328AC724235"): "杰妮",
    B("238581ED8B73B3D1"): "赛巴",
    B("1664E62A60BC4A08"): "巴尔博",
    B("360EC426382D4106"): "卡姆依",
    B("5FF494FDA3990E05"): "雷欧",
    B("23F4062B2D9C5B08"): "帕奥拉",
    B("C8C77167F877FC86"): "卡秋雅",
    B("C924DD07511647AB"): "阿特拉斯",
    B("FC06A32898274235"): "杰西",
    B("80B2CB28B2424207"): "索尼娅",
    B("845D1F1EE06B864E"): "迪恩",
    B("9FC67226B1111A06"): "爱丝特",
    B("CCFEAF2A72B13008"): "孔拉特",
    B("0544223A1727BCFF"): "诺玛",
    B("96DC98FDD2571105"): "Emma",
    B("452635116FBCA1FB"): "Randal",
    B("59D494FD2D830E05"): "Yuzu",
    B("EFC0B48F4FA55B00"): "Shade",
}

PROFESSIONS = {
    B("C51B98DC5787885C"): "村民（男）",
    B("831A98DC2786885C"): "村民（女）",
    B("4AC058885C6D1EBF"): "轻骑兵（男）",
    B("08BF58882C6C1EBF"): "轻骑兵（女）",
    B("89A60099B78ACB0C"): "帕拉丁（男）",
    B("47A500998789CB0C"): "帕拉丁（女）",
    B("BD41DF7E3385F1C6"): "黄金骑士（男）",
    B("7B40DF7E0384F1C6"): "黄金骑士（女）",
    B("0FFE1B4AA175776F"): "士兵",
    B("A612F3C21E68886D"): "重甲骑士",
    B("F6DB920958FF7BF2"): "男爵",
    B("5A40290862B10470"): "佣兵",
    B("66F4C9C39A01F651"): "剑士",
    B("52CF17AB9A7B8DCA"): "魔战士",
    B("E3E9012321FF7726"): "弓手",
    B("B28F72B8D40E4C9A"): "狙击手",
    B("38B628F2D6A2A4F3"): "弓骑兵",
    B("92F226DE6E78A15D"): "战士（阿鲁姆专用）",
    B("5A04E7044433696E"): "Hero",
    B("DD0EAFB1433FCFCC"): "魔道士（男）",
    B("9B0DAFB1133ECFCC"): "魔道士（女）",
    B("39DC3BC6D5C02953"): "贤者",
    B("9C62D71350DE579C"): "天马骑士",
    B("D74265C1A194D89A"): "角马骑士",
    B("69705A3B5F5180C6"): "修女",
    B("F903575FEB1ECE95"): "圣女",
    B("20FDDBEAF653E363"): "神官（女）",
    B("27FCDBEA4553E363"): "神官骑士 (赛莉卡专用)",
    B("E8A51124186AFE85"): "公主",
    B("F7F99AE449837761"): "男孩子",
    B("B5F89AE419827761"): "女孩子",
    B("9742C34037AEFAD2"): "Lord (Marth)",
    B("0942133AA9DEAFCF"): "Hero (Ike)",
    B("EFB6BE25D74AABC5"): "Lord (Lucina)",
    B("FA8BBF2522E0ABC5"): "Tactician (Robin)",
    B("185A06A44A912675"): "Lord (Roy)",
    B("503F90DB3CD08E74"): "Lord (CorrinM)",
    B("0E3E90DB0CCF8E74"): "Lord (CorrinF)",
    B("D964005DA93AA3A3"): "Conqueror (DLC)",
    B("81F6224C9BE113CE"): "Rigain (DLC)",
    B("7460F8D7AC561E25"): "Spartan (DLC)",
    B("D6402D042A30E3D3"): "Oliphantier (DLC)",
    B("572032FD3F4049A8"): "Exemplar (DLC)",
    B("E78EF6EE29DD61B3"): "Guru (DLC)",
    B("E5588604F5D2C4FE"): "Harrier (DLC)",
    B("398FBB505747C11F"): "Skogul (DLC)",
    B("D0537D79EED22FFD"): "Yasha (DLC)",
    B("CEAF96134A701BC4"): "Enchantress (DLC)",
    B("02825A5FA20BD095"): "Fiend",
    B("0D0D28E04D0CA05D"): "Brigand",
    B("BE0BFAD1864030EB"): "Arcanist",
    B("9037EFA118C296D4"): "Cantor",
    B("08815A5FAE0AD095"): "Witch",
    B("C56EE1B4938C944D"): "Revenant",
    B("377579B889EE5A4F"): "Entombed",
    B("664B89FC580A3B3C"): "Bonewalker",
    B("6F4E9854F78B45AC"): "Lich",
    B("3EC029DFF46EE535"): "Gargoyle",
    B("B8875909E4B75FF2"): "Deathgoyle",
    B("D81A5502DE4A9974"): "Necrodragon",
    B("224C595F145FCF95"): "White Dragon",
    B("FFE63DB7FD3ABF4E"): "Mogall",
    B("9A19565FB2A7CD95"): "Fell God",
    B("23D51B8BCB5E75ED"): "Mila's Servant",
    B("C68A3E760EE2B9D5"): "Duma's Apostle",
    B("AC37A3DAD8BDFA7F"): "Dracul",
    B("84E41FF620BD3979"): "Titan",
    B("83E832D5176CE059"): "Guardian",
    B("68ADE887607F0182"): "Garuda",
    B("6B9C3A078F24E84E"): "Vestal",
    B("FB8D384AD9E62632"): "Fafnir",
    B("88A21EB5768BB34D"): "Dagon",
    B("BA7A9509B2027EF2"): "Balor",
    B("15538ABD115E6820"): "Deimos",
    B("7F0C525F3B40CB95"): "Fire Dragon",
    B("F119565FDFA7CD95"): "Fell Dragon",
}

del B
