from lib.utils import gen_values, gen_flag


STATUS = ('无', '毒', '睡', '沉默', '狂暴')
STATUS_VALUE = gen_values(STATUS)

ITEMS = (
    "无",
    "(E)铁剑",
    "(E)细剑",
    "(D)钢剑",
    "(A)银剑",
    "(D)铁之大剑",
    "(C)钢之大剑",
    "(A)银之大剑",
    "(D)毒剑",
    "(★)突刺剑",
    "(★)玛尼·卡缇",
    "(B)勇者之剑",
    "(D)倭刀",
    "(C)必杀刃",
    "(C)破甲剑",
    "(C)斩龙剑",
    "(C)光之剑",
    "(A)卢尼之剑",
    "(C)破枪剑",
    "(D)长柄刀",
    "(E)铁枪",
    "(E)细枪",
    "(D)钢枪",
    "(A)银枪",
    "(E)毒枪",
    "(B)勇者之枪",
    "(C)必杀枪",
    "(D)刺马枪",
    "(E)投枪",
    "(B)锁链枪",
    "(C)破斧枪",
    "(E)铁斧",
    "(E)钢斧",
    "(A)银斧",
    "(D)毒斧",
    "(B)勇者之斧",
    "(C)必杀斧",
    "(D)战戟",
    "(D)大锤",
    "(E)恶魔之斧",
    "(E)投斧",
    "(A)回旋斧",
    "(C)破剑斧",
    "(C)弑剑斧",
    "(E)铁弓",
    "(D)钢弓",
    "(A)银弓",
    "(D)毒弓",
    "(C)必杀弓",
    "(B)勇者之弓",
    "(D)短弓",
    "(D)长弓",
    "(E)弩",
    "(E)钢铁弩",
    "(E)必杀弩",
    "(E)火炎",
    "(D)闪电",
    "(C)地狱业火",
    "(B)雷暴",
    "(A)终末之冬",
    "(★)弗尔布雷斯(业火之理)",
    "(S)神之风刃",
    "(E)闪光",
    "(D)阳光",
    "(C)神圣之光",
    "(B)净化之光",
    "(A)光轮",
    "(S)露丝",
    "(D)熔流",
    "(C)月光",
    "(C)吸星术",
    "(B)月食",
    "(A)诺斯费拉特",
    "(S)格斯潘斯特",
    "(E)回复之杖",
    "(D)治疗之杖",
    "(C)痊愈之杖",
    "(B)治愈之杖",
    "(A)生命之杖",
    "(C)恢复之杖",
    "(B)沉默之杖",
    "(B)睡眠之杖",
    "(B)狂乱之杖",
    "(A)传送杖",
    "(B)救援杖",
    "(D)松明之杖",
    "(C)修理杖",
    "(D)开锁杖",
    "(C)魔防杖",
    "(C)龙斧",
    "天使之衣",
    "能量指环",
    "秘传之书",
    "疾风之羽",
    "女神像",
    "龙盾",
    "魔法护身符",
    "靴子",
    "体格指环",
    "英雄之证",
    "骑士勋章",
    "猎户座之箭",
    "天空之鞭",
    "导引之指环",
    "宝箱钥匙",
    "门钥匙",
    "盗贼钥匙",
    "伤药",
    "特效药",
    "圣水",
    "消毒液",
    "火把",
    "迪鲁菲的守护",
    "会员卡",
    "银卡",
    "白色宝玉",
    "青色宝玉",
    "赤色宝玉",
    "金币",
    "(B)锁链枪",
    "宝箱钥匙",
    "炎之爆弹",
    "光之结界",
    "帕比斯的守护",
    "法拉之力",
    "尼尼斯之守护",
    "托尔之怒",
    "赛奇之祈祷",
    "(E)军师之剑",
    "(E)军师之枪",
    "(E)军师之斧",
    "(E)军师之弓",
    "(★)幽兰黛尔(烈火之剑)",
    "(★)阿尔玛兹(天雷之斧)",
    "(S)亚利艾尔(至高之光)",
    "地之刻印",
    "亚法之水滴",
    "天之刻印",
    "军师之书",
    "暗之契约书",
    "(★)索尔·卡缇",
    "(★)群狼之灾",
    "(-)艾雷修基加尔",
    "灼热的气息",
    "(S)帝王之剑",
    "(S)王者之枪",
    "(S)暴君之斧",
    "(S)利安弗列切",
    "(D)刺突枪",
    "(C)短枪",
    "霸者之证",
    "3000G",
    "5000G",
    "(B)风之剑",
    "伤药",
    "伤药",
    "伤药",
    "舞蹈",
    "演奏",
)
ITEM_VALUES = gen_values(ITEMS)

CHAPTERS = (
    "序章　草原的少女",
    "第1章　命运的脚步声",
    "第2章　精灵之剑",
    "第3章　小小佣兵团",
    "第4章　生计下的阴影",
    "第5章　穿越国境",
    "第6章　自豪的血统",
    "第7章　旅行的姐弟",
    "第7章外传　黑影",
    "第8章　谋略的漩涡",
    "第9章　悲哀的再会",
    "第10章　遥远的草原",
    "第11章　旅行开始",
    "第11章　旅行开始",
    "第12章　比肩的朋友",
    "第13章　寻求真实",
    "第13章外传　行商人马里纳斯",
    "第14章　蠢蠢欲动的家伙们",
    "第14章　蠢蠢欲动的家伙们",
    "第15章　基亚兰的公女",
    "第16章　谜一般的行踪",
    "第16章外传　港镇帕顿",
    "第17章　海盗船",
    "第18章　魔之岛",
    "第18章外传　封魔者",
    "第18章外传　封魔者",
    "第19章　龙之门",
    "第20章　新的决意",
    "第21章　两个羁绊",
    "第22章　活生生的传说",
    "第22章外传　制造的生命",
    "第23章A　四牙袭来",
    "第23章B　四牙袭来",
    "第23章　四牙袭来",
    "第24章　触摸不到的手，传达不到的心",
    "25章A　黑暗的白花",
    "25章B　黑暗的白花",
    "26章　黎明前的攻防",
    "26章外传　决别之夜",
    "27章　命运的齿轮",
    "28章　勇者罗兰",
    "28章　勇者罗兰",
    "29章　悠久的黄沙",
    "29章外传　战斗准备",
    "30章　背水一战",
    "30章　背水一战",
    "终章　光",
    "终章　光",
)
CHAPTER_VALUES = gen_values(CHAPTERS)

PROFESSIONS = (
    "领主(艾利乌德)",
    "领主(琳)",
    "领主(赫克托耳)",
    "利西亚骑士",
    "利西亚剑士",
    "利西亚重骑士",
    "领主骑士",
    "利刃领主",
    "重装领主",
    "佣兵(男)",
    "佣兵(女)",
    "勇者(男)",
    "勇者(女)",
    "剑士(男)",
    "剑士(女)",
    "剑圣(男)",
    "剑圣(女)",
    "战士(男)",
    "大战士(男)",
    "重甲骑士(男)",
    "重甲骑士(女)",
    "将军(男)",
    "将军(女)",
    "弓兵(男)",
    "弓兵(女)",
    "弓箭手(男)",
    "弓箭手(女)",
    "修道士(男)",
    "僧侣(女)",
    "司祭(男)",
    "司祭(女)",
    "魔道士(男)",
    "魔道士(女)",
    "贤者(男)",
    "贤者(女)",
    "巫师(男)",
    "巫师(女)",
    "德鲁伊(男)",
    "德鲁伊(女)",
    "轻骑士(男)",
    "轻骑士(女)",
    "圣骑士(男)",
    "圣骑士(女)",
    "神官骑士(女)",
    "女武神(女)",
    "游牧民(男)",
    "游牧民(女)",
    "游牧骑兵(男)",
    "游牧骑兵(女)",
    "天马骑士(女)",
    "隼骑士(女)",
    "龙骑士(男)",
    "龙骑士(女)",
    "龙骑统帅(男)",
    "龙骑统帅(女)",
    "士兵",
    "山贼(男)",
    "海贼(男)",
    "狂战士(男)",
    "盗贼(男)",
    "盗贼(女)",
    "刺客",
    "市民(倒下)",
    "舞者",
    "吟游诗人",
    "大贤者",
    "魔封者",
    "运输队(帐篷)",
    "灾祸招致者",
    "太古的火龙",
    "市民(小男孩)",
    "市民(小女孩)",
    "(死亡)",
    "布拉米蒙德",
    "贵族(男)",
    "贵族(女)",
    "伯尔尼王子",
    "公主",
    "市民",
    "湖盗",
    "伯尔尼王子(军师)",
    "伯尔尼王子(倒下)",
    "伯尔尼王子(背朝)",
    "孩子(舞女背朝)",
    "太古的火龙(白龙)",
    "勇士(倒下)",
    "孩子(小男孩)",
    "孩子(小女孩)",
    "运输队(马车)",
    "贤者(女)",
    "(弩车)",
    "(弩车)",
    "(弩车)",
    "(弩车)",
    "(弩车)",
    "(弩车)",
    "(空)",
)
PROFESSION_VALUES = tuple(0x8C4F4BC + i * 0x54 for i in range(len(PROFESSIONS)))

PROFICIENCYS = ('S级', 'A级', 'B级', 'C级', 'D级', 'E级', '-级')
PROFICIENCY_VALUES = (0xFB, 0xC9, 0x79, 0x47, 0x1F, 0x01, 0x00)