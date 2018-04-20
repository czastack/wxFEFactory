from lib import utils
from .. import datasets
from ..datasets import PERSONALITYS

BACKPACK_LABELS = datasets.BACKPACK_LABELS[:-1]
BACKPACK_KEYS = datasets.BACKPACK_KEYS[:-1]


APPEARANCE = (
    "男孩",
    "女孩",
    "男孩－骑自行车－快速",
    "女孩－骑自行车－快速",
    "男孩－骑自行车－慢速",
    "女孩－骑自行车－慢速",
    "男孩－滑梯",
    "女孩－滑梯",
    "男孩－潜水",
    "女孩－潜水",
    "男孩－掏精灵球(bug)",
    "女孩－掏精灵球(bug)",
    "男孩－甩钓鱼杆",
    "女孩－甩钓鱼杆",
    "男孩－浇水",
    "女孩－浇水",
)


AREAS = (
    (0x0001, "你家的那个小镇"),
    (0x0002, "101路上方的小镇"),
    (0x0003, "格斗系道观小镇"),
    (0x0004, "火系道观小镇"),
    (0x0005, "火山灰道观小镇"),
    (0x0006, "117路左边小镇"),
    (0x0007, "暮水镇"),
    (0x0008, "普通系道观小镇"),
    (0x0009, "卡依船厂"),
    (0x000A, "电系道观小镇"),
    (0x000B, "石系道观小镇"),
    (0x000C, "飞行系道观小镇"),
    (0x000D, "驻守区旁小镇"),
    (0x000E, "超能力道观小镇"),
    (0x000F, "水系道观小镇"),
    (0x0010, "第一个四大天王"),
    (0x0011, "乘船老爷爷家"),
    (0x0012, "四口之家"),
    (0x0013, "坐缆车的地方"),
    (0x0014, "火山灰镇得TM28的地方"),
    (0x0016, "饲养屋"),
    (0x0017, "驻守区"),
    (0x0018, "流星瀑布"),
    (0x001D, "古力可小屋"),
    (0x001E, "得到收集火山灰的屋子"),
    (0x001F, "果实老人家"),
    (0x0020, "得到小电怪的研究所"),
    (0x0021, "兑换进化石"),
    (0x0101, "自己房间"),
    (0x0102, "古辰镇右下角的小屋"),
    (0x0103, "武斗镇"),
    (0x0104, "釜炎镇道馆"),
    (0x0105, "对战帐篷秋叶镇分址"),
    (0x0106, "对战帐篷绿荫镇分址"),
    (0x0107, "暮水镇神奇宝贝中心2楼"),
    (0x0108, "橙华市道馆"),
    (0x0109, "库斯诺吉的船场2楼"),
    (0x010A, "风野自行车行"),
    (0x010B, "卡那兹市 得文公司2楼"),
    (0x010C, "茵郁市道馆"),
    (0x010D, "水静市 静水旅馆2楼"),
    (0x010E, "绿岭市道馆左边的小屋"),
    (0x010F, "琉璃市道馆地下"),
    (0x0110, "第三个四大天王（女）"),
    (0x0111, "漂亮的花瓣花店"),
    (0x0112, "老奶奶的歇息小屋"),
    (0x0113, "釜炎镇附近的缆车屋"),
    (0x0114, "化石迷之家（拿挖洞技）"),
    (0x0115, "扶养家"),
    (0x0116, "野生原野区"),
    (0x0117, "流星瀑布"),
    (0x0118, "流星瀑布地下"),
    (0x0119, "秘密基地"),
    (0x011A, "野生原野区"),
    (0x011B, "104号公路（bug）"),
    (0x011C, "110号公路-奇妙的戏法屋"),
    (0x011D, "奇妙的戏法屋内"),
    (0x011E, "123号公路-树果大神的家"),
    (0x011F, "得到小电怪的研究所"),
    (0x0120, "得到小电怪的研究所内"),
    (0x0202, "古辰镇"),
    (0x0203, "武斗镇PC 2楼"),
    (0x0204, "釜炎镇道馆内"),
    (0x0205, "锦标赛"),
    (0x0206, "锦标赛2"),
    (0x0207, "暮水镇PC右边小屋"),
    (0x0208, "橙华市PC左边小屋"),
    (0x020C, "茵郁市"),
    (0x020F, "琉璃岛"),
    (0x030E, "绿岭市"),
    (0x031A, "狩猎区"),
    (0x0405, "秋叶镇"),
    (0x0406, "绿荫镇"),
    (0x0408, "橙华市"),
    (0x0504, "釜炎镇"),
    (0x050A, "紫堇市"),
    (0x050B, "卡那兹市"),
    (0x060D, "水静市"),
    (0x0A10, "彩幽市"),
    (0x0A1A, "南岛"),
    (0x0B09, "凯那市"),
    (0x0C10, "彩幽市"),
    (0x351A, "对战开拓区"),
    (0x3810, "潜水洞"),
    (0x3811, "冠军之路（斗士载入）"),
    (0x3812, "看看洞"),
    (0x3815, "无人发电厂"),
    (0x3819, "未知"),
    (0x381A, "梦幻岛"),
    (0x3A1A, "迪奥西斯"),
    (0x4210, "以前捕捉古拉顿和海皇牙的洞"),
    (0x4211, "废弃船"),
    (0x4217, "废弃船拿钥匙的屋子"),
    (0x4219, "新大陆战斗塔"),
    (0x421A, "凤凰、路基亚捕捉地点"),
)

AREA_LABELS, AREA_VALUES = utils.split_value_label(AREAS)

FURNITURES = (
    "无",
    "小桌子",
    "怪兽桌子",
    "沉桌子",
    "硬桌子",
    "轻桌子",
    "美丽桌子",
    "砖的桌子",
    "露营桌子",
    "坚硬桌子",
    "小椅子",
    "怪兽椅子",
    "沉椅子",
    "硬椅子",
    "轻椅子",
    "美丽椅子",
    "砖的椅子",
    "露营椅子",
    "坚硬椅子",
    "鲜红的花树",
    "南国的花树",
    "可爱的花树",
    "美丽的花树",
    "大大的花树",
    "奇丽的花树",
    "红砖",
    "黄砖",
    "蓝砖",
    "红气球",
    "蓝气球",
    "黄气球",
    "红帐篷",
    "蓝帐篷",
    "结实的木板",
    "滑台",
    "直栅栏",
    "横栅栏",
    "轮胎",
    "大高台",
    "泥团子",
    "破门",
    "沙子装饰品",
    "银盾",
    "金盾",
    "玻璃花瓶",
    "电视",
    "圆的电视",
    "可爱电视3",
    "闪光地毯",
    "跳跃地毯",
    "圆的地毯",
    "音乐地毯CL",
    "音乐地毯D",
    "音乐地毯E",
    "音乐地毯F",
    "音乐地毯G",
    "音乐地毯A",
    "音乐地毯B",
    "音乐地毯CH",
    "冲浪术地毯",
    "雷电地毯",
    "大文字地毯",
    "米雪地毯",
    "颓废地毯",
    "地裂地毯",
    "卷曲地毯",
    "球宣传画",
    "绿宣传画",
    "红宣传画",
    "水色宣传画",
    "可爱宣传画",
    "闪光宣传画",
    "长的宣传画",
    "大海宣传画",
    "天空宣传画",
    "热吻宣传画",
    "皮丘类型",
    "皮卡丘类型",
    "水鼠类型",
    "波克比类型",
    "火球鼠类型",
    "菊草叶类型",
    "小锯鳄类型",
    "胖丁类型",
    "喵喵类型",
    "皮皮类型",
    "百变怪类型",
    "迷唇娃类型",
    "草青蛙类型",
    "火稚鸡类型",
    "水精灵类型",
    "钻墙怪类型",
    "快乐兽类型",
    "古生兽类型",
    "变色兽类型",
    "利利鼠类型",
    "小松鼠类型",
    "云雀类型",
    "库林怪类型",
    "顶叶兽类型",
    "种子怪类型",
    "皮卡型",
    "圆的型",
    "热吻型",
    "针鼠型",
    "古鲁鲁型",
    "钻石型",
    "球型",
    "草型",
    "火焰型",
    "水型",
    "卡比兽类型",
    "铁甲暴龙类型",
    "乘龙类型",
    "妙蛙花类型",
    "喷火龙类型",
    "水箭龟类型",
    "皮皮鲸类型",
    "雷兽类型",
    "土雷兽类型",
    "天雷兽类型",
)

ITEMS = (
    "无",
    "大师球",
    "超力怪兽球",
    "超级球     比怪兽球更厉害些",
    "怪兽球     普通的球",
    "砂狐球     砂狐乐园专用球",
    "触网球     容易抓水和虫类的怪兽",
    "大布斯球        容易抓海底的怪兽",
    "尼斯道球        怪兽越弱越容易抓",
    "利比道球        容易抓抓过的球",
    "达伊玛球        回合数越长越容易抓",
    "高基石球        抓到的怪兽变亲密",
    "布雷密球        珍惜怪兽球",
    "伤药      体力恢复20",
    "解毒药     恢复毒状态",
    "烧伤恢复        恢复烧伤状态",
    "解冻药     恢复冻状态",
    "清醒药     恢复沉睡状态",
    "麻痹恢复        恢复麻痹状态",
    "恢复药     全恢复体力与所有状态",
    "慢谈药     体力全恢复",
    "伤药      体力恢复200",
    "好伤药     体力恢复50",
    "万能恢复        全部恢复",
    "精神片     死亡恢复体力一半",
    "精神草     死亡全恢复体力",
    "美味水     恢复体力50",
    "精神汽水        恢复体力60",
    "米力液     恢复体力80",
    "木木奶     恢复体力100",
    "力量粉     恢复体力50，很苦粉，减低怪兽亲密度",
    "力量根     恢复体力200，很苦根，减低怪兽亲密度",
    "万能粉     全恢复状态，非常苦的粉，大大减低与怪兽的亲密度",
    "复活草     死亡复活，很苦的草",
    "PP艾依        1种技能值恢复10",
    "PP力卡        1种技能值全恢复",
    "未知",
    "PP最大        1只怪兽的全部技能值全恢复",
    "飞音饼     恢复全部异常状态",
    "蓝玻璃     恢复沉睡状态，可用无限次",
    "黄玻璃     恢复混乱状态，可用无限次",
    "红玻璃     恢复颓废状态，可用无限次",
    "黑玻璃     不遇野生怪兽",
    "白玻璃     容易遇野生怪兽",
    "树果汁     恢复体力20",
    "圣是      死亡恢复全部体力，异常状态恢复",
    "浅水盐     看看洞用的道具",
    "浅水贝     看看洞用的道具",
    "红碎片     换进化石的道具",
    "蓝碎片     换进化石的道具",
    "黄碎片     换进化石的道具",
    "绿碎片     换进化石的道具",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "最大上升        体力基础值提高",
    "赞美语     攻击基础值提高",
    "落海夫     防御基础值提高",
    "因得西     敏捷基础值提高",
    "立麦森     特攻基础值提高",
    "奇异甜食        怪兽升1级",
    "值上升     技能值的最大值上升",
    "极道山果        德望基础值提高",
    "值最大     技能值提高到最大",
    "未知",
    "效果卡     战斗中…能避开对方的攻击，用于装备",
    "清洗物     战斗中…容易命中要害，用于装备",
    "布拉斯力量       战斗中…攻击力上升，用于装备",
    "力道      战斗中…防御力上升，用于装备",
    "敏捷力     战斗中…敏捷上升，用于装备",
    "纪念打     战斗中…技能容易命中",
    "特别上升        战斗中…特攻的威力上升，用于装备",
    "皮皮木偶        在战斗中逃脱",
    "小松鼠尾        在战斗中逃脱",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "太阳石     让独特的怪兽进化",
    "月亮石     让独特的怪兽进化",
    "火焰石     让独特的怪兽进化",
    "雷电石     让独特的怪兽进化",
    "水石      让独特的怪兽进化",
    "珊瑚石     让独特的怪兽进化",
    "未知",
    "未知",
    "未知",
    "未知",
    "小的树果        普通的树果容易成熟",
    "大的树果        珍贵的树果难成熟",
    "未知",
    "珍珠      美丽的珍珠容易成熟",
    "大珍珠     很美丽的大珍珠难成熟",
    "星沙      美丽的红色的沙子",
    "星星碎片        美丽的红宝石碎片",
    "金珠      金星",
    "心灵碎片        可以恢复忘却的技能",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "彩色邮件        针鼠模样的信件",
    "哈伯邮件        海鸥模样的信件",
    "闪光邮件        皮卡丘模样的信件",
    "机械邮件        小磁怪模样的信件",
    "鸟烟邮件        食叶兽模样的信件",
    "十字邮件        皮皮鲸模样的信件",
    "珍贵邮件        有持有怪兽模样的信件",
    "阴影邮件        钻墙怪模样的信件",
    "热带邮件        美丽花模样的信件",
    "花边邮件        有持有怪兽模样的信件",
    "神奇邮件        豪华的信件",
    "怀旧邮件        3只怪兽的信件",
    "解麻果     恢复麻痹状态1号",
    "醒睡果     恢复沉睡状态2号",
    "解毒果     恢复中毒状态3号",
    "烧伤果     恢复烧伤状态4号",
    "解冻果     恢复冰冻状态5号",
    "木果      恢复技能值10，6号",
    "桔果      恢复体力10，7号",
    "太阳果     恢复混乱状态8号",
    "雷木果     恢复全部状态9号",
    "黄石果     恢复体力30，10号",
    "飞来果     恢复体力产生混乱11号",
    "沙一果     恢复体力产生混乱12号",
    "真之果     恢复体力产生混乱13号",
    "混光果     恢复体力产生混乱14号",
    "易果      恢复体力产生混乱15号",
    "红果      怪兽盒材料16号",
    "紫果      怪兽盒材料17号",
    "香果      怪兽盒材料18号，会种出娜娜",
    "利果      怪兽盒材料19号",
    "波罗果     怪兽盒材料20号",
    "灯灯果     怪兽盒材料21号",
    "猫形果     怪兽盒材料22号",
    "水波果     怪兽盒材料23号",
    "黄果      怪兽盒材料24号",
    "鸟布果     怪兽盒材料25号",
    "红刺果     怪兽盒材料26号",
    "木高西果        怪兽盒材料27号",
    "高芝果     怪兽盒材料28号",
    "布拉达果        怪兽盒材料29号",
    "麦鲁果     怪兽盒材料30号",
    "万吉果     怪兽盒材料31号",
    "西亚果     怪兽盒材料32号",
    "卡依斯果        怪兽盒材料33号",
    "刀利果     怪兽盒材料34号",
    "海比果     怪兽盒材料35号",
    "吉拉果     战斗中…危急时攻击力上升36号",
    "利卡果     战斗中…危急时防御力上升37号",
    "卡木拉果        战斗中…危急时敏捷上升38号",
    "哑达比果        战斗中…危急时特攻上升39号",
    "阿芝果     战斗中…危急时德望上升40号",
    "山果      战斗中…危急时容易命中要害41号",
    "星星果     战斗中…危急时使其中一种能力迅速提高42号",
    "神秘果有        怪兽盒材料43号",
    "未知",
    "未知",
    "未知",
    "光粉      降低对手命中率",
    "白色海石花       下降能力复原",
    "竞争背心        敏捷下降，好好饲育",
    "学习装置        持有的怪兽得到经验值",
    "老师指甲        偶尔能先发出攻击",
    "安闲玲     持有的怪兽变亲密",
    "精神海石花       持有的怪兽恢复颓废状态",
    "守日器     攻击的威力提高",
    "王者之证        有时能让对手沉睡",
    "银粉      虫类技能的威力上升",
    "守卫饭     持有的怪兽参战能得到2倍金钱",
    "清符      难以与野生怪兽",
    "心珠      特攻和德望上升，限于雄奇怪和木皮怪",
    "进化牙     特攻上升，限于海贝",
    "进化鳞片        德望上升，限于海贝",
    "烟珠      遇到野生的怪兽能逃脱",
    "不变石     持有的怪兽不会进化",
    "精神器     偶尔能防御",
    "幸福怪兽蛋       怪兽经验值更容易上升",
    "焦点镜     容易命中要害",
    "杯衣      钢类技能威力上升",
    "余物      体力能在战斗间慢慢恢复",
    "龙鳞      飞龙类怪兽持有的奇异鳞片",
    "电珠      特攻上升，限于皮卡丘",
    "软沙      地面类技能的威力上升",
    "坚硬石头        岩石类技能的威力上升",
    "奇迹种     草类技能的威力上升",
    "黑色眼镜        恶类技能的威力上升",
    "黑带      格斗类技能的威力上升",
    "磁铁      电类技能的威力上升",
    "神秘水珠        水类技能的威力上升",
    "尖嘴      飞行类技能的威力上升",
    "毒针      毒类技能的威力上升",
    "不化冰     冰冻技能的威力上升",
    "诅咒符     幽灵类技能的威力上升",
    "银勺      超能技能的威力上升",
    "木炭      火焰类技能的威力上升",
    "龙牙      飞龙类技能的威力上升",
    "西库头巾        正常类技能的威力上升",
    "上升叶片        奇异箱子，收集用",
    "空贝      对敌人损伤时体力会恢复",
    "潮物      水类技能的威力上升一点",
    "气物      敌人的命中率下降一点",
    "吉利蛋钳        容易命中要害，限于吉利蛋",
    "木物      防御力上升，限于百变怪",
    "粗骨头     手持道具，若可拉可拉或嘎拉嘎拉持有，则其攻击×2倍",
    "道具大葱        手持道具，若大葱鸭持有，则其会心一击率升２级",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "未知",
    "红手巾     持有参加比赛会比平时显得聪明",
    "蓝手巾     持有参加比赛会比平时显得美丽",
    "粉手巾     持有参加比赛会比平时显得可爱",
    "绿手巾     持有参加比赛会比平时显得聪明",
    "黄手巾     持有参加比赛会比平时显得坚强",
    "音速自行车",
    "硬币盒",
    "探测器",
    "低级的钓竿",
    "中级钓竿",
    "高级钓竿",
    "船票",
    "选美赛通行证",
    "未知",
    "皮皮鲸洒水壶",
    "德邦的行李箱",
    "火山灰收集袋",
    "地道的钥匙",
    "跃进自行车",
    "美容糖盒",
    "给戴戈的信",
    "梦幻船票",
    "红色之玉",
    "蓝色之玉",
    "探知机",
    "Go-Go护眼罩",
    "陨石",
    "１号房的钥匙",
    "２号房的钥匙",
    "４号房的钥匙",
    "６号房的钥匙",
    "仓库的钥匙",
    "躯干的化石",
    "爪子的化石",
    "德邦观测镜    【9区无这个道具的准确名字】",
    "技能机器０１  格斗　气合拳　150　20pp",
    "技能机器０２  龙　　龙之爪　80　15pp",
    "技能机器０３  水　　水之波动　60　20pp",
    "技能机器０４  超能　瞑想　-　20pp",
    "技能机器０５  普通　吼叫　-　20pp",
    "技能机器０６  毒　　剧毒　-　10pp",
    "技能机器０７  冰　　冰雹　-　10pp",
    "技能机器０８  格斗　巨大化　-　20pp",
    "技能机器０９  草　　种子机枪　10　30pp",
    "技能机器１０  普通　觉醒力量　-　15pp",
    "技能机器１１  火　　日本晴　-　5pp",
    "技能机器１２  恶　　挑拨　-　20pp",
    "技能机器１３  冰　　冷冻光线　95　10pp",
    "技能机器１４  冰　　暴风雪　120　5pp",
    "技能机器１５  普通　破坏光线　150　5pp",
    "技能机器１６  超能　光之壁　-　30pp",
    "技能机器１７  普通　守护　-　10pp",
    "技能机器１８  水　　祈雨　-　5pp",
    "技能机器１９  草　　亿万威力吸取　60　5pp",
    "技能机器２０  普通　神秘的守护　-　25pp",
    "技能机器２１  普通　撒气　-　20pp",
    "技能机器２２  草　　太阳光线　120　10pp",
    "技能机器２３  钢　　钢之尾　100　15pp",
    "技能机器２４  电　　十万伏特　95　15pp",
    "技能机器２５  电　　闪电　120　10pp",
    "技能机器２６  地面　地震　100　10pp",
    "技能机器２７  普通　报恩　-　20pp",
    "技能机器２８  地面　挖洞　60　10pp",
    "技能机器２９  超能　精神干扰　90　10pp",
    "技能机器３０  幽灵　影子球　80　15pp",
    "技能机器３１  格斗　瓦割　75　15pp",
    "技能机器３２  普通　影分身　-　15pp",
    "技能机器３３  超能　反射盾　-　20pp",
    "技能机器３４  电　　电击波　60　20pp",
    "技能机器３５  火　　火炎放射　95　15pp",
    "技能机器３６  毒　　泥爆弹　90　10pp",
    "技能机器３７  岩石　沙尘暴　-　10pp",
    "技能机器３８  火　　大字火　120　5pp",
    "技能机器３９  岩石　岩石封杀　50　10pp",
    "技能机器４０  飞行　燕返　60　20pp",
    "技能机器４１  恶　　寻衅　-　15pp",
    "技能机器４２  普通　空元气　70　20pp",
    "技能机器４３  普通　秘密力量　70　20pp",
    "技能机器４４  超能　睡眠　-　10pp",
    "技能机器４５  普通　着迷　-　15pp",
    "技能机器４６  恶　　盗窃　40　10pp",
    "技能机器４７  钢　　钢之翼　70　25pp",
    "技能机器４８  超能　特性交换　-　10pp",
    "技能机器４９  恶　　强夺　-　10pp",
    "技能机器５０  火　　燃烧殆尽　140　5pp",
    "秘传机器０１  普通　居合切　50　30pp",
    "秘传机器０２  飞行　飞空　70　15pp",
    "秘传机器０３  水　　冲浪　95　15pp",
    "秘传机器０４  普通　怪力　80　15pp",
    "秘传机器０５  普通　闪光　-　20pp",
    "秘传机器０６  格斗　岩碎　20　15pp",
    "秘传机器０７  水　　攀瀑　80　15pp",
    "秘传机器０８  水　　潜水　60　10pp",
    "未知",
    "未知",
    "待送物品 与火叶通信物品",
    "宠物笛子",
    "神秘的钥匙",
    "自行车兑换券",
    "金假牙",
    "神秘的琥珀",
    "刷卡钥匙",
    "电梯的钥匙",
    "海之化石",
    "甲贝化石",
    "喜禄福的观测镜",
    "自行车",
    "城镇地图",
    "战斗感知器",
    "录音机",
    "遗传机器箱",
    "树果袋",
    "教程电视机",
    "一二三岛的通行证",
    "彩虹通行证",
    "茶",
    "神秘的船票",
    "诞生岛的船票",
    "树果粉的瓶子",
    "红宝石",
    "蓝宝石",
    "熔岩团之证",
    "古代海图",
)

POKEMONS = (
    "无",
    "妙娃种子",
    "妙娃草",
    "妙娃花",
    "小火龙",
    "火恐龙",
    "喷火龙",
    "杰尼龟",
    "卡咪龟",
    "水箭龟",
    "绿毛虫",
    "铁甲蛹",
    "巴大蝴",
    "独角虫",
    "铁壳蛹",
    "大针蜂",
    "波波",
    "比比鸟",
    "比雕",
    "小拉达",
    "拉达",
    "鬼雀",
    "大嘴雀",
    "阿柏蛇",
    "阿柏怪",
    "皮卡丘",
    "雷丘",
    "穿山鼠",
    "穿山王",
    "尼多兰♀",
    "尼多丽娜",
    "尼多后",
    "尼多郎♂",
    "尼多力诺",
    "尼多王",
    "皮皮",
    "皮可斯",
    "六尾",
    "九尾",
    "胖丁",
    "胖可丁",
    "超音蝠",
    "大嘴蝠",
    "走路草",
    "臭臭花",
    "霸王花",
    "蘑菇虫",
    "巨菇虫",
    "毛球",
    "末入蛾",
    "地鼠",
    "三地鼠",
    "喵喵",
    "猫老大",
    "可达鸭",
    "哥达鸭",
    "猴怪",
    "火爆猴",
    "卡蒂狗",
    "风速狗",
    "蚊香蝌蚪",
    "蚊香蛙",
    "大力蛙",
    "卡斯",
    "勇吉拉",
    "胡地",
    "腕力",
    "豪力",
    "怪力",
    "喇叭花",
    "口呆花",
    "大食花",
    "玛瑙水母",
    "毒刺水母",
    "小拳石",
    "隆隆石",
    "隆隆岩",
    "小火马",
    "烈焰马",
    "呆呆兽",
    "呆河马",
    "小磁怪",
    "三磁怪",
    "大葱鸭",
    "多多",
    "多多利",
    "小海狮",
    "白海狮",
    "臭泥",
    "臭臭泥",
    "大舌贝",
    "铁甲贝",
    "鬼斯",
    "鬼斯通",
    "耿鬼",
    "大岩蛇",
    "食梦兽",
    "催眠兽",
    "大钳蟹",
    "巨钳蟹",
    "雷电球",
    "雷霆球",
    "蛋蛋",
    "椰蛋树",
    "卡拉卡拉",
    "嘎拉嘎拉",
    "沙瓦郎",
    "艾比郎",
    "大舌头",
    "瓦斯弹",
    "双弹瓦斯",
    "铁甲犀牛",
    "铁甲暴龙",
    "吉利蛋",
    "蔓藤怪",
    "袋龙",
    "墨海马",
    "海刺龙",
    "角金鱼",
    "金鱼王",
    "海星",
    "宝石海星",
    "魔偶",
    "飞天螳螂",
    "迷唇姐",
    "电击兽",
    "鸭嘴火龙",
    "钳刀甲虫",
    "肯泰罗",
    "鲤鱼王",
    "暴鲤龙",
    "乘龙",
    "百变怪",
    "伊布",
    "水伊布",
    "雷伊布",
    "火伊布",
    "3D龙",
    "菊石兽",
    "多刺菊石兽",
    "万年虫",
    "镰刀虫",
    "化石翼龙",
    "卡比兽",
    "急冻鸟",
    "闪电鸟",
    "火焰鸟",
    "迷你龙",
    "哈克龙",
    "快龙",
    "超梦",
    "梦幻",
    "菊草叶",
    "月桂叶",
    "大菊花",
    "火球鼠",
    "岩浆鼠",
    "暴焰兽",
    "小锯鳄",
    "蓝鳄",
    "大力鳄",
    "尾立",
    "大尾立",
    "小猫头鹰",
    "猫头鹰",
    "金龟虫",
    "昆虫战士",
    "独角蛛",
    "大角蛛",
    "叉字蝠",
    "电灯鱼",
    "大电灯鱼",
    "皮丘",
    "小皮皮",
    "小胖丁",
    "刺头蛋",
    "刺头鸟",
    "天然雀",
    "天然鸟",
    "电绵羊",
    "电气羊",
    "电气龙",
    "美丽花",
    "水鼠",
    "大水鼠",
    "伪装树",
    "大水蛙",
    "毽子草",
    "毽子花",
    "毽子棉",
    "强尾猴",
    "向日种子",
    "向日葵花",
    "花羽蜓",
    "乌波",
    "沼王",
    "光依布",
    "暗依布",
    "暗乌鸦",
    "呆呆兽王",
    "梦妖",
    "未知图腾",
    "果然翁",
    "双头长颈鹿",
    "松果兽",
    "核果兽",
    "土龙",
    "蝎子蝠",
    "钢岩蛇",
    "布鲁",
    "布鲁皇",
    "河豚",
    "钢甲螳螂",
    "壶壶龟",
    "独角仙",
    "狃拉",
    "姬熊",
    "圈圈熊",
    "小蜗牛",
    "熔岩蜗牛",
    "小猪怪",
    "长毛猪",
    "太阳珊瑚",
    "怪蛙鱼",
    "章鱼",
    "企鹅",
    "飞鱼怪",
    "钢鸟",
    "暗犬",
    "地狱犬",
    "海马龙",
    "短脚象",
    "轮子象",
    "3D龙2",
    "惊角鹿",
    "图图犬",
    "巴尔郎",
    "卡波郎",
    "迷唇娃",
    "小电击兽",
    "小鸭嘴火龙",
    "奶牛",
    "幸福蛋",
    "雷皇",
    "炎帝",
    "水君",
    "幼甲兽",
    "蛹甲兽",
    "巨大甲兽",
    "路基亚",
    "凤凰",
    "雪拉比",
    "树蜥蜴",
    "森林蜥蜴",
    "蜥蜴王",
    "小火鸡",
    "斗火鸡",
    "火鸡战士",
    "小水狗",
    "水狗",
    "水狗王",
    "皮皮犬",
    "黑毛犬",
    "针鼠",
    "大飞鼠",
    "红毛虫",
    "小白蛹",
    "黄蝶",
    "小粉蛹",
    "毒蛾",
    "顶叶兽",
    "顶叶童",
    "乐天河童",
    "橡实果",
    "长鼻叶",
    "铁扇天狗",
    "钻地虫",
    "风速蝉",
    "鬼蝉",
    "麻燕",
    "大麻燕",
    "木果兽",
    "木生兽",
    "晕眩熊",
    "海鸥",
    "大嘴鹈鹕",
    "水蛛怪",
    "巨蛛怪",
    "皮皮鲸",
    "鲸鱼王",
    "小松鼠",
    "大松鼠",
    "变色龙",
    "土偶",
    "三土偶",
    "磁石怪",
    "熔岩乌龟",
    "地狱超人",
    "泥鳅",
    "龙鳅",
    "心形鱼",
    "奇亚蟹",
    "大利蟹",
    "丑丑鱼",
    "美丽龙",
    "三色鲨",
    "鲨鱼王",
    "大头怪",
    "小蜻蜓龙",
    "蜻蜓龙",
    "拳击兔",
    "相扑熊",
    "电气兽",
    "雷电兽",
    "喷火驼",
    "双峰喷火驼",
    "海象球",
    "大海象",
    "海象王",
    "仙人球",
    "恶魔仙人掌",
    "小头冰怪",
    "巨头冰怪",
    "月亮石",
    "太阳石",
    "小水鼠",
    "弹簧猪",
    "飞天猪",
    "正电兔",
    "负电兔",
    "巨嘴娃",
    "冥思兽",
    "佳雷木",
    "云雀",
    "大云雀",
    "果然宝宝",
    "钻墙鬼",
    "独眼鬼",
    "芭蕾玫瑰",
    "小懒猴",
    "狂猴",
    "大猩猩",
    "毒布丁",
    "毒布丁王",
    "香蕉飞龙",
    "音波兔",
    "噪音怪",
    "噪音王",
    "海贝",
    "大嘴鳗",
    "长睫鳗",
    "灾兽",
    "小失眠鬼",
    "失眠鬼",
    "钢尾蛇",
    "斩猫",
    "化石鱼",
    "钢甲虫",
    "钢甲犀牛",
    "钢甲暴龙",
    "天气怪",
    "母萤火虫",
    "公萤火虫",
    "化石花",
    "化石巨花",
    "化石蝎",
    "化石巨蝎",
    "感知兽",
    "神知兽",
    "圣护兽",
    "宝贝龙",
    "甲壳龙",
    "血翼飞龙",
    "铁哑铃",
    "金属怪",
    "钢螃蟹",
    "岩神柱",
    "冰神柱",
    "钢神柱",
    "海皇牙",
    "古拉顿",
    "烈空龙",
    "红水都",
    "蓝水都",
    "基拉祈",
    "迪奥西斯",
    "风铃子",
)