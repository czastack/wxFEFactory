PERSONS = ('男主角', '机械师', '女战士')
CHARIOTS = tuple('战车%d' % i for i in range(1, 9))


TITLES = (
    "HOMELESS",
    "FLOWER",
    "LOVEHT",
    "SCARYHT",
    "YAMISFAN",
    "THEONE",
    "HITMAN",
    "AZRAEL",
    "WUDI",
    "SLMKILLER",
    "REDDEVIL",
    "BOUNTIFUL",
    "LENDKING",
    "ITEMCLTER",
    "TANKMAN",
    "GREATHT",
    "LOVETANK",
    "WRENCHER",
    "MECHER",
    "TANKDOC",
    "TANKGM",
    "TANKMAGIC",
    "REPAIR",
    "MIGREPAIR",
    "SNIPER",
    "COMMANDER",
    "BATTLECMP",
    "",
    "",
    "NULL",
    "",
    "",
    "BOMBGIRL",
    "BAZOOKA",
    "MISSILE",
    "HIGHWIND",
    "ROSEWOOD",
    "DEATHLESS",
    "WPMASTER",
    "FINALWP",
    "ONEKILL",
    "DESTROIER",
    "FIGHTGD",
    "",
    "",
    "REDWOLF",
)

HUMAN_ITEMS = (
    "碱性车蜡",
    "修理工具箱",
    "机械师工具箱",
    "印花大手帕",
    "松的毛巾",
    "姐姐的毛巾",
    "防毒面具",
    "接地尾线",
    "耳塞",
    "再生胶囊",
    "回复胶囊",
    "回复饮剂",
    "能量胶囊",
    "全满饮剂",
    "中和乳霜",
    "碱性喷剂",
    "麻痹散",
    "灭火器",
    "兴奋剂",
    "加速剂",
    "火箭礼花",
    "铅笔型飞弹",
    "冷冻瓶",
    "催眠瓶",
    "蛊惑瓶",
    "小石子",
    "大石头",
    "火焰瓶",
    "浓缩酸液",
    "手榴弹",
    "信号发送器",
    "大款钱包",
    "蚊香",
    "错乱注射器",
    "硝化甘油瓶",
    "DD菠萝弹",
    "杀虫剂",
    "BS机",
    "烟幕弹礼花",
    "降水机器人",
    "地雷探测器",
    "金属探测器",
    "青蛙赛跑掌上机",
    "战车射击掌上机",
    "怪物的照片-沙门菌猿一家",
    "怪物的照片-Dr.霸王花",
    "怪物的照片-食人鱼怪",
    "怪物的照片-马歇尔",
    "怪物的照片-猛犸象",
    "怪物的照片-甲壳虫战车",
    "怪物的照片-铜管乌贼",
    "怪物的照片-齐柏林水母",
    "怪物的照片-神风鬼王",
    "怪物的照片-鬼蜈蚣",
    "怪物的照片-戈麦斯",
    "怪物的照片-垃圾怪弗兰克",
    "怪物的照片-沙门菌猿波特",
    "怪物的照片-乐狂",
    "怪物的照片-隆美尔游魂战车",
    "怪物的照片-帕鲁.巴迪斯",
    "怪物的照片-仿生战狗",
    "怪物的照片-巨型炮",
    "怪物的照片-衣橱异型",
    "怪物的照片-不良团体",
    "怪物的照片-帕鲁的手下",
    "怪物的照片-变异鳄鱼",
    "怪物的照片-滴管无翼鸟",
    "怪物的照片-劫匪战车",
    "怪物的照片-妖虎战车",
    "怪物的照片-毁灭战车",
    "帕鲁的照片",
    "军号",
    "猎人典籍",
    "甘甜的水",
    "古钱币",
    "草莓口红",
    "ID卡(c)",
    "ID卡(o)",
    "ID卡(m)",
    "ID卡(p)",
    "ID卡(u)",
    "ID卡(t)",
    "ID卡(e)",
    "ID卡(r)",
    "房门钥匙",
    "万能钥匙",
    "松的肥皂",
    "麻醉胶囊",
    "纹身贴纸",
    "闪银耳环",
    "父亲的衬衣",
    "姐姐的围裙",
    "松的睡袍",
    "松的拖鞋",
    "眼镜镜片",
    "镜头镜片",
    "红宝石镜片",
    "太阳镜片",
    "汪汪狗食",
    "铜棒",
    "银棒",
    "金棒",
    "研究工作笔记",
    "沾血的记事本",
    "密码备忘录",
    "结婚戒指",
    "猴子的指甲泥",
    "生化麦芽",
    "蛙人的脚蹼",
    "不明细胞",
    "蟹黄",
    "蚂蚁内脏",
    "蚁黄",
    "转舞细胞",
    "滑溜细胞",
    "冰凉细胞",
    "鳄鱼胸脯肉",
    "蜂蜜",
    "坚硬细胞",
    "鸟胸肉",
    "痘痘细胞",
    "章鱼疣",
    "粘稠细胞",
    "流星细胞",
    "酸肝",
    "柔软果子",
    "瘫软种子",
    "冻肉",
    "无(只能放在最后)"
) # END is 0xFF

