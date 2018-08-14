WEAPON_LIST = [
    ("Melee 手持物", (
        ("GOLFCLUB", "高尔夫球杆", 0x440E4788),
        ("HAMMER", "铁锤", 0x4E875F73),
        ("NIGHTSTICK", "警棍", 0x678B81B1),
        ("CROWBAR", "铁撬", 0x84BD7BFD),
        ("DAGGER", "古董骑兵匕首", 0x92A27487),
        ("BAT", "球棒", 0x958A4A8F),
        ("KNIFE", "小刀", 0x99B507EA),
        ("HANDCUFFS", "手铐", 0xD04C944D),
        ("GARBAGEBAG", "垃圾袋", 0xE232C28C),
        ("BOTTLE", "瓶子", 0xF9E6AA4B),
    )),
    ("Pistol 手枪", (
        ("PISTOL", "手枪", 0x1B06D571),
        ("COMBATPISTOL", "战斗手枪", 0x5EF9FEC4),
        ("PISTOL50", "50口径手枪", 0x99AEEB3B),
        ("SNSPISTOL", "劣质手枪", 0xBFD21232),
        ("HEAVYPISTOL", "重型手枪", 0xD205520E),
        ("VINTAGEPISTOL", "复古手枪", 0x083839C4),
        ("MARKSMANPISTOL", "射手手枪", 0xDC4DB296),
        ("APPISTOL", "穿甲手枪", 0x22D8FE39),
        ("STUNGUN", "电击枪", 0x3656C8C1),
        ("FLAREGUN", "闪光弹枪", 0x47757124),
    )),
    ("ShotGun 霰弹枪", (
        ("PUMPSHOTGUN", "泵动式霰弹枪", 0x1D073A89),
        ("SAWNOFFSHOTGUN", "削短型霰弹枪", 0x7846A318),
        ("BULLPUPSHOTGUN", "犊牛式霰弹枪", 0x9D61E50F),
        ("ASSAULTSHOTGUN", "突击霰弹枪", 0xE284C527),
        ("MUSKET", "老式火枪", 0xA89CB99E),
        ("HEAVYSHOTGUN", "重型霰弹枪", 0x3AABBBAA),
        )),
    ("SMG 微冲 / MG 冲锋枪", (
        ("MICROSMG", "小型冲锋枪", 0x13532244),
        ("SMG", "冲锋枪", 0x2BE6766B),
        ("ASSAULTSMG", "突击冲锋枪", 0xEFE7E2DF),
        ("COMBATPDW", "战斗自卫冲锋枪", 0xA3D4D34),
        ("MG", "机关枪", 0x9D07F764),
        ("COMBATMG", "战斗机关枪", 0x7FD62962),
        ("GUSENBERG", "古森柏冲锋枪", 0x61012683),
    )),
    ("AssaultRifle 步枪", (
        ("ASSAULTRIFLE", "突击步枪", 0xBFEFFF6D),
        ("CARBINERIFLE", "卡宾步枪", 0x83BF0278),
        ("ADVANCEDRIFLE", "高阶步枪", 0xAF113F99),
        ("SPECIALCARBINE", "特制卡宾步枪", 0xC0A3098D),
        ("BULLPUPRIFLE", "犊牛式步枪", 0x7F229F94),
    )),
    ("Sniper 狙击枪", (
        ("SNIPERRIFLE", "狙击枪", 0x05FC3C11),
        ("HEAVYSNIPER", "重型狙击枪", 0x0C472FE2),
        ("MARKSMANRIFLE", "射手步枪", 0xC734385A),
    )),
    ("Heavy 重武器", (
        ("GRENADELAUNCHER", "榴弹发射器", 0xA284510B),
        ("RPG", "火箭砲", 0xB1CA77B1),
        ("PASSENGER_ROCKET", "不可使用", 0x166218FF),
        ("STINGER", "火箭砲", 0x687652CE),
        ("MINIGUN", "火神机枪", 0x42BF8A85),
        ("FIREWORK", "烟火发射器", 0x7F7497E5),
        ("RAILGUN", "镭射枪", 0x6D544C99),
        ("HOMINGLAUNCHER", "追踪弹发射器", 0x63AB0442),
        ("GRENADELAUNCHER_SMOKE", "烟雾弹发射器", 0x4DD2DC56),
        # ("AIRSTRIKE_ROCKET", "空袭", 0x13579279),
        # ("VEHICLE_ROCKET", "车载火箭炮", 0xBEFDC581),
    )),
    ("Thrown 投掷物", (
        ("GRENADE", "手榴弹", 0x93E220BD),
        ("STICKYBOMB", "黏弹", 0x2C3731D9),
        ("PROXMINE", "感应式地雷", 0xAB564B93),
        ("SMOKEGRENADE", "催泪瓦斯", 0xFDBC8A50),
        ("BZGAS", "毒气弹", 0xA0973D5E),
        ("MOLOTOV", "汽油弹", 0x24B17070),
        ("FIREEXTINGUISHER", "灭火器", 0x060EC506),
        ("PETROLCAN", "汽油桶", 0x34A67B97),
        ("BALL", "球", 0x23C9F95C),
        ("SNOWBALL", "雪球", 0x787F0BB),
        ("FLARE", "信号弹", 0x497FACC3),
    )),
    ("其他", (
        ("PARACHUTE", "降落伞", 0xFBAB5776),
        ("KNUCKLE", "指节套环", 0xD8DF3C3C),
        ("DIGISCANNER", "串口扫描仪", 0xFDBADCED),
        ("BRIEFCASE_02", "公文包02", 0x01B79F17),
        ("BRIEFCASE", "公文包", 0x88C78EB7),
    )),
    # ("车载武器", (
    #     ("ROTORS", "轮子", 0xB1205A4E),
    #     ("TANK", "坦克", 0x73F7C04B),
    #     ("SPACE_ROCKET", "九头蛇飞弹", 0xF8A3939F),
    #     ("PLANE_ROCKET", "天煞飞弹", 0xCF0896E0),
    #     ("PLAYER_LAZER", "镭射炮", 0xE2822A29),
    #     ("PLAYER_LASER", "玩家激光(无杀伤力)", 0xEFFD014B),
    #     ("PLAYER_BULLET", "PLAYER_BULLET", 0x4B139B2D),
    #     ("PLAYER_BUZZARD", "机关枪", 0x46B89C8E),
    #     ("PLAYER_HUNTER", "阿帕奇镭射炮", 0x9F1A91DE),
    #     ("ENEMY_LASER", "敌人激光(无杀伤力)", 0x5D6660AB),
    #     ("SEARCHLIGHT", "搜寻光", 0xCDAC517D),
    #     ("RADAR", "雷达", 0xD276317E),
    #     ("WATER_CANNON", "高压水枪", 0x67D18297),
    #     ("TURRET_INSURGENT", "叛乱份子机关枪", 0x44DB5498),
    #     ("TURRET_TECHNICAL", "铁尼高机关枪", 0x7FD2EA0B),
    #     ("NOSE_TURRET_VALKYRIE", "鼻炮塔", 0x4170E491),
    #     ("PLAYER_SAVAGE", "白金汉镭射炮", 0x61A31349),
    # )),
]

SHOOT_WEAPON_CHOICES = (
    ("车载火箭炮", 0xBEFDC581),
    ("空袭", 0x13579279),
    ("火箭砲", 0xB1CA77B1),
    ("火箭砲2", 0x687652CE),
    ("镭射枪", 0x6D544C99),
    ("追踪弹发射器", 0x63AB0442),
    ("烟火发射器", 0x7F7497E5),
    ("坦克", 0x73F7C04B),
    ("九头蛇飞弹", 0xF8A3939F),
    ("天煞飞弹", 0xCF0896E0),
    ("天煞镭射炮", 0xE2822A29),
    ("阿帕奇镭射炮", 0x9F1A91DE),
    ("鼻炮塔", 0x4170E491),
    ("当前武器", 0),
)


# 载具种类
# VC_Compacts = 0 # 小型汽车
# VC_Sedans = 1 # 轿车
# VC_Suv = 2 # 运动休旅车
# VC_Coupes = 3 # 轿跑车
# VC_Muscle = 4 # 美式肌肉车
# VC_SportClassics = 5 # 跑车
# VC_Sports = 6 # 经典跑车
# VC_Super = 7 # 超级跑车
# VC_Motorcycles = 8 # 摩托车
# VC_OffRoad = 9 # 越野车
# VC_Industrial = 10 # 工业用车
# VC_Utility = 11 # 工作车辆
# VC_Van = 12 # 厢型车
# VC_Cycle = 13 # 单车
# VC_Boats = 14 # 船
# VC_Helicopters = 15 # 直升机
# VC_Planes = 16 # 飞机
# VC_Service = 17 # 服务
# VC_Emergency = 18 # 紧急车辆
# VC_Military = 19 # 军队
# VC_Commercial = 20 # 商务用
# VC_Train = 21 # 列车

# PICKUP_TYPE = (
#     ("CustomScript", 0x2C014CA6),
#     ("VehicleCustomScript", 0xA5B8CAA9),
#     ("Parachute", 0x6773257D),
#     ("PortablePackage", 0x80AB931C),
#     ("PortableCrateUnfixed", 0x6E717A95),
#     ("Health", 0x8F707C18),
#     ("HealthSnack", 0x1CD2CF66),
#     ("Armour", 0x4BFB42D1),
#     ("MoneyCase", 0xCE6FDD6B),
#     ("MoneySecurityCase", 0xDE78F17E),
#     ("MoneyVariable", 0xFE18F3AF),
#     ("MoneyMedBag", 0x14568F28),
#     ("MoneyPurse", 0x1E9A99F8),
#     ("MoneyDepBag", 0x20893292),
#     ("MoneyWallet", 0x5DE0AD3E),
#     ("MoneyPaperBag", 0x711D02A4),
#     ("WeaponPistol", 0xF9AFB48F),
#     ("WeaponCombatPistol", 0x8967B4F3),
#     ("WeaponAPPistol", 0x3B662889),
#     ("WeaponSNSPistol", 0xC5B72713),
#     ("WeaponHeavyPistol", 0x9CF13918),
#     ("WeaponMicroSMG", 0x1D9588D3),
#     ("WeaponSMG", 0x3A4C2AD2),
#     ("WeaponMG", 0x85CAA9B1),
#     ("WeaponCombatMG", 0xB2930A14),
#     ("WeaponAssaultRifle", 0xF33C83B0),
#     ("WeaponCarbineRifle", 0xDF711959),
#     ("WeaponAdvancedRifle", 0xB2B5325E),
#     ("WeaponSpecialCarbine", 0x968339D),
#     ("WeaponBullpupRifle", 0x815D66E8),
#     ("WeaponPumpShotgun", 0xA9355DCD),
#     ("WeaponSawnoffShotgun", 0x96B412A3),
#     ("WeaponAssaultShotgun", 0x9299C95B),
#     ("WeaponSniperRifle", 0xFE2A352C),
#     ("WeaponHeavySniper", 0x693583AD),
#     ("WeaponGrenadeLauncher", 0x2E764125),
#     ("WeaponRPG", 0x4D36C349),
#     ("WeaponMinigun", 0x2F36B434),
#     ("WeaponGrenade", 0x5E0683A1),
#     ("WeaponStickyBomb", 0x7C119D58),
#     ("WeaponSmokeGrenade", 0x1CD604C7),
#     ("WeaponMolotov", 0x2DD30479),
#     ("WeaponPetrolCan", 0xC69DE3FF),
#     ("WeaponKnife", 0x278D8734),
#     ("WeaponNightstick", 0x5EA16D74),
#     ("WeaponBat", 0x81EE601E),
#     ("WeaponCrowbar", 0x872DC888),
#     ("WeaponGolfclub", 0x88EAACA7),
#     ("WeaponBottle", 0xFA51ABF5),
#     ("VehicleWeaponPistol", 0xA54AE7B7),
#     ("VehicleWeaponCombatPistol", 0xD0AACEF7),
#     ("VehicleWeaponAPPistol", 0xCC8B3905),
#     ("VehicleWeaponMicroSMG", 0xB86AEE5B),
#     ("VehicleWeaponSawnoffShotgun", 0x2E071B5A),
#     ("VehicleWeaponGrenade", 0xA717F898),
#     ("VehicleWeaponSmokeGrenade", 0x65A7D8E9),
#     ("VehicleWeaponStickyBomb", 0x2C804FE3),
#     ("VehicleWeaponMolotov", 0x84D676D4),
#     ("VehicleHealth", 0x98D79EF),
#     ("AmmoPistol", 0x20796A82),
#     ("AmmoSMG", 0x116FC4E6),
#     ("AmmoMG", 0xDE58E0B3),
#     ("AmmoRifle", 0xE4BD2FC6),
#     ("AmmoShotgun", 0x77F3F2DD),
#     ("AmmoSniper", 0xC02CF125),
#     ("AmmoGrenadeLauncher", 0x881AB0A8),
#     ("AmmoRPG", 0x84837FD7),
#     ("AmmoMinigun", 0xF25A01B9),
#     ("AmmoMissileMP", 0xF99E15D0),
#     ("AmmoBulletMP", 0x550447A9),
#     ("AmmoGrenadeLauncherMP", 0x1069C3B8)
# )


# DRIVING_STYLE FLAG
# None = 0
# FollowTraffic = 1
# YieldToPeds = 2
# AvoidVehicles = 4
# AvoidEmptyVehicles = 8
# AvoidPeds = 16
# AvoidObjects = 32
# StopAtTrafficLights = 128
# UseBlinkers = 256
# AllowGoingWrongWay = 512
# Reverse = 1024
# AllowMedianCrossing = 262144
# DriveBySight = 4194304
# IgnorePathFinding = 16777216
# TryToAvoidHighways = 536870912
# StopAtDestination = 0x80000000

DRIVING_STYLE = (
    ("IgnoreLights", 0x802c0025),
    ("Normal (typically used by the game)", 0xc00ab),
    ("Sometimes Overtake traffic", 0x5),
    ("Rushed", 0x400c0025),
    ("Avoid traffic", 0xc0024),
    ("Avoid traffic extreme", 0x6),
    ("Avoid everything", 0x34),
    ("Careful driving", 0x23),
)


WEATHER_LIST = (
    ("阳光明媚", "EXTRASUNNY"),
    ("晴朗", "CLEAR"),
    ("多云", "CLOUDS"),
    ("霾", "SMOG"),
    ("雾", "FOGGY"),
    ("阴", "OVERCAST"),
    ("雨", "RAIN"),
    ("雷阵雨", "THUNDER"),
    ("太阳雨", "CLEARING"),
    ("酸雨", "NEUTRAL"),
    ("雪 (无光照)", "SNOW"),
    ("暴风雪 (无光照)", "BLIZZARD"),
    ("雪", "SNOWLIGHT"),
    ("圣诞雪", "XMAS"),
)


COLOR_LIST = (
    0x080808, 0x0F0F0F, 0x211E1C, 0x2E2C29, 0x665E5A, 0x877C77, 0x595451, 0x473B32,
    0x333333, 0x26221F, 0x2E2923, 0x101112, 0x050505, 0x121212, 0x33322F, 0x080808,
    0x121212, 0x242220, 0x615957, 0x2E2923, 0x473B32, 0x12100F, 0x212121, 0x5E5D5B,
    0x998A88, 0x877169, 0x54463B, 0x000069, 0x000B8A, 0x00006B, 0x091061, 0x0A0A4A,
    0x0E0E47, 0x000C38, 0x0B0326, 0x120063, 0x002880, 0x2D4F6E, 0x0048BD, 0x000078,
    0x000036, 0x003FAB, 0x007EDE, 0x000052, 0x04048C, 0x00104A, 0x252559, 0x314275,
    0x040821, 0x071200, 0x0B1A00, 0x1E2100, 0x1E261F, 0x053800, 0x45410B, 0x038541,
    0x151F0F, 0x133602, 0x192416, 0x25362A, 0x565C45, 0x140D00, 0x291000, 0x4F2F1C,
    0x571B00, 0x784E3B, 0x3B2D27, 0xDBB295, 0x7A623E, 0x40311C, 0xC45500, 0x2E181A,
    0x291616, 0x6D310E, 0x835A39, 0x2E1409, 0x21100F, 0x522A15, 0x544632, 0x632515,
    0xA13B22, 0xA11F1F, 0x2E0E03, 0x731E0F, 0x321C00, 0x54372A, 0x5E3C30, 0x96673B,
    0x0F89F5, 0x00A6D9, 0x1B344A, 0x27A8A2, 0x008F56, 0x4B5157, 0x061B29, 0x172126,
    0x070D12, 0x112133, 0x23303D, 0x43535E, 0x2B3837, 0x181922, 0x365057, 0x091324,
    0x00173B, 0x46626E, 0x738D99, 0xA5C0CF, 0x09171F, 0x1D313D, 0x475866, 0xF0F0F0,
    0xC9B9B3, 0x555F61, 0x1A1E24, 0x131417, 0x2F373B, 0x45403B, 0x211E1A, 0x6B645E,
    0x000000, 0xB0B0B0, 0x999999, 0x1965B5, 0x335CC4, 0x3C7847, 0x2584BA, 0xA1772A,
    0x223024, 0x545F6B, 0x346EC9, 0xD9D9D9, 0xF0F0F0, 0x28423F, 0xFFFFFF, 0x5912B0,
    0x9997F6, 0x552F8F, 0x1066C2, 0x45BD69, 0xEFAE00, 0x080100, 0x080005, 0x000008,
    0x515756, 0x420632, 0x0F0800, 0x080808, 0x420632, 0x080005, 0x000B6B, 0x101712,
    0x253332, 0x2D353B, 0x566670, 0x2B302B, 0x474341, 0xB59066, 0x1B3947, 0x1B3947,
    0x59D8FF,
)


DIRECTION_FRONT = 0
DIRECTION_BACK = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3
DIRECTION_ABOVE = 4
ATTACH_DIRECTION = (
    ("前", DIRECTION_FRONT),
    ("后", DIRECTION_BACK),
    ("左", DIRECTION_LEFT),
    ("右", DIRECTION_RIGHT),
    ("上", DIRECTION_ABOVE),
)