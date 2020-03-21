VERSIONS = ('steam', 'codex')

CHARACTERS = (
    "里昂",
    "克莱尔",
    "艾达",
    "雪莉",
    "汉克",
    "豆腐",
    "武器店老板",
    "局长",
    "记者",
    "太太",
    "幸存者",
    "市长女儿",
    "USS 士兵",
    "警长"
)


CHARACTERS_CODE = (
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    13,
    20,
    12,
    31
)


CHARACTERS_OFFSET = tuple(range(48, 408, 24))

# (item_code, weapon_code, label)
INVENTORY_OPTIONS = (
    (0, -1, "啥都没有"),
    (0, 0x01, "G19 手枪"),
    (0, 0x02, "武器2"),
    (0, 0x03, "武器3"),
    (0, 0x04, "武器4"),
    (0, 0x07, "武器5"),
    (0, 0x08, "武器6"),
    (0, 0x09, "武器7"),
    (0, 0x0B, "M3 散弹枪"),
    (0, 0x15, "CQBR 冲锋枪"),
    (0, 0x17, "武器10"),
    (0, 0x1F, "武器11"),
    (0, 0x29, "武器12"),
    (0, 0x2A, "武器13"),
    (0, 0x2B, "武器14"),
    (0, 0x2C, "武器15"),
    (0, 0x2D, "武器16"),
    (0, 0x2E, "武器17"),
    (0, 0x2F, "武器18"),
    (0, 0x31, "武器19"),
    (0, 0x32, "武器20"),
    (0, 0x41, "武器21"),
    (0, 0x42, "武器22"),
    (0, 0x52, "武器23"),
    (0, 0x53, "武器24"),
    (0, 0x54, "武器25"),
    (0, 0x55, "武器26"),
    (0, 0xDE, "武器27"),
    (0, 0xF2, "武器28"),
    (0, 0xFC, "武器29"),
    (0x01, -1, "急救喷雾"),
    (0x02, -1, "绿色药草"),
    (0x03, -1, "红色药草"),
    (0x04, -1, "蓝色药草"),
    (0x05, -1, "混合药草 (绿+绿)"),
    (0x06, -1, "混合药草 (绿+红)"),
    (0x07, -1, "混合药草 (绿+蓝)"),
    (0x08, -1, "混合药草 (绿+绿+蓝)"),
    (0x09, -1, "混合药草 (绿+绿+绿)"),
    (0x0A, -1, "混合药草 (绿+红+蓝)"),
    (0x0B, -1, "混合药草 (红+蓝)"),
    (0x0C, -1, "绿药"),
    (0x0D, -1, "红药"),
    (0x0E, -1, "蓝药"),
    (0x0F, -1, "手枪子弹"),
    (0x10, -1, "散弹枪子弹"),
    (0x11, -1, "冲锋枪子弹"),
    (0x12, -1, "闪电鹰子弹"),
    (0x16, -1, "硫酸弹"),
    (0x17, -1, "火焰弹"),
    (0x18, -1, "针状弹药(电击枪弹药)"),
    (0x19, -1, "燃料"),
    (0x1A, -1, "大口径手枪弹药"),
    (0x1B, -1, "强力子弹(SLS 60)"),
    (0x1F, -1, "雷管"),
    (0x20, -1, "墨带(存档)"),
    (0x21, -1, "木板"),
    (0x22, -1, "雷管 (无电池)"),
    (0x23, -1, "电池"),
    (0x24, -1, "火药"),
    (0x25, -1, "火药 (Lage)"),
    (0x26, -1, "高级火药 (黄色)"),
    (0x27, -1, "高级火药 (白色)"),
    (0x30, -1, "大容量弹夹 (玛蒂尔达)"),
    (0x31, -1, "枪口制退器 (玛蒂尔达)"),
    (0x32, -1, "枪托 (玛蒂尔达)"),
    (0x33, -1, "快速装弹器 (SLS 60)"),
    (0x34, -1, "激光瞄准器 (JMB Hp3)"),
    (0x35, -1, "强化枪身 (SLS 60)"),
    (0x36, -1, "大容量弹夹 (JMB Hp3)"),
    (0x37, -1, "散弹枪枪托 (W-870)"),
    (0x38, -1, "长枪管 (W-870)"),
    (0x3A, -1, "大容量弹夹 (MQ 11)"),
    (0x3C, -1, "消音器 (MQ 11)"),
    (0x3D, -1, "红点瞄准器 (闪电鹰)"),
    (0x3E, -1, "长枪管 (闪电鹰)"),
    (0x40, -1, "肩式枪托 (GM 79)"),
    (0x41, -1, "调整器 (火焰喷射器)"),
    (0x42, -1, "高压电容器 (火花射击)"),
    (0x48, -1, "胶卷: “隐藏的地方”"),
    (0x49, -1, "胶卷: “崛起的新秀”"),
    (0x4A, -1, "胶卷: “纪念”"),
    (0x4B, -1, "胶卷: “3F 储物柜”"),
    (0x4C, -1, "影片: “狮子雕像”"),
    (0x4D, -1, "储藏室钥匙"),
    (0x4F, -1, "千斤顶把手"),
    (0x50, -1, "方形曲柄"),
    (0x51, -1, "独角兽奖章"),
    (0x52, -1, "黑桃钥匙"),
    (0x53, -1, "停车场钥匙卡"),
    (0x54, -1, "武器储物柜钥匙卡"),
    (0x56, -1, "阀门手柄"),
    (0x57, -1, "S.T.A.R.S. 徽章"),
    (0x58, -1, "权杖"),
    (0x5A, -1, "红宝石"),
    (0x5B, -1, "宝石盒"),
    (0x5D, -1, "主教插头"),
    (0x5E, -1, "城堡插头"),
    (0x5F, -1, "国王插头"),
    (0x62, -1, "图案砖块"),
    (0x66, -1, "USB 加密钥匙"),
    (0x70, -1, "备用钥匙 (终端按键)"),
    (0x72, -1, "红色书籍"),
    (0x73, -1, "雕像的左臂"),
    (0x74, -1, "拿着书的左臂"),
    (0x76, -1, "狮子奖章"),
    (0x77, -1, "钻石钥匙"),
    (0x78, -1, "汽车钥匙"),
    (0x7C, -1, "少女奖章"),
    (0x7E, -1, "电源面板部件"),
    (0x7F, -1, "电源面板部件"),
    (0x80, -1, "情人浮雕"),
    (0x81, -1, "小齿轮"),
    (0x82, -1, "大齿轮"),
    (0x83, -1, "中庭钥匙"),
    (0x84, -1, "骑士插头"),
    (0x85, -1, "兵卒插头"),
    (0x86, -1, "皇后插头"),
    (0x87, -1, "盒装电子部件"),
    (0x88, -1, "盒装电子部件"),
    (0x9F, -1, "孤儿院钥匙"),
    (0xA0, -1, "俱乐部钥匙"),
    (0xA9, -1, "红心钥匙"),
    (0xAA, -1, "美国数字录像带"),
    (0xB0, -1, "T型阀手柄"),
    (0xB3, -1, "分散墨盒 (空)"),
    (0xB4, -1, "分散墨盒 (溶液)"),
    (0xB5, -1, "分散墨盒 (除草剂)"),
    (0xB7, -1, "接合插头"),
    (0xBA, -1, "升级芯片 (管理员)"),
    (0xBB, -1, "ID 腕带 (管理员)"),
    (0xBC, -1, "电子芯片"),
    (0xBD, -1, "信号调制器"),
    (0xBE, -1, "奖杯 (第1)"),
    (0xBF, -1, "奖杯 (第2)"),
    (0xC2, -1, "下水道钥匙"),
    (0xC3, -1, "ID 腕带 (访客) (Leon)"),
    (0xC4, -1, "ID 腕带 (总参谋部) (Leon)"),
    (0xC5, -1, "ID 腕带 (高级职员) (Leon)"),
    (0xC6, -1, "升级芯片 (总参谋部)"),
    (0xC7, -1, "升级芯片 (高级职员)"),
    (0xC8, -1, "ID 腕带 (访客) (Claire)"),
    (0xC9, -1, "ID 腕带 (总参谋部) (Claire)"),
    (0xCA, -1, "ID 腕带 (高级职员) (克莱尔)"),
    (0xCB, -1, "实验室数字录像带"),
    (0xF0, -1, "保险丝(主厅)"),
    (0xF1, -1, "(休息室走廊)"),
    (0xF3, -1, "剪刀"),
    (0xF4, -1, "断线钳"),
    (0xF5, -1, "毛绒娃娃"),
    (0x11E, -1, "旧钥匙")
)

INVENTORY_LABELS = [item[2] for item in INVENTORY_OPTIONS]

# weapo_code: ammo_code
AMMO_MAP = {
    0x01: 0x0F,
    0x02: 0x1A,
    0x03: 0x0F,
    0x04: 0x1A,
    0x07: 0x0F,
    0x08: 0x0F,
    0x09: 0x0F,
    0x0B: 0x10,
    0x15: 0x11,
    0x17: 0x11,
    0x1F: 0x12,
    0x2A: 0x16,
    0x2B: 0x19,
    0x2C: 0x18,
    0x52: 0x0F,
}