HUMAN_EQUIPS = (
    "钢珠弹弓",
    "弩枪",
    "霰弹枪",
    "印地安战斧",
    ".44大型左轮",
    "回旋扳手",
    "红牡丹匕首",
    "乌兹冲锋手枪",
    "爆裂电锯",
    "火焰枪",
    "激光步枪",
    "榴弹冲锋枪",
    "飞行军刀",
    "声波枪",
    "手持火神炮",
    "中子炮",
    "棒球发球机",
    "超声波枪",
    "光束剑",
    "火箭筒",
    "飞火铁拳",
    "飞龙喷火",
    "TNT弹连发箱",
    "切腹刀",
    "除草火焰枪",
    "柳钉枪",
    "双重链锯",
    "电击鞭",
    "酸液枪",
    "兰博的火弓",
    "冷冻光束枪",
    "TNT风暴炮",
    "遥控扳手",
    "光束暴雪枪",
    "咆哮枪",
    "恺撒铁爪",
    "最终风暴枪",
    "等离子暴雨枪",
    "恶棍的开山刀",
    "戈麦斯的铁锤",
    "激光炮-单体350",
    "激光炮-一组320",
    "激光炮-全体300",
    "激光炮-单体400",
    "激光炮-一组380",
    "激光炮-全体330",
    "激光炮-单体500",
    "激光炮=全体420",
    "棒球帽",
    "迷彩贝雷帽",
    "坦克手皮帽",
    "工地安全帽",
    "橄榄球头盔",
    "赛车手头盔",
    "兔女郎帽",
    "中东人头巾",
    "防弹假发",
    "冰球面具",
    "人造纤维头盔",
    "虎皮帽",
    "狙击手头盔",
    "礼帽",
    "机动部队头盔",
    "和平之头带",
    "帆布衣",
    "迷彩服",
    "皮衣",
    "重型皮外套",
    "消防服",
    "绝缘披风",
    "金属格斗装",
    "高能聚合衣",
    "指挥官风衣",
    "飞行服",
    "绝缘装",
    "飞车特技装",
    "凯夫拉旗袍",
    "高温作业服",
    "医师服",
    "凯旋大衣",
    "钢铁护胸",
    "桑拿浴紧身衣",
    "高腰身甲",
    "CVC隔热绝缘服",
    "西伯利亚大衣",
    "战车手连体装",
    "聚酰胺耐热服",
    "突击队战甲",
    "白线手套",
    "皮手套",
    "机械师手套",
    "重金属手套",
    "赛车手手套",
    "战斗手套",
    "金属拳套",
    "神力手套",
    "神枪手护腕",
    "格斗手套",
    "袜子",
    "高跟鞋",
    "钉鞋",
    "劳保鞋",
    "鳄鱼皮鞋",
    "高弹力靴",
    "战斗钉鞋",
    "金属护腿",
    "举重运动鞋",
    "陆军作战靴",
    "报废的护甲",
    "防护皮甲",
    "红牡丹胸甲",
    "防弹背心",
    "陶瓷护垫",
    "钢铁束腰护甲",
    "硅胶护垫",
    "护体挡板",
    "高效防护背心",
    "绝缘罩甲",
    "抗激光背心",
    "全能护甲",
    "无(只能放在最后)"
) # END is 0x7F

CHASSIS = (
    "蛇式坦克",
    "越野车",
    "救护车",
    "装甲车",
    "虎式坦克",
    "M1坦克",
    "红狼坦克",
    "白虎坦克",
    "半履带式卡车",
    "拖车",
    "谢尔曼坦克",
    "猎豹防空炮车",
    "追猎者歼击车",
    "黑豹坦克",
)

HOLE_TYPES = ("大炮类", "机枪类", "特殊类", "无")
HOLE_TYPE_VALUES = (0, 1, 2, 0xFF)

CHARIOT_ITEMS = (
    "犬系统",
    "灭火装置",
    "发音盒α",
    "发音盒Z",
    "医疗装置",
    "装甲包40",
    "装甲包80",
    "装甲包L",
    "装甲包XL",
    "碱性涂层",
    "隐形涂层",
    "镜面涂层",
    "迷彩伪装",
    "电磁屏障",
    "换气装置",
    "冷气",
    "暖气",
    "空调",
    "雷达盘",
    "接地链条",
    "除臭剂",
    "皮革车座",
    "花纹车座套",
    "水晶车座套",
    "绒毛小熊玩具",
    "嫩叶标志",
    "欢迎超车标志",
    "猛犸象牙",
    "铅蘑菇",
    "鸟粪",
    "小兔挂饰",
    "一路平安护符",
) # END is 0x3F

CHARIOT_EQUIP_HEADS = (
    ("名称", "防御", "重量", "攻击/命中/积载", "弹仓/回避", "攻击范围/特性"),
    (240, 100, 100, 200, 150, 200),
)
CHARIOT_EQUIP_INFOS = (
    # 主炮, 防御, 重量, 攻击, 弹仓, 攻击范围
    ("35mm机关炮", 42, 85, 45, 99, "单体"),
    ("48mm机关炮", 42, 105, 70, 99, "单体"),
    ("88mm机关炮", 42, 195, 110, 99, "单体"),
    ("37mm炮", 39, 100, 75, 25, "单体"),
    ("45mm炮", 48, 120, 80, 10, "单体"),
    ("55mm炮", 48, 160, 120, 10, "单体"),
    ("75mm炮", 48, 180, 160, 10, "单体"),
    ("95mm炮", 48, 220, 230, 10, "单体"),
    ("105mm加农炮", 50, 250, 300, 10, "单体"),
    ("125mm加农炮", 50, 260, 400, 10, "单体"),
    ("135mm加农炮", 50, 270, 470, 10, "单体"),
    ("155mm加农炮", 50, 280, 540, 10, "单体"),
    ("175mm加农炮", 50, 290, 700, 10, "单体"),
    ("195mm加农炮", 50, 300, 720, 15, "单体"),
    ("205mm加农炮", 50, 310, 780, 10, "单体"),
    ("115mmT型炮", 58, 280, 350, 15, "单体"),
    ("125mmT型炮", 58, 320, 420, 15, "单体"),
    ("165mmT型炮", 58, 360, 620, 15, "单体"),
    ("165mm幽魂炮", 70, 100, 650, 5, "单体"),
    ("80mm火箭炮", 60, 400, 200, 25, "单体"),
    ("92mm火箭炮", 60, 420, 340, 25, "单体"),
    ("140mm火箭炮", 60, 480, 520, 25, "单体"),
    ("155mm火箭炮", 60, 530, 545, 30, "单体"),
    ("180mm火箭炮", 60, 1000, 710, 25, "单体"),
    ("160mm未定型炮", 65, 560, 570, 20, "单体"),
    ("177mm未定型炮", 65, 760, 640, 30, "单体"),
    ("180mm连环炮", 100, 850, 610, 10, "单体"),
    ("195mm连环炮", 120, 1000, 680, 10, "单体"),
    ("205mm红牡丹炮", 180, 1500, 700, 25, "单体"),
    ("220mm大地女神炮", 86, 1000, 800, 10, "单体"),
    ("225mm多头蛇炮", 140, 750, 720, 5, "单体"),
    ("雷电加农炮", 90, 600, 615, 10, "单体"),

    # 副炮
    ("7mm机枪", 28, 80, 40, 0, "单体"),
    ("7.7mm机枪", 28, 82, 43, 0, "单体"),
    ("9mm机枪", 28, 90, 60, 0, "单体"),
    ("11mm机枪", 28, 100, 100, 0, "单体"),
    ("13mm机枪", 28, 105, 145, 0, "单体"),
    ("15mm机枪", 28, 110, 160, 0, "单体"),
    ("18mm机枪", 28, 120, 240, 0, "单体"),
    ("25mm机枪", 28, 130, 350, 0, "单体"),
    ("格林炮", 30, 120, 75, 0, "一组"),
    ("9mm火神炮", 32, 140, 80, 0, "一组"),
    ("11mm火神炮", 32, 180, 130, 0, "一组"),
    ("15mm火神炮", 32, 195, 158, 0, "一组"),
    ("20mm火神炮", 32, 220, 280, 0, "一组"),
    ("22mm火神炮", 32, 250, 310, 0, "一组"),
    ("红牡丹火神炮", 95, 10, 340, 0, "一组"),
    ("火焰喷射器", 20, 240, 180, 0, "单体"),
    ("光束机枪", 40, 200, 200, 0, "单体"),
    ("雷电机枪", 40, 250, 245, 0, "单体"),
    ("追击激光机枪", 45, 200, 210, 0, "一组"),
    ("冲杀号角机枪", 50, 280, 270, 0, "单体"),
    ("猛攻长笛机枪", 50, 260, 295, 0, "一组"),
    ("雷暴机枪", 45, 300, 400, 0, "一组"),

    # 特殊炮
    ("ATM导弹", 25, 200, 320, 10, "单体"),
    ("MC刺客导弹", 36, 440, 540, 7, "单体"),
    ("圣剑导弹", 72, 240, 710, 5, "单体"),
    ("ATM红牡丹导弹", 30, 220, 768, 4, "单体"),
    ("火龙炮", 45, 350, 655, 3, "一组"),
    ("癫狂火夫炮", 58, 700, 420, 4, "一组"),
    ("LI花生米炮", 20, 400, 380, 2, "一组"),
    ("S龙卷风炮", 120, 1100, 860, 5, "一组"),
    ("RD燃烧弹炮", 40, 520, 340, 6, "一组"),
    ("固体燃烧弹炮", 50, 696, 350, 4, "一组"),
    ("波动炮", 100, 840, 800, 5, "一组"),
    ("TNT榴弹炮", 28, 180, 440, 3, "单体"),
    ("西红柿飓风炮", 80, 1100, 420, 4, "全体"),
    ("激光排炮", 28, 360, 410, 3, "单体"),
    ("冲击利刃弹", 70, 600, 620, 5, "单体"),
    ("DD暴走炮", 82, 560, 650, 15, "单体"),
    ("TNT清道夫炮", 84, 900, 540, 3, "全体"),
    ("暴雨气旋炮", 96, 1200, 600, 3, "全体"),
    ("踢踏舞者炮", 30, 240, 279, 4, "全体"),
    ("烈日中子炮", 60, 900, 580, 2, "全体"),

    # C装置, 防御, 重量, 命中, 回避, 程序
    ("哈尔900", 30, 80, 1, 1, ""),
    ("感恩II", 30, 90, 1, 1, "截"),
    ("沃兹奈尔克II", 40, 20, 2, 2, "返"),
    ("沃兹奈尔克SI", 60, 20, 3, 3, "返截"),
    ("99式神话", 140, 350, 4, 4, "援"),
    ("拉库特", 110, 120, 2, 2, "返援"),
    ("艾米", 100, 300, 5, 5, "返截援"),
    ("诺伊曼", 90, 60, 6, 6, "收"),
    ("所罗门2", 190, 200, 8, 8, "收截"),
    ("达罗斯1000", 170, 150, 4, 4, "收截援"),
    ("诺亚系统No.R", 98, 490, 15, 1, "杀"),
    ("哈尔900r", 30, 80, 1, 1, "租"),
    ("哈尔900r'", 30, 80, 1, 1, "租截"),
    ("哈尔900r''", 30, 80, 1, 1, "租截援"),
    ("沃兹奈尔克IIr", 40, 20, 2, 2, "租"),
    ("沃兹奈尔克IIr'", 40, 20, 2, 2, "租截援"),
    ("艾米r", 100, 300, 5, 5, "租援"),
    ("艾米r'", 100, 300, 5, 5, "租截"),
    ("艾米r''", 100, 300, 5, 5, "租截援"),
    ("所罗门2'", 190, 200, 8, 8, "租截援"),

    # 引擎, 防御, 重量, 载重
    ("甲壳虫", 24, 10, 8, "", ""),
    ("甲壳虫T", 24, 10, 9, "", ""),
    ("甲壳虫TT", 24, 10, 10, "", ""),
    ("横纲力士", 30, 20, 12, "", ""),
    ("横纲力士T", 30, 20, 15, "", ""),
    ("横纲力士TS", 30, 20, 18, "", ""),
    ("公牛", 40, 30, 20, "", ""),
    ("巨型公牛", 40, 30, 23, "", ""),
    ("终极公牛", 40, 30, 26, "", ""),
    ("涡轮动力", 58, 40, 27, "", ""),
    ("涡轮动力T", 58, 40, 29, "", ""),
    ("涡轮动力TT", 58, 40, 31, "", ""),
    ("V24超人", 83, 50, 32, "", ""),
    ("V32超人", 83, 50, 35, "", ""),
    ("V48超人", 83, 50, 38, "", ""),
    ("疾风", 90, 60, 40, "", ""),
    ("疾风T", 90, 60, 42, "", ""),
    ("疾风TS", 90, 60, 44, "", ""),
    ("OHC卡门", 100, 70, 45, "", ""),
    ("增强卡门", 100, 70, 48, "", ""),
    ("飞火卡门", 100, 70, 51, "", ""),
    ("V48金刚", 115, 80, 52, "", ""),
    ("V66金刚", 115, 80, 55, "", ""),
    ("V100金刚", 115, 80, 58, "", ""),
    ("苦力劳工", 80, 70, 25, "", ""),
    ("强力苦力劳工", 80, 70, 28, "", ""),
    ("最强苦力劳工", 80, 70, 32, "", ""),
)

CHARIOT_EQUIPS = tuple(item[0] for item in CHARIOT_EQUIP_INFOS) # END is 0x7F

SPECIAL_BULLETS = ()


WANTED_LIST = (
    "沙门菌猿一家",
    "Dr.霸王花",
    "食人鱼怪",
    "马歇尔",
    "猛犸象",
    "甲壳虫战车",
    "铜管乌贼",
    "齐柏林水母(固)",
    "神风鬼王",
    "鬼蜈蚣",
    "戈麦斯",
    "垃圾怪弗兰克",
    "沙门菌猿波特",
    "乐狂",
    "隆美尔游魂战车",
    "帕鲁·巴迪斯",
)
WANTED_STATUS = ("未击败", "击破", "已领赏金")
WANTED_STATUS_VALUES = (0, 0x63, 0xE3)