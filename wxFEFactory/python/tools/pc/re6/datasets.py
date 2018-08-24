from lib.hack.utils import OptionProvider


PERSONS = ('里昂', '海伦娜', '克里斯', '皮尔斯', '杰克', '雪莉', '艾达', '特工')


CHAR_CLOTH_LIST = OptionProvider((
    ('里昂 (美国)', 0x0000),
    ('里昂 (亚洲)', 0x0100),
    ('里昂 (服装 1)', 0x1000),
    ('里昂 (服装 2)', 0x1100),
    ('里昂 (复古)', 0x1200),
    ('海伦娜 (美国)', 0x0001),
    ('海伦娜 (亚洲)', 0x0101),
    ('海伦娜 (黛博拉)', 0x0201),
    ('海伦娜 (服装 1)', 0x1001),
    ('海伦娜 (服装 2)', 0x1101),
    ('海伦娜 (复古)', 0x1201),
    ('克里斯 (亚洲)', 0x0002),
    ('克里斯 (欧洲)', 0x0102),
    ('克里斯 (便服)', 0x0202),
    ('克里斯 (服装 1)', 0x1002),
    ('克里斯 (服装 2)', 0x1102),
    ('克里斯 (复古)', 0x1202),
    ('皮尔斯 (亚洲)', 0x0003),
    ('皮尔斯 (欧洲)', 0x0103),
    ('皮尔斯 (便服)', 0x0203),
    ('皮尔斯 (突变)', 0x0303),
    ('皮尔斯 (服装 1)', 0x1003),
    ('皮尔斯 (服装 2)', 0x1103),
    ('皮尔斯 (复古)', 0x1203),
    ('杰克 (欧洲)', 0x0004),
    ('杰克 (拘留)', 0x0104),
    ('杰克 (亚洲)', 0x0204),
    ('杰克 (雪地)', 0x0304),
    ('杰克 (服装 1)', 0x1004),
    ('杰克 (服装 2)', 0x1104),
    ('杰克 (复古)', 0x1204),
    ('雪莉 (欧洲)', 0x0005),
    ('雪莉 (拘留)', 0x0105),
    ('雪莉 (亚洲)', 0x0205),
    ('雪莉 (雪地)', 0x0305),
    ('雪莉 (服装 1)', 0x1005),
    ('雪莉 (服装 2)', 0x1105),
    ('雪莉 (复古)', 0x1205),
    ('艾达 (正常)', 0x0006),
    ('艾达 (赤裸?)', 0x0106),
    ('艾达 (卡拉)', 0x0206),
    ('艾达 (服装 1)', 0x1006),
    ('艾达 (服装 2)', 0x1106),
    ('艾达 (复古)', 0x1206),
    ('特工', 0x0007),
    ('BSAA新兵', 0x0207),
    ('尼克 (L4D2)', 0x1300),
    ('教练 (L4D2)', 0x1302),
    ('艾利斯 (L4D2)', 0x1303),
    ('萝雪儿 (L4D2)', 0x1305),
))

INVENTORY_ITEMS = OptionProvider((
    ('无', 0x0000),
    ('徒手', 0x0100),
    ('"909"半自动手枪', 0x0101),
    ('"皮卡多"半自动手枪', 0x0102),
    ('"飞翼"半自动双枪', 0x0103),
    ('霰弹枪', 0x0104),
    ('突击霰弹枪', 0x0105),
    ('九头蛇', 0x0106),
    ('"沙漠之鹰"半自动手枪', 0x0107),
    ('"弑象者"左轮手枪', 0x0108),
    ('狙击步枪', 0x0109),
    ('半自动狙击步枪', 0x010A),
    ('反器材狙击步枪', 0x010B),
    ('弹药箱50', 0x010C),
    ('三连射', 0x010D),
    ('MP-AF', 0x010E),
    ('特殊战术突击步枪', 0x010F),
    ('"暴熊"榴弹突击步枪', 0x0110),
    ('突击步枪RN', 0x0111),
    ('榴弹发射器', 0x0112),
    ('手榴弹', 0x0113),
    ('燃烧弹', 0x0114),
    ('闪光弹', 0x0115),
    ('远程炸弹', 0x0116),
    ('十字弓', 0x0117),
    ('救生刀', 0x0118),
    ('战斗刀', 0x0119),
    ('电击棒', 0x011A),
    ('火箭筒', 0x011B),
    ('炮塔', 0x011C),
    ('生命药片', 0x011D),
    ('炮塔', 0x011E),
    ('通讯器', 0x011F),
    ('急救喷雾', 0x0120),
    ('炮塔', 0x0121),
    ('VTOL飞弹', 0x0122),
    ('VTOL机关枪', 0x0123),
    ('艾达的直昇机飞弹', 0x0124),
    ('艾达的直昇机机关枪', 0x0125),
    ('突变之手', 0x0126),
    ('黛博拉', 0x0127),
    ('9毫米口径弹药', 0x0201),
    ('12口径弹壳', 0x0202),
    ('7.62毫米口径北约弹药', 0x0203),
    ('5.56毫米口径北约弹药', 0x0204),
    ('12.7mm 弹药', 0x0205),
    ('.50 AE 麦林弹药', 0x0206),
    ('.500 S&W 麦林弹药', 0x0207),
    ('40mm 爆炸弹', 0x0208),
    ('40mm 硫酸弹', 0x0209),
    ('40mm 冷冻弹', 0x020A),
    ('73mm 爆炸火箭', 0x020B),
    ('弓箭 (正常)', 0x020C),
    ('弓箭 (管炸弹)', 0x020D),
    ('10口径弹壳', 0x020E),
    ('药草 (绿)', 0x0301),
    ('药草 (红)', 0x0302),
    ('药草 (绿)', 0x0303),
    ('药草 (红)', 0x0304),
    ('药草 (绿+绿)', 0x0305),
    ('药草 (绿+红)', 0x0306),
    ('药草 (绿+绿+绿)', 0x0307),
))

SKILLS = (
    '无',
    '枪支 Lv. 1',
    '枪支 Lv. 2',
    '枪支 Lv. 3',
    '体术 Lv. 1',
    '体术 Lv. 2',
    '体术 Lv. 3',
    '防御 Lv. 1',
    '防御 Lv. 2',
    '防御 Lv. 3',
    '爆头 Lv. 1',
    '爆头 Lv. 2',
    '爆头 Lv. 3',
    '穿透 Lv. 1',
    '穿透 Lv. 2',
    '穿透 Lv. 3',
    '吉瓦弗杀手 Lv. 1',
    '吉瓦弗杀手 Lv. 2',
    '殭尸猎人 Lv. 1',
    '殭尸猎人 Lv. 2',
    '榴弹增强',
    '手枪能手',
    '散弹枪能手',
    '麦林能手',
    '狙击枪能手',
    '机关枪能手',
    '突击步枪能手',
    '榴弹发射器能手',
    '十字弓能手',
    '无限手枪',
    '无限散弹枪',
    '无限麦林',
    '无限狙击枪',
    '无限机关枪',
    '无限突击步枪',
    '无限榴弹发射器',
    '无限十字弓',
    '手枪弹药拾获加增',
    '散弹枪弹壳拾获加增',
    '麦林弹药拾获加增',
    '步枪弹药拾获加增',
    '榴弹拾获加增',
    '弓箭拾获加增',
    '最后一击',
    '无声行动',
    '快速装弹',
    '锁定 Lv. 1',
    '锁定 Lv. 2',
    '稳固 Lv. 1',
    '稳固 Lv. 2',
    '突围',
    '道具落下加增',
    '回复 Lv. 1',
    '回复 Lv. 2',
    '格斗值加增 Lv. 1',
    '格斗值加增 Lv. 2',
    '鹰眼',
    '组队',
    '实地军医 Lv. 1',
    '实地军医 Lv. 2',
    '独行者',
    '无准星射击',
    '打破吧！',
    '时间奖励 +',
    '连击奖励 +',
    '破限者',
    '闪电战戏',
    '速射伤害加增',
    '力量反击',
    '绝地反击',
    '武术能手',
    '射击能手',
    '最后抵抗',
    '报复',
    '先发制人',
    '持枪者',
    '奄奄一息',
    '制药者',
    '军医',
    '第一回应者',
    '别紧张',
    '自然痊癒',
    '怪物点数增强',
    '怪物点数加增',
    '训练',
    '怪物攻击 LV. 1',
    '怪物攻击 LV. 2',
    '怪物攻击 LV. 3',
    '怪物防御 LV. 1',
    '怪物防御 LV. 2',
    '怪物防御 LV. 3',
    '怪物生命 LV. 1',
    '怪物生命 LV. 2',
    '怪物生命 LV. 3',
    '怪物耐力 LV. 1',
    '怪物耐力 LV. 2',
    '怪物耐力 LV. 3',
)

MELEE_SKILLS = OptionProvider((
    ('电击棒正常攻击 1 (快速攻击)', 0x010B),
    ('电击棒正常攻击 2', 0x010C),
    ('电击棒正常攻击 3', 0x010D),
    ('电击棒正常攻击 4', 0x010F),
    ('电击棒储满攻击 1', 0x0110),
    ('电击棒储满攻击 2', 0x0112),
    ('电击棒储满攻击 3', 0x0113),
    ('赤手空拳储满攻击 1', 0x0151),
    ('赤手空拳储满攻击 2', 0x0152),
    ('赤手空拳储满攻击 3 (快速攻击)', 0x0153),
    ('赤手空拳储满攻击 4', 0x0154),
    ('赤手空拳储满攻击 5', 0x0155),
    ('赤手空拳储满攻击 6', 0x0156),
    ('赤手空拳储满攻击 7', 0x0157),
    ('赤手空拳储满攻击 8', 0x0158),
    ('赤手空拳储满攻击 9', 0x0159),
    ('赤手空拳储满攻击 10', 0x015A),
    ('赤手空拳正常攻击 1', 0x015B),
    ('赤手空拳正常攻击 2', 0x015C),
    ('赤手空拳正常攻击 3', 0x015D),
    ('360度旋风腿', 0x015E),
    ('杰克预设体术 1', 0x015F),
    ('杰克预设体术 2', 0x0160),
    ('克里斯预设体术 1', 0x0169),
    ('克里斯预设体术 2', 0x016A),
    ('反手攻击', 0x016B),
    ('最终攻击（海伦娜的视角）', 0x016C),
    ('最终攻击（里昂的视角）', 0x016D),
    ('最终攻击（艾达的视角）', 0x016E),
    ('最终攻击（克里斯的视角）', 0x016F),
    ('最终攻击（杰克的视角）', 0x0170),
    ('最终攻击（雪莉的视角）', 0x0171),
    ('皮尔斯／特工预设体术 1', 0x0172),
    ('皮尔斯／特工预设体术 2', 0x0173),
    ('踢 + 360度旋转', 0x0174),
    ('海伦娜／艾达预设体术 1', 0x0175),
    ('雪莉预设体术 1', 0x0176),
    ('雪莉预设体术 2', 0x0177),
    ('海伦娜／艾达预设体术 2', 0x0178),
    ('720度旋风腿', 0x0179),
    ('长型武器体术 1', 0x017A),
    ('长型武器体术 2', 0x017B),
    ('长型武器刺入', 0x017C),
    ('里昂预设体术 1', 0x017D),
    ('里昂预设体术 2', 0x017E),
    ('大型武器体术 1', 0x017F),
    ('大型武器体术 2', 0x0180),
    ('最终攻击（皮尔斯的视角）', 0x0181),
    ('360度踢', 0x0182),
    ('冲刺体术', 0x0183),
    ('最终攻击（特工的视角）', 0x0184),
    ('男性背向体术', 0x0185),
    ('女性背向体术', 0x0186),
    ('筋疲力竭的体术', 0x0187),
    ('爬行体术', 0x0188),
    ('闪躲 + 肘击', 0x0189),
    ('闪躲 + 撞击', 0x018A),
    ('闪躲 + 猛击', 0x018B),
    ('地面踢', 0x018C),
    ('反击 - 肘击', 0x018D),
    ('反击 - 背向踢', 0x018E),
    ('反击 - 地面360度踢', 0x018F),
    ('反击 - 360度踢', 0x0190),
    ('反击 - 手枪猛击', 0x0191),
    ('反击 - 大型武器猛击', 0x0192),
    ('地面体术 - 跺脚', 0x0193),
    ('地面体术 - 大型武器 1', 0x0194),
    ('地面体术 - 大型武器 2', 0x0195),
    ('地面体术 - 大型武器 3', 0x0197),
    ('打破箱子 - 手枪', 0x0198),
    ('打破箱子 - 大型武器', 0x0199),
    ('打破箱子 - 踢', 0x019A),
))
