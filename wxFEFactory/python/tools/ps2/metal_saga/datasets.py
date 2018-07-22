from lib.hack.utils import ItemProvider


PERSONS = ('主角', '基里亚', '米卡', '拉希德', '夏莉', '阿尔法', 'Shiba', 'Tosa', 'Terry', 'Bernie')
CHARIOTS = tuple('战车%d' % i for i in range(1, 9))


TITLES = (
    "菜鸟",
    "终于够格的人",
    "资深猎人",
    "精英猎人",
    "无敌之男",
    "战斗狂",
    "大富翁",
    "武器狂",
    "战车狂",
    "道具收集狂",
    "败家子",
    "传说之猎人",
    "巴特的挚友",
    "奥林匹亚先生",
    "舞者",
    "玩家",
    "后宫之主",
    "活在爱中的人",
    "妹控",
    "恋母君",
    "牵引专业户",
    "勇者",
    "购物狂",
    "幸运儿",
    "赌神",
    "屠夫",
    "垃圾回收者",
    "顶级饲养员",
    "沙门氏菌猿杀手",
    "租借王",
    "废柴",
    "巴特真正的朋友",
    "镜片之友",
    "放荡儿子",
    "用扳手的人",
    "机械的朋友",
    "战车技师",
    "坦克医生",
    "铁之魔术师",
    "神技修理师",
    "见习修理生",
    "美眉机械师",
    "旅行剑士",
    "钢之保镖",
    "沙漠武士",
    "沙漠将军",
    "剑圣",
    "无敌保镖",
    "火箭炮少女",
    "导弹女士",
    "枪手",
    "不死身之女",
    "最终兵器",
    "胭脂旗",
    "谜之少女",
)

ITEMS = (
    "空", # 0000
    # 人类装备
    "蝴蝶刀", # 0001
    "金属棒", # 0002
    "双刃弯刀", # 0003
    "大砍刀", # 0004
    "虎爪", # 0005
    "青龙刀", # 0006
    "波斯长刀", # 0007
    "绯牡丹匕首", # 0008
    "锡兰弯刀", # 0009
    "无铭刀", # 000A
    "Keen Edge", # 000B
    "高速振动剑", # 000C
    "大马士革剑", # 000D
    "野太刀", # 000E
    "两头剑", # 000F
    "拳刃", # 0000
    "破甲刀", # 0011
    "双鬼丸", # 0012
    "徒手", # 0013
    "粉碎棒", # 0014
    "喷射军刀", # 0015
    "蓝月刀", # 0016
    "和泉守兼定", # 0017
    "德林格手枪", # 0018
    "电击警棍", # 0019
    "崛川国広", # 001A
    "晶体军刀1", # 001B
    "晶体军刀2", # 001C
    "晶体军刀3", # 001D
    "晶体军刀4", # 001E
    "晶体军刀5", # 001F
    "晶体军刀6", # 0020
    "晶体军刀7", # 0021
    "钻头爪", # 0022
    "光束爪", # 0023
    "爆弹爪", # 0024
    "降魔刀", # 0025
    "真·降魔刀", # 0026
    "钢珠弹弓", # 0027
    "左轮手枪", # 0028
    "PPK", # 0029
    "弩枪", # 002A
    "柯尔特左轮", # 002B
    "贝瑞塔", # 002C
    "UDAR", # 002D
    "火箭飞拳", # 002E
    "沙漠之鹰", # 002F
    "吉布森霰弹枪", # 0030
    "SVD狙击枪", # 0031
    "霰弹枪", # 0032
    "乌兹冲锋枪", # 0033
    "PPsh41", # 0034
    "AK47", # 0035
    "汤普森冲锋枪", # 0036
    "榴弹枪", # 0037
    "微型火神炮", # 0038
    "回旋扳手", # 0039
    "飞刀", # 003A
    "遥控扳手", # 003B
    "烈风手枪", # 003C
    "G3A3", # 003D
    "TNT偏执狂", # 003E
    "铆钉枪", # 003F
    "Pzb39·改", # 0040
    "终极风暴枪", # 0041
    "毒刺飞弹", # 0042
    "声纳枪", # 0043
    "火焰枪", # 0044
    "烈焰炮", # 0045
    "硝酸连射枪", # 0046
    "电气枪", # 0047
    "冷冻枪", # 0048
    "暴雪光束", # 0049
    "徒手", # 004A
    "水泥枪", # 004B
    "龙息枪", # 004C
    "镭射炮1", # 004D
    "镭射炮2", # 004E
    "镭射炮3", # 004F
    "镭射炮4", # 0050
    "镭射炮5", # 0051
    "镭射炮6", # 0052
    "镭射炮7", # 0053
    "USP", # 0054
    "AutoMag", # 0055
    "英格拉姆冲锋枪", # 0056
    "P90", # 0057
    "犬用枪", # 0058
    "犬用火神炮", # 0059
    "犬用加农炮", # 005A
    "犬用反坦克导弹", # 005B
    "犬用激光枪", # 005C
    "犬用声纳枪", # 005D
    "犬用火焰喷射器", # 005E
    "犬用雷电枪", # 005F
    "犬用暴雪炮", # 0060
    "犬用臼炮", # 0061
    "犬用飞翼", # 0062
    "犬用火箭炮", # 0063
    "作业帽", # 0064
    "迷彩帽", # 0065
    "头套", # 0066
    "护目镜头盔", # 0067
    "埃及头巾", # 0068
    "软礼帽", # 0069
    "牛仔帽", # 006A
    "缠头巾", # 006B
    "奔尼帽", # 006C
    "曲棍球面具", # 006D
    "安全头盔", # 006E
    "防弹假发", # 006F
    "芳纶纤维头巾", # 0070
    "CVC头盔", # 0071
    "人造纤维头盔", # 0072
    "阿里巴巴头巾", # 0073
    "凯撒冠", # 0074
    "猫耳头饰", # 0075
    "兔女郎帽", # 0076
    "牛仔衣", # 0077
    "迷彩服", # 0078
    "飞行茄克", # 0079
    "皮夹克", # 007A
    "防弹花衬衫", # 007B
    "消防服", # 007C
    "长风衣", # 007D
    "骑手套装", # 007E
    "BDU茄克", # 007F
    "绯牡丹便装", # 0080
    "军用雨衣", # 0081
    "高能聚合衣", # 0082
    "金属套装", # 0083
    "高温作业服", # 0084
    "医疗套装", # 0085
    "萨拉托加套装", # 0086
    "CVC护甲", # 0087
    "萨拉托加护甲", # 0088
    "突击甲", # 0089
    "阿里巴巴背心", # 008A
    "圣痕麻衣", # 008B
    "防弹旗袍", # 008C
    "高叉护甲", # 008D
    "女仆服", # 008E
    "铁胸衣", # 008F
    "手套", # 0090
    "皮手套", # 0091
    "铁指虎", # 0092
    "重金属手套", # 0093
    "战斗铁莲花", # 0094
    "铁手套", # 0095
    "扳机臂套", # 0096
    "CVC手套", # 0097
    "力量手套", # 0098
    "机械师手套", # 0099
    "分趾鞋", # 009A
    "运动鞋", # 009B
    "休闲靴", # 009C
    "安全靴", # 009D
    "西式长靴", # 009E
    "战斗钉鞋", # 009F
    "金属护胫", # 00A0
    "绯牡丹木展", # 00A1
    "CVC长靴", # 00A2
    "包钢长靴", # 00A3
    "军用护胫", # 00A4
    "犬用战甲LV1", # 00A5
    "犬用战甲LV2", # 00A6
    "犬用战甲LV3", # 00A7
    "犬用战甲LV4", # 00A8
    "犬用战甲LV5", # 00A9
    "犬用战甲LV6", # 00AA
    "犬用战甲LV7", # 00AB
    "犬用战甲LV8", # 00AC
    "犬用战甲LV9", # 00AD
    "防护贴条", # 00AE
    "炉盖", # 00AF
    "绯牡丹腰带", # 00B0
    "防弹背心", # 00B1
    "硅胶护垫", # 00B2
    "陶瓷护垫", # 00B3
    "护体挡板", # 00B4
    "晶体护盾", # 00B5
    "缓冲护甲", # 00B6
    "APP背心", # 00B7
    "镜铠", # 00B8
    "滤音护甲", # 00B9
    "耐火护甲", # 00BA
    "避雷护甲", # 00BB
    "防寒护甲", # 00BC
    "犬用护甲", # 00BD
    "废甲", # 00BE

    # 坦克装备
    "37mm炮", # 00BF
    "50mm炮", # 00C0
    "75mm炮S", # 00C1
    "75mm炮L", # 00C2
    "88mm炮", # 00C3
    "76mmT型炮", # 00C4
    "90mmT型炮", # 00C5
    "105mm线膛炮", # 00C6
    "120mm线膛炮", # 00C7
    "92mm火花炮", # 00C8
    "160mm火花炮", # 00C9
    "120mm滑膛炮", # 00CA
    "140mm滑膛炮", # 00CB
    "177mm无常炮", # 00CC
    "205mm加农炮", # 00CD
    "205mm绯牡丹", # 00CE
    "220mm盖亚炮", # 00CF
    "225mm九头蛇炮", # 00D0
    "轨道加农炮", # 00D1
    "180mm连射炮", # 00D2
    "190mm连射炮", # 00D3
    "三发连射炮", # 00D4
    "165mm幽灵炮", # 00D5
    "雷电加农炮", # 00D6
    "等离子加农炮", # 00D7
    "20mm机关炮", # 00D8
    "25mm机关炮", # 00D9
    "30mm机关炮", # 00DA
    "35mm机关炮", # 00DB
    "57mm机关炮", # 00DC
    "7.62mm机关枪", # 00DD
    "9mm火神炮", # 00DE
    "9mm机关枪", # 00DF
    "12.7mm火神炮", # 00E0
    "12.7mm机关枪", # 00E1
    "20mm火神炮", # 00E2
    "20mm机关枪", # 00E3
    "30mm火神炮", # 00E4
    "30mm机关枪", # 00E5
    "35mm火神炮", # 00E6
    "35mm机关枪", # 00E7
    "绯牡丹火神炮", # 00E8
    "火焰喷射器", # 00E9
    "火龙", # 00EA
    "雷电连射炮", # 00EB
    "雷暴机关炮", # 00EC
    "冲锋号机枪", # 00ED
    "破坏笛机枪", # 00EE
    "光束爆发枪", # 00EF
    "扫射激光枪", # 00F0
    "蛇头激光枪", # 00F1
    "榴弹投射器", # 00F2
    "踢踏舞者炮", # 00F3
    "IM脏躁炮", # 00F4
    "AT导弹", # 00F5
    "寻血猎狗式", # 00F6
    "拍击者", # 00F7
    "蒸馏器", # 00F8
    "凝固汽油炮", # 00F9
    "狂厨式", # 00FA
    "TNT榴弹炮", # 00FB
    "钻头导弹", # 00FC
    "日炙弹XX", # 00FD
    "高音粒子弹", # 00FE
    "气旋加农炮", # 00FF
    "CIWS", # 0100
    "RAM", # 0101
    "剑舞式", # 0102
    "北风式", # 0103
    "摇滚式", # 0104
    "贯雷枪式", # 0105
    "露雳领域式", # 0106
    "汀达罗斯式", # 0107
    "削钢剑式", # 0108
    "ATM绯牡丹", # 0109
    "越野车", # 010A
    "德马格", # 010B
    "蚊式", # 010C
    "野巴士", # 010D
    "旋风(对空)", # 010E
    "突击炮", # 010F
    "巴巴罗萨", # 0110
    "消防车", # 0111
    "虎式", # 0112
    "罗西纳", # 0113
    "伏尔甘", # 0114
    "猎豹(对空)", # 0115
    "梅卡瓦", # 0116
    "露露贝尔", # 0117
    "隆美尔", # 0118
    "艾布兰", # 0119
    "零式", # 011A
    "豹式", # 011B
    "鼠式", # 011C
    "猎杀者号", # 011D
    "虎王式", # 011E
    "黑豹式G", # 011F
    "士魂号（74式）", # 0120
    "出租战车1号", # 0121
    "出租战车2号", # 0122
    "出租战车3号", # 0123
    "出租战车4号", # 0124
    "出租战车5号", # 0125
    "出租战车6号", # 0126
    "出租战车7号", # 0127
    "出租战车8号", # 0128
    "出租战车9号", # 0129
    "出租战车10号", # 012A
    "驴式", # 012B
    "力士式", # 012C
    "公牛式", # 012D
    "苦力式", # 012E
    "V24巨人式", # 012F
    "鲁道夫式", # 0130
    "友式", # 0131
    "OHC卡门式", # 0132
    "V48金刚式", # 0133
    "精灵式", # 0134
    "感恩II", # 0135
    "伍兹奈克SI", # 0136
    "99式神话", # 0137
    "艾米", # 0138
    "健谈者", # 0139
    "诺伊曼", # 013A
    "达洛斯", # 013B
    "所罗门2", # 013C
    "梅塔特隆", # 013D
    "西格马80", # 013E

    # 人类道具
    "回复胶囊", # 013F
    "回复饮料", # 0140
    "能量胶囊", # 0141
    "能量饮料", # 0142
    "波奇气瓶", # 0143
    "中和剂", # 0144
    "碱性喷雾", # 0145
    "麻痹散", # 0146
    "超级麻痹散", # 0147
    "瞬间怀炉", # 0148
    "兴奋剂20", # 0149
    "兴奋剂50", # 014A
    "敏捷剂20", # 014B
    "敏捷剂50", # 014C
    "主助推器", # 014D
    "汪汪美食家", # 014E
    "怀旧照片", # 014F
    "再生胶囊", # 0150
    "装甲包40", # 0151
    "装甲包80", # 0152
    "装甲包L", # 0153
    "装甲包XL", # 0154
    "装甲包XXL", # 0155
    "修理工具箱", # 0156
    "机械工具箱", # 0157
    "去污剂", # 0158
    "碱性车蜡", # 0159
    "碱性涂层", # 015A
    "隐形涂层", # 015B
    "镜面涂层", # 015C
    "再启动钥匙", # 015D
    
    # 攻击类道具
    "手榴弹", # 015E
    "APAP毒刺飞弹", # 015F
    "光子手榴弹", # 0160
    "音波手榴弹", # 0161
    "火炎瓶", # 0162
    "电击手榴弹", # 0163
    "冰冻手榴弹", # 0164
    "对空手榴弹", # 0165
    "鼹鼠手榴弹", # 0166
    "水雷手榴弹", # 0167
    "远程手榴弹", # 0168
    "飞行炸弹", # 0169
    "追踪炸弹", # 016A
    "胡桃钳", # 016B
    "手榴弹", # 016C
    "火箭烟花", # 016D
    "烟花束", # 016E
    "铅笔飞弹", # 016F
    "DDパゥD菠萝弹", # 0170
    "火箭简", # 0171
    "冷冻瓶", # 0172
    "催眠瓶", # 0173
    "恐吓瓶", # 0174
    "火炎瓶", # 0175
    "硝化甘油瓶", # 0176
    "莫洛托夫鸡尾酒", # 0177
    "浓缩甲醇", # 0178
    "电击网", # 0179

    # 卖钱用掉落道具
    "粘糊糊细胞", # 017A
    "颤巍巍细胞", # 017B
    "眼球", # 017C
    "米饭", # 017D
    "狗尾", # 017E
    "滑溜溜细胞", # 017F
    "奢侈品", # 0180
    "蚁肠", # 0181
    "安全鸡肉", # 0182
    "卷饵（暂定）", # 0183
    "蜂蜜", # 0184
    "傻", # 0185
    "鱼肉", # 0186
    "高级鱼肉", # 0187
    "章鱼爪", # 0188
    "软软的果子", # 0189
    "收获铅蘑菇", # 018A
    "神圣蛋白质", # 018B
    "冷冰冰细胞", # 018C
    "硬邦邦细胞", # 018D
    "砂金", # 018E
    "蛇尾", # 018F
    "贝壳", # 0190
    "铜条", # 0191
    "银条", # 0192
    "金条", # 0193
    "银斧", # 0194
    "金斧", # 0195

    # 其他类道具
    "古币", # 0196
    "军号", # 0197
    "圣经", # 0198
    "草莓口红", # 0199
    "松的肥皂", # 019A
    "松的拖鞋", # 019B
    "松的浴袍", # 019C
    "松的毛巾", # 019D
    "纹身贴纸", # 019E
    "妹妹的围裙", # 019F
    "妹妹的毛巾", # 01A0
    "妈妈的手帕", # 01A1
    "爸爸的衬衫", # 01A2
    "杀虫药", # 01A3
    "杀虫剂", # 01A4
    "口香糖", # 01A5
    "耳塞", # 01A6
    "防毒面具", # 01A7
    "犬用面具", # 01A8
    "兔耳", # 01A9
    "兔尾", # 01AA
    "猫耳", # 01AB
    "猫尾", # 01AC
    "接地链条", # 01AD
    "犬标签", # 01AE
    "除蚤项圈", # 01AF
    "红色头巾", # 01B0
    "迷彩头巾", # 01B1
    "易投的石块", # 01B2
    "难投的石块", # 01B3
    "微妙的石头", # 01B4
    "美丽的石头", # 01B5
    "铜战车击破章", # 01B6
    "银战车击破章", # 01B7
    "金战车击破章", # 01B8
    "铂战车击破章", # 01B9
    "果汁", # 01BA
    "BS背带", # 01BB
    "大奖章", # 01BC
    "哑铃", # 01BD
    "筋肉饮料", # 01BE
    "超级凡士林", # 01BF
    "筋肉奖章", # 01C0
    "舞者耳环", # 01C1
    "舞者项链", # 01C2
    "舞者之鞋", # 01C3
    "舞者手套", # 01C4

    # 古董品
    "禽龙", # 01C5
    "畸形禽龙", # 01C6
    "暴龙", # 01C7
    "猿人", # 01C8
    "猛犸", # 01C9
    "绳文土器", # 01CA
    "土偶", # 01CB
    "埴轮", # 01CC
    "机器人", # 01CD
    "假人", # 01CE
    
    # 核心
    "180mm连射炮核心" # 01CF
    "190mm连射炮核心", # 01D0
    "三发连射炮核心", # 01D1
    "165mm幽灵炮核心", # 01D2
    "雷电加农炮核心", # 01D3
    "等离子加农炮核心", # 01D4
    "TNT榴弹炮核心", # 01D5
    "钻头导弹核心", # 01D6
    "日炙弹XX核心", # 01D7
    "高音粒子弹核心", # 01D8
    "气旋加农炮核心", # 01D9
    "CIWS核心", # 01DA
    "RAM核心", # 01DB
    "剑舞式核心", # 01DC
    "北风式核心", # 01DD
    "摇滚式核心", # 01DE
    "贯雷枪式核心", # 01DF
    "露雳领域式核心", # 01E0
    "汀达罗斯式核心", # 01E1
    "削钢剑式核心", # 01E2
    "ATM绯牡丹核心", # 01E3
    "冲锋号机枪核心", # 01E4
    "破坏笛机枪核心", # 01E5
    "光束爆发枪核心", # 01E6
    "扫射激光枪核心", # 01E7
    "蛇头激光枪核心", # 01E8

    # LOVE机器
    "LOVE机器1111", # 01E9
    "LOVE机器1112", # 01EA
    "LOVE机器1113", # 01EB
    "LOVE机器1121", # 01EC
    "LOVE机器1122", # 01ED
    "LOVE机器1123", # 01EE
    "LOVE机器1131", # 01EF
    "LOVE机器1132", # 01F0
    "LOVE机器1133", # 01F1
    "LOVE机器1211", # 01F2
    "LOVE机器1212", # 01F3
    "LOVE机器1213", # 01F4
    "LOVE机器1221", # 01F5
    "LOVE机器1222", # 01F6
    "LOVE机器1223", # 01F7
    "LOVE机器1231", # 01F8
    "LOVE机器1232", # 01F9
    "LOVE机器1233", # 01FA
    "LOVE机器1311", # 01FB
    "LOVE机器1312", # 01FC
    "LOVE机器1313", # 01FD
    "LOVE机器1321", # 01FE
    "LOVE机器1322", # 01FF
    "LOVE机器1323", # 0200
    "LOVE机器1331", # 0201
    "LOVE机器1332", # 0202
    "LOVE机器1333", # 0203
    "LOVE机器2111", # 0204
    "LOVE机器2112", # 0205
    "LOVE机器2113", # 0206
    "LOVE机器2121", # 0207
    "LOVE机器2122", # 0208
    "LOVE机器2123", # 0209
    "LOVE机器2131", # 020A
    "LOVE机器2132", # 020B
    "LOVE机器2133", # 020C
    "LOVE机器2211", # 020D
    "LOVE机器2212", # 020E
    "LOVE机器2213", # 020F
    "LOVE机器2221", # 0210
    "LOVE机器2222", # 0211
    "LOVE机器2223", # 0212
    "LOVE机器2231", # 0213
    "LOVE机器2232", # 0214
    "LOVE机器2233", # 0215
    "LOVE机器2311", # 0216
    "LOVE机器2312", # 0217
    "LOVE机器2313", # 0218
    "LOVE机器2321", # 0219
    "LOVE机器2323", # 021A
    "LOVE机器2323", # 021B
    "LOVE机器2331", # 021C
    "LOVE机器2332", # 021D
    "LOVE机器2333", # 021E
    "LOVE机器3111", # 021F
    "LOVE机器3112", # 0220
    "LOVE机器3113", # 0221
    "LOVE机器3121", # 0222
    "LOVE机器3122", # 0223
    "LOVE机器3123", # 0224
    "LOVE机器3131", # 0225
    "LOVE机器3132", # 0226
    "LOVE机器3133", # 0227
    "LOVE机器3211", # 0228
    "LOVE机器3212", # 0229
    "LOVE机器3213", # 022A
    "LOVE机器3221", # 022B
    "LOVE机器3222", # 022C
    "LOVE机器3233", # 022D
    "LOVE机器3231", # 022E
    "LOVE机器3232", # 022F
    "LOVE机器3233", # 0230
    "LOVE机器3311", # 0231
    "LOVE机器3312", # 0232
    "LOVE机器3313", # 0233
    "LOVE机器3321", # 0234
    "LOVE机器3322", # 0235
    "LOVE机器3323", # 0236
    "LOVE机器3331", # 0237
    "LOVE机器3332", # 0238
    "LOVE机器3333", # 0239
    "L1芯片", # 023A
    "L2芯片", # 023B
    "L3芯片", # 023C
    "O1芯片", # 023D
    "O2芯片", # 023E
    "O3芯片", # 023F
    "V1芯片", # 0240
    "V2芯片", # 0241
    "V3芯片", # 0242
    "E1芯片", # 0243
    "E2芯片", # 0244
    "E3芯片", # 0245

    # 透镜
    "太阳镜", # 0246
    "宝石镜", # 0247
    "眼镜", # 0248
    "光镜", # 0249

    # 合成素材和其他东西
    "炮管", # 024A
    "导向器", # 024B
    "金属板", # 024C
    "猴眼", # 024D
    "鹰眼", # 024E
    "鼹眼", # 024F
    "鱼眼", # 0250
    "狗眼", # 0251
    "鹫眼", # 0252
    "蛇眼", # 0253
    "鸦眼", # 0254
    "铁锤", # 0255
    "爆裂铁锤", # 0256
    "闪光灯", # 0257
    "增幅器", # 0258
    "喷嘴", # 0259
    "电容器", # 025A
    "增压器", # 025B
    "安全插件7", # 025C
    "安全插件8", # 025D
    "安全插件9", # 025E
    "安全插件10", # 025F
    "安全插件11", # 0260
    "安全插件12", # 0261
    "安全插件13", # 0262
    "蛇的炮管", # 0263
    "蛇的爆缩机", # 0264
    "蛇的图标", # 0265
    "等离子炮管", # 0266
    "等离子电磁线圈", # 0267
    "等离子电容器", # 0268
    "绯牡丹炮管", # 0269
    "绯牡丹速射装置", # 026A
    "雄性激素", # 026B
    "尖爪之石", # 026C
    "鬣蜥齿之石", # 026D
    "角之石", # 026E
    "大颚之石", # 026F
    "小手之石", # 0270
    "牙之石", # 0271
    "巨大背骨之石", # 0272
    "头颅之石", # 0273
    "背骨之石", # 0274
    "腕之石", # 0275
    "化石花束之石", # 0276
    "巨牙之石", # 0277
    "大耳之石", # 0278
    "独眼巨人头颅之石", # 0279
    "圆形肉之石", # 027A
    "圆简状碎片", # 027B
    "把手碎片", # 027C
    "未知碎片", # 027D
    "躯干碎片", # 027E
    "头部碎片", # 027F
    "胸部碎片", # 0280
    "举起的手碎片", # 0281
    "垂下的手碎片", # 0282
    "简状身体碎片", # 0283
    "裙子碎片", # 0284
    "手腕部件碎片", # 0285
    "太阳镜碎片", # 0286
    "皮夹克碎片", # 0287
    "咖啡罐碎片", # 0288
    "伪装", # 0289
    "刀身", # 028A
    "刀柄", # 028B
    "刀鞘", # 028C
    "小型刀身", # 028D
    "小型刀柄", # 028E
    "小型刀鞘", # 028F
    "怪刀身", # 0290
    "怪刀柄", # 0291
    "怪刀鞘", # 0292
    "烈风枪身", # 0293
    "烈风枪管", # 0294
    "烈风滑套", # 0295
    "突击枪身", # 0296
    "突击枪管", # 0297
    "突击滑套", # 0298
    "未知块", # 0299
    "中型块", # 029A
    "大型块", # 029B
    "水泥枪枪身", # 029C
    "水泥枪枪管", # 029D
    "水泥枪滑套", # 029E
    "龙枪身", # 029F
    "龙枪管", # 02A0
    "龙滑套", # 02A1
    "USP枪身", # 02A2
    "USP枪管", # 02A3
    "USP滑套", # 02A4
    "麦林枪身", # 02A5
    "麦林枪管", # 02A6
    "麦林滑套", # 02A7
    "英格拉枪身", # 02A8
    "英格拉枪管", # 02A9
    "英格拉滑套", # 02AA
    "汪汪炮管", # 02AB
    "犬用轭具", # 02AC
    "犬接合器", # 02AD
    "钻头刃", # 02AE
    "爪柄", # 02AF
    "钻头鞘", # 02B0
    "光束包", # 02B1
    "爆弹包", # 02B2
    "降魔刀助推器", # 02B3
    "真·降魔小刀", # 02B4
    "魔刀身", # 02B5
    "呼魔玉", # 02B6
    "巴士牌", # 02B7
    "205mm绯牡丹核心", # 02B8
    "绯牡丹火神炮核心", # 02B9
    "假人", # 02BA
    "垃圾", # 02BB
    "生化垃圾", # 02BC
    "数码垃圾", # 02BD
    "机械垃圾", # 02BE
    "车体垃圾", # 02BF
    "未知垃圾", # 02C0
    "特别垃圾", # 02C1
    "不寻常的垃圾", # 02C2
    "非常棒的垃圾", # 02C3
    "一流机械垃圾", # 02C4
    "旧文明的垃圾", # 02C5
    "地雷探测器", # 02C6
    "金属探测器", # 02C7
    "BS控制器", # 02C8
    "挂件", # 02C9
    "万能钥匙", # 02CA
    "生发剂", # 02CB
    "生发剂3", # 02CC
    "生发剂T", # 02CD
    "生发剂L", # 02CE
    "生发剂A", # 02CF
    "山芋", # 02D0
    "烤山芋", # 02D1
    "护身符", # 02D2
    "泰迪熊", # 02D3
    
    # 装饰用家具
    "写着\"根性\"字画", # 02D4
    "毕加索的名画", # 02D5
    "达利的名画", # 02D6
    "山水画", # 02D7
    "浮世绘", # 02D8
    "河豚君", # 02D9
    "壁挂钟", # 02DA
    "世界地图", # 02DB
    "波斯地毯", # 02DC
    "榻榻米", # 02DD
    "木质地板", # 02DE
    "木雕熊", # 02DF
    "招财猫", # 02E0
    "八音盒", # 02E1
    "七福神", # 02E2
    "金鱼缸", # 02E3
    "仙人掌盆栽", # 02E4
    "青瓷壶", # 02E5
    "景德镇瓷器", # 02E6
    "花瓶", # 02E7
    "战车模型", # 02E8
    "蔷薇花束", # 02E9
    "向日葵花束", # 02EA
    "非洲菊花束", # 02EB
    "饭桌", # 02EC
    "暖桌", # 02ED
    "时髦桌子", # 02EE
    "地炉", # 02EF
    "食金虫的笼子", # 02F0
    "信乐烧狸", # 02F1
    "观叶植物", # 02F2
    "火盆", # 02F3
    "电风扇", # 02F4
    "点唱机", # 02F5
    "点唱机DX", # 02F6
    "观赏鱼缸", # 02F7
    "饲养箱", # 02F8
    "百叶箱", # 02F9
    "自动售货机", # 02FA
    "衣橱", # 02FB
    "壁橱", # 02FC
    "日式衣柜", # 02FD
    "多屉衣柜", # 02FE
    "带锁的柜子", # 02FF
    "单门电冰箱", # 02F0
    "双门电冰箱", # 02F1
    "豪华电冰箱", # 02F2
    "洗衣机", # 02F3
    "干衣机", # 02F4
    "洗干一体机", # 02F5
    "和服", # 02F6
    "巫服", # 02F7
    "兔女郎装", # 02F8
    "礼服", # 02F9
    "婚纱", # 02FA
    "旗袍", # 02FB
    "女仆装", # 02FC
    "女侍装", # 02FD
    "紧身衣", # 02FE
    "泳装", # 02FF

    # 坦克道具
    "传真", # 0310
    "探照灯", # 0311
    "夜视装置", # 0312
    "灭火装置", # 0313
    "医疗装置", # 0314
    "[空栏]", # 0315
    "换气装置", # 0316
    "冷气", # 0317
    "暖气", # 0318
    "空调", # 0319
    "[空栏]", # 031A
    "[空栏]", # 031B
    "[空栏]", # 031C
    "迷彩伪装", # 031D
    "接地链条", # 031E
    "电磁护屏", # 031F
    "雷达示波器", # 0320
    "撞击板", # 0321
    "[空栏]", # 0322
    "[空栏]", # 0323
    "[空栏]", # 0324
    "[空栏]", # 0325
    "[空栏]", # 0326
    "车喇叭L2", # 0327
    "车喇叭R2", # 0328
    "警报器RA", # 0329
    "除臭剂", # 032A
    "皮革车座", # 032B
    "花纹车座套", # 032C
    "丝绸车座套", # 032D
    "迷彩车座套", # 032E
    "泰迪熊玩具", # 032F
    "嫩叶标志", # 0330
    "欢迎超车标志", # 0331
    "小兔挂饰", # 0332
    "安全护身符", # 0333
    "铅蘑菇", # 0334
    "鸟粪", # 0335
    "废铁", # 0336
    "废铁", # 0337
    "废铁", # 0338
    "烟雾", # 0339
    "红旗", # 033A
    "蓝旗", # 033B
    "绿旗", # 033C
    "黄旗", # 033D
    "黑旗", # 033E
    "鲤鱼幡", # 033F
    "风向鸡", # 0340
    "大渔旗", # 0341
    "旗帜", # 0342

    # 炮弹
    "预备弹", # 0343
    "爆裂弹", # 0344
    "光子弹", # 0345
    "声波弹", # 0346
    "凝固汽油弹", # 0347
    "电磁弹", # 0348
    "冷冻弹", # 0349
    "短箭弹", # 035A
    "炮弹（对地下）", # 035B
    "炮弹（对水中）", # 035C
    "RAP弹", # 035D
    "炮弹（对高空）", # 035E
    "炮弹（对隐形）", # 035F
    "APFSDS弹", # 0350
    "炮弹（部件破坏）", # 0351

    # 特技
    "探索", # 0352
    "探索＆消灭", # 0353
    "修理Lv1", # 0354
    "修理Lv2", # 0355
    "洗车", # 0356
    "轻量化", # 0357
    "中国菜", # 0358
    "废物利用", # 0359
    "特价预感", # 035A
    "工装天使", # 035B
    "家常菜", # 035C
    "战士感觉", # 035D
    "感应器", # 035E
    "超嗅觉", # 035F
    "兽气息", # 0360
    "再生", # 0361
    "药酒桶Lv1", # 0362
    "药酒桶Lv2", # 0363
    "药酒桶Lv3", # 0364
    "药酒桶Lv4", # 0365
    "药酒桶Lv1+", # 0366
    "药酒桶Lv2+", # 0367
    "药酒桶Lv3+", # 0368
    "药酒桶Lv4+", # 0369
    "BS激光", # 036A
    "扩散型BS激光", # 036B
    "穿刺", # 036C
    "鹰眼", # 036D
    "闪避", # 036E
    "牛眼", # 036F
    "对空炮火", # 0370
    "钢铁之城", # 0371
    "冲撞", # 0372
    "火箭启动", # 0373
    "配合行动", # 0374
    "高速机动", # 0375
    "斗志", # 0376
    "突破", # 0377
    "狂奔", # 0378
    "高速驾驶", # 0379
    "火力全开", # 037A
    "自动模式", # 037B
    "即时修理Lv1", # 037C
    "即时修理Lv2", # 037D
    "弱点看破", # 037E
    "小鬼攻击", # 037F
    "短路", # 0380
    "速制炸弹", # 0381
    "拆解魔", # 0382
    "破车", # 0383
    "信号中断", # 0384
    "机械停止", # 0385
    "增压", # 0386
    "解除警报", # 0387
    "工服天使", # 0388
    "支援", # 0389
    "双手枪乱射", # 038A
    "拦截", # 038B
    "远距离狙击", # 038C
    "第三次行动", # 038D
    "快速瞄准", # 038E
    "死神之矢", # 038F
    "猎鸟", # 0390
    "精确射击", # 0391
    "死点射击", # 0392
    "缚影", # 0393
    "最后行动", # 0394
    "弹幕射击", # 0395
    "先手必胜", # 0396
    "零点行动", # 0397
    "致命一击", # 0398
    "枪之舞", # 0399
    "地面突刺", # 039A
    "破箭式", # 039B
    "大回旋斩", # 039C
    "燕返", # 039D
    "真空斩", # 039E
    "见切", # 039F
    "心头灭却", # 03A0
    "修罗", # 03A1
    "霞斩", # 03A2
    "死线斩", # 03A3
    "愤怒", # 03A4
    "最后的一太刀", # 03A5
    "分身斩", # 03A6
    "罗刹", # 03A7
    "死神之手", # 03A8
    "死亡之舞", # 03A9
    "自我修复", # 03AA
    "预备能量", # 03AB
    "预测反击", # 03AC
    "宙斯盾系统", # 03AD
    "宙斯盾系统II", # 03AE
    "手持火神炮", # 03AF
    "集束枪", # 03B0
    "激光步枪", # 03B1
    "榴弹枪", # 03B2
    "关节射击", # 03B3
    "光剑", # 03B4
    "钢铁之爪", # 03B5
    "破坏冲击椎", # 03B6
    "长程追踪导弹", # 03B7
    "电击触发器", # 03B8
    "爆炎连射导弹", # 03B9
    "榴弹发射机", # 03BA
    "金属翼", # 03BB
    "光之翼", # 03BC
    "复仇女神I", # 03BD
    "复仇女神II", # 03BE
    "兽气息", # 03BF
    "再生", # 03C0
    "掩护", # 03C1
    "第二次行动", # 03C2
    "流星", # 03C3
    "流星冲击", # 03C4
    "狗的斗志", # 03C5
    "战号", # 03C6
    "弹头冲撞", # 03C7
    "狂乱冲撞", # 03C8
    "对空冲撞", # 03C9
    "践踏", # 03CA
    "强化皮肤", # 03CB
    "防护罩", # 03CC
    "火焰呼吸", # 03CD
    "眼部光束", # 03CE
    "牵引车光束", # 03CF
    "变色龙光束", # 03D0
    "透明化", # 03D1
    "诱骗", # 03D2
    "保卫", # 03D3
    "迫降", # 03D4
    "挖掘", # 03D5
    "上浮", # 03D6
    "再现", # 03D7
    "追击", # 03D8
    "下降", # 03D9
    "观察迹象", # 03DA
    "破除防护", # 03DB
    "自爆禁止", # 03DC
    "退却阻止", # 03DD

    "阿尔法", # 03DE

    # 其他类道具
    "节子的照片1", # 03DF
    "节子的照片2", # 03E0
    "节子的照片3", # 03E1
    "节子的照片4", # 03E2
    "节子的照片5", # 03E3
    "节子的照片6", # 03E4
    "节子的照片7", # 03E5
    "节子的照片8", # 03E6
    "节子的照片9", # 03E7
    "小孩的照片", # 03E8
    "全家福", # 03E9
    "筋肉宝典", # 03EA
    "怪鱼", # 03EB
    "H书", # 03EC
    "破洞长靴", # 03ED
    "铜奖章", # 03EE
    "银奖章", # 03EF
    "金奖章", # 03F0
    "金块", # 03F1
    "黄金像", # 03F2
    "财宝", # 03F3
    "存储装置", # 03F4
    "宝物地图", # 03F5
    "秘密藏宝图", # 03F6
    "私房钱地图", # 03F7
    "旧地图", # 03F8
    "海盗的地图", # 03F9
    "奇怪的地图", # 03FA
    "豪华的地图", # 03FB
    "超大型奖章", # 03FC
    "只有一半的地图", # 03FD
    "财宝地图", # 03FE
    "传说地图", # 03FF
    "古文书", # 0400
    "钻头爪的笔记", # 0401
    "光束爪的笔记", # 0402
    "爆弹爪的笔记", # 0403
    "真·降魔小刀的笔记", # 0404
    "真·降魔刀的笔记", # 0405
    "165mm幽灵炮的笔记", # 0406
    "205mm绯牡丹的笔记", # 0407
    "绯牡丹火神炮的笔记", # 0408
    "财宝地图的笔记", # 0409
    "传说地图的笔记", # 040A
    "咖喱便当", # 040B
    "游艺桌", # 040C
    "最强之证", # 040D
    "破碎的地图", # 040E
    "地图的碎片", # 040F
    "只有一半的地图", # 0410
    "地图一角", # 0411
    "电击网", # 0412
    "十连胜之证", # 0413
    "二十连胜之证", # 0414
    "三十连胜之证", # 0415
    "所罗门手套", # 0416
    "所罗门之靴", # 0417
    "所罗门之盔", # 0418
    "所罗门之铠", # 0419
    "所罗门之剑", # 041A
)

def itemof(start, end, can_empty=True):
    return ItemProvider(ITEMS, start, end, can_empty)

HUMEN_ITEM = itemof(0x013F, 0x0310) # 人类道具

EQUIP_WEAPON = itemof(0x0001, 0x0064) # 武器
EQUIP_HEAD = itemof(0x0064, 0x0077) # 头部装备
EQUIP_BODY = itemof(0x0077, 0x0090) # 上身装备
EQUIP_HAND = itemof(0x0090, 0x009A) # 手部装备
EQUIP_FOOT = itemof(0x009A, 0x00A5) # 脚部装备
EQUIP_ORN = itemof(0x00A5, 0x00BF) # 装饰
ALL_EQUIP = itemof(0x0001, 0x00BF) # 全部人类装备
CHARIOT_ALL_ITEM = itemof(0x00BF, 0x013F) # 全部战车物品
CHARIOT_CHASSIS = itemof(0x010A, 0x012B) # 底盘
CHARIOT_ITEM = itemof(0x0310, 0x0343) # 战车道具
SPECIAL_BULLETS = itemof(0x0343, 0x0352) # 特殊炮弹
SPECIAL_SKILLS = itemof(0x0352, 0x03DF) # 特技
OTHER_ITEMS = itemof(0x03DF, 0x041B) # 其他类道具

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
    ("甲壳虫", 24, 10, 800, "", ""),
    ("甲壳虫T", 24, 10, 900, "", ""),
    ("甲壳虫TT", 24, 10, 1000, "", ""),
    ("横纲力士", 30, 20, 1200, "", ""),
    ("横纲力士T", 30, 20, 1500, "", ""),
    ("横纲力士TS", 30, 20, 1800, "", ""),
    ("公牛", 40, 30, 2000, "", ""),
    ("巨型公牛", 40, 30, 2300, "", ""),
    ("终极公牛", 40, 30, 2600, "", ""),
    ("涡轮动力", 58, 40, 2700, "", ""),
    ("涡轮动力T", 58, 40, 2900, "", ""),
    ("涡轮动力TT", 58, 40, 3100, "", ""),
    ("V24超人", 83, 50, 3200, "", ""),
    ("V32超人", 83, 50, 3500, "", ""),
    ("V48超人", 83, 50, 3800, "", ""),
    ("疾风", 90, 60, 4000, "", ""),
    ("疾风T", 90, 60, 4200, "", ""),
    ("疾风TS", 90, 60, 4400, "", ""),
    ("OHC卡门", 100, 70, 4500, "", ""),
    ("增强卡门", 100, 70, 4800, "", ""),
    ("飞火卡门", 100, 70, 5100, "", ""),
    ("V48金刚", 115, 80, 5200, "", ""),
    ("V66金刚", 115, 80, 5500, "", ""),
    ("V100金刚", 115, 80, 5800, "", ""),
    ("苦力劳工", 80, 70, 2500, "", ""),
    ("强力苦力劳工", 80, 70, 2800, "", ""),
    ("最强苦力劳工", 80, 70, 3200, "", ""),
)

CHARIOT_EQUIPS = tuple(item[0] for item in CHARIOT_EQUIP_INFOS) # END is 0x7F

SPECIAL_BULLETS = ()


WANTED_LIST = (

)
WANTED_STATUS = ("未击败", "击破", "已领赏金")
WANTED_STATUS_VALUES = (0, 0x63, 0xE3)
