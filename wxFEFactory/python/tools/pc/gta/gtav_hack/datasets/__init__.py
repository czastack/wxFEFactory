WEAPON_LIST = [
    ("Melee 手持物", (
        (0x440E4788, "GOLFCLUB", "高尔夫球杆"),
        (0x4E875F73, "HAMMER", "铁锤"),
        (0x678B81B1, "NIGHTSTICK", "警棍"),
        (0x84BD7BFD, "CROWBAR", "铁撬"),
        (0x92A27487, "DAGGER", "古董骑兵匕首"),
        (0x958A4A8F, "BAT", "球棒"),
        (0x99B507EA, "KNIFE", "小刀"),
        (0xD04C944D, "HANDCUFFS", "手铐"),
        (0xE232C28C, "GARBAGEBAG", "垃圾袋"),
        (0xF9E6AA4B, "BOTTLE", "瓶子"),
    )),
    ("Pistol 手枪", (
        (0x1B06D571, "PISTOL", "手枪"),
        (0x5EF9FEC4, "COMBATPISTOL", "战斗手枪"),
        (0x99AEEB3B, "PISTOL50", "50口径手枪"),
        (0xBFD21232, "SNSPISTOL", "劣质手枪"),
        (0xD205520E, "HEAVYPISTOL", "重型手枪"),
        (0x083839C4, "VINTAGEPISTOL", "复古手枪"),
        (0xDC4DB296, "MARKSMANPISTOL", "射手手枪"),
        (0x22D8FE39, "APPISTOL", "穿甲手枪"),
        (0x3656C8C1, "STUNGUN", "电击枪"),
        (0x47757124, "FLAREGUN", "闪光弹枪"),
    )),
    ("ShotGun 霰弹枪", (
        (0x1D073A89, "PUMPSHOTGUN", "泵动式霰弹枪"),
        (0x7846A318, "SAWNOFFSHOTGUN", "削短型霰弹枪"),
        (0x9D61E50F, "BULLPUPSHOTGUN", "犊牛式霰弹枪"),
        (0xE284C527, "ASSAULTSHOTGUN", "突击霰弹枪"),
        (0xA89CB99E, "MUSKET", "老式火枪"),
        (0x3AABBBAA, "HEAVYSHOTGUN", "重型霰弹枪"),
    )),
    ("SMG 微冲 / MG 冲锋枪", (
        (0x13532244, "MICROSMG", "小型冲锋枪"),
        (0x2BE6766B, "SMG", "冲锋枪"),
        (0xEFE7E2DF, "ASSAULTSMG", "突击冲锋枪"),
        (0xA3D4D34, "COMBATPDW", "战斗自卫冲锋枪"),
        (0x9D07F764, "MG", "机关枪"),
        (0x7FD62962, "COMBATMG", "战斗机关枪"),
        (0x61012683, "GUSENBERG", "古森柏冲锋枪"),
    )),
    ("AssaultRifle 步枪", (
        (0xBFEFFF6D, "ASSAULTRIFLE", "突击步枪"),
        (0x83BF0278, "CARBINERIFLE", "卡宾步枪"),
        (0xAF113F99, "ADVANCEDRIFLE", "高阶步枪"),
        (0xC0A3098D, "SPECIALCARBINE", "特制卡宾步枪"),
        (0x7F229F94, "BULLPUPRIFLE", "犊牛式步枪"),
    )),
    ("Sniper 狙击枪", (
        (0x05FC3C11, "SNIPERRIFLE", "狙击枪"),
        (0x0C472FE2, "HEAVYSNIPER", "重型狙击枪"),
        (0xC734385A, "MARKSMANRIFLE", "射手步枪"),
    )),
    ("Heavy 重武器", (
        (0xA284510B, "GRENADELAUNCHER", "榴弹发射器"),
        (0xB1CA77B1, "RPG", "火箭砲"),
        (0x166218FF, "PASSENGER_ROCKET", "不可使用"),
        (0x687652CE, "STINGER", "火箭砲"),
        (0x42BF8A85, "MINIGUN", "火神机枪"),
        (0x7F7497E5, "FIREWORK", "烟火发射器"),
        (0x6D544C99, "RAILGUN", "镭射枪"),
        (0x63AB0442, "HOMINGLAUNCHER", "追踪弹发射器"),
        (0x4DD2DC56, "GRENADELAUNCHER_SMOKE", "烟雾弹发射器"),
        #0x13579279,  ("AIRSTRIKE_ROCKET", "空袭"),
        #0xBEFDC581,  ("VEHICLE_ROCKET", "车载火箭炮"),
    )),
    ("Thrown 投掷物", (
        (0x93E220BD, "GRENADE", "手榴弹"),
        (0x2C3731D9, "STICKYBOMB", "黏弹"),
        (0xAB564B93, "PROXMINE", "感应式地雷"),
        (0xFDBC8A50, "SMOKEGRENADE", "催泪瓦斯"),
        (0xA0973D5E, "BZGAS", "毒气弹"),
        (0x24B17070, "MOLOTOV", "汽油弹"),
        (0x060EC506, "FIREEXTINGUISHER", "灭火器"),
        (0x34A67B97, "PETROLCAN", "汽油桶"),
        (0x23C9F95C, "BALL", "球"),
        (0x787F0BB, "SNOWBALL", "雪球"),
        (0x497FACC3, "FLARE", "信号弹"),
    )),
    ("其他", (
        (0xFBAB5776, "PARACHUTE", "降落伞"),
        (0xD8DF3C3C, "KNUCKLE", "指节套环"),
        (0xFDBADCED, "DIGISCANNER", "串口扫描仪"),
        (0x01B79F17, "BRIEFCASE_02", "公文包02"),
        (0x88C78EB7, "BRIEFCASE", "公文包"),
    )),
    # ("车载武器", (
    #      (0xB1205A4E, "ROTORS", "轮子"),
    #      (0x73F7C04B, "TANK", "坦克"),
    #      (0xF8A3939F, "SPACE_ROCKET", "九头蛇飞弹"),
    #      (0xCF0896E0, "PLANE_ROCKET", "天煞飞弹"),
    #      (0xE2822A29, "PLAYER_LAZER", "镭射炮"),
    #      (0xEFFD014B, "PLAYER_LASER", "玩家激光(无杀伤力)"),
    #      (0x4B139B2D, "PLAYER_BULLET", "PLAYER_BULLET"),
    #      (0x46B89C8E, "PLAYER_BUZZARD", "机关枪"),
    #      (0x9F1A91DE, "PLAYER_HUNTER", "阿帕奇镭射炮"),
    #      (0x5D6660AB, "ENEMY_LASER", "敌人激光(无杀伤力)"),
    #      (0xCDAC517D, "SEARCHLIGHT", "搜寻光"),
    #      (0xD276317E, "RADAR", "雷达"),
    #      (0x67D18297, "WATER_CANNON", "高压水枪"),
    #      (0x44DB5498, "TURRET_INSURGENT", "叛乱份子机关枪"),
    #      (0x7FD2EA0B, "TURRET_TECHNICAL", "铁尼高机关枪"),
    #      (0x4170E491, "NOSE_TURRET_VALKYRIE", "鼻炮塔"),
    #      (0x61A31349, "PLAYER_SAVAGE", "白金汉镭射炮"),
    # )),
]

SHOOT_WEAPON_CHOICES = (
    (0xBEFDC581, "车载火箭炮"),
    (0x13579279, "空袭"),
    (0xB1CA77B1, "火箭砲"),
    (0x687652CE, "火箭砲2"),
    (0x6D544C99, "镭射枪"),
    (0x63AB0442, "追踪弹发射器"),
    (0x7F7497E5, "烟火发射器"),
    (0x73F7C04B, "坦克"),
    (0xF8A3939F, "九头蛇飞弹"),
    (0xCF0896E0, "天煞飞弹"),
    (0xE2822A29, "天煞镭射炮"),
    (0x9F1A91DE, "阿帕奇镭射炮"),
    (0x4170E491, "鼻炮塔"),
    (0, "当前武器"),
)


# 载具种类
# VC_Compacts = 0  # 小型汽车
# VC_Sedans = 1  # 轿车
# VC_Suv = 2  # 运动休旅车
# VC_Coupes = 3  # 轿跑车
# VC_Muscle = 4  # 美式肌肉车
# VC_SportClassics = 5  # 跑车
# VC_Sports = 6  # 经典跑车
# VC_Super = 7  # 超级跑车
# VC_Motorcycles = 8  # 摩托车
# VC_OffRoad = 9  # 越野车
# VC_Industrial = 10  # 工业用车
# VC_Utility = 11  # 工作车辆
# VC_Van = 12  # 厢型车
# VC_Cycle = 13  # 单车
# VC_Boats = 14  # 船
# VC_Helicopters = 15  # 直升机
# VC_Planes = 16  # 飞机
# VC_Service = 17  # 服务
# VC_Emergency = 18  # 紧急车辆
# VC_Military = 19  # 军队
# VC_Commercial = 20  # 商务用
# VC_Train = 21  # 列车

# PICKUP_TYPE = (
#     (0x2C014CA6, "CustomScript"),
#     (0xA5B8CAA9, "VehicleCustomScript"),
#     (0x6773257D, "Parachute"),
#     (0x80AB931C, "PortablePackage"),
#     (0x6E717A95, "PortableCrateUnfixed"),
#     (0x8F707C18, "Health"),
#     (0x1CD2CF66, "HealthSnack"),
#     (0x4BFB42D1, "Armour"),
#     (0xCE6FDD6B, "MoneyCase"),
#     (0xDE78F17E, "MoneySecurityCase"),
#     (0xFE18F3AF, "MoneyVariable"),
#     (0x14568F28, "MoneyMedBag"),
#     (0x1E9A99F8, "MoneyPurse"),
#     (0x20893292, "MoneyDepBag"),
#     (0x5DE0AD3E, "MoneyWallet"),
#     (0x711D02A4, "MoneyPaperBag"),
#     (0xF9AFB48F, "WeaponPistol"),
#     (0x8967B4F3, "WeaponCombatPistol"),
#     (0x3B662889, "WeaponAPPistol"),
#     (0xC5B72713, "WeaponSNSPistol"),
#     (0x9CF13918, "WeaponHeavyPistol"),
#     (0x1D9588D3, "WeaponMicroSMG"),
#     (0x3A4C2AD2, "WeaponSMG"),
#     (0x85CAA9B1, "WeaponMG"),
#     (0xB2930A14, "WeaponCombatMG"),
#     (0xF33C83B0, "WeaponAssaultRifle"),
#     (0xDF711959, "WeaponCarbineRifle"),
#     (0xB2B5325E, "WeaponAdvancedRifle"),
#     (0x0968339D, "WeaponSpecialCarbine"),
#     (0x815D66E8, "WeaponBullpupRifle"),
#     (0xA9355DCD, "WeaponPumpShotgun"),
#     (0x96B412A3, "WeaponSawnoffShotgun"),
#     (0x9299C95B, "WeaponAssaultShotgun"),
#     (0xFE2A352C, "WeaponSniperRifle"),
#     (0x693583AD, "WeaponHeavySniper"),
#     (0x2E764125, "WeaponGrenadeLauncher"),
#     (0x4D36C349, "WeaponRPG"),
#     (0x2F36B434, "WeaponMinigun"),
#     (0x5E0683A1, "WeaponGrenade"),
#     (0x7C119D58, "WeaponStickyBomb"),
#     (0x1CD604C7, "WeaponSmokeGrenade"),
#     (0x2DD30479, "WeaponMolotov"),
#     (0xC69DE3FF, "WeaponPetrolCan"),
#     (0x278D8734, "WeaponKnife"),
#     (0x5EA16D74, "WeaponNightstick"),
#     (0x81EE601E, "WeaponBat"),
#     (0x872DC888, "WeaponCrowbar"),
#     (0x88EAACA7, "WeaponGolfclub"),
#     (0xFA51ABF5, "WeaponBottle"),
#     (0xA54AE7B7, "VehicleWeaponPistol"),
#     (0xD0AACEF7, "VehicleWeaponCombatPistol"),
#     (0xCC8B3905, "VehicleWeaponAPPistol"),
#     (0xB86AEE5B, "VehicleWeaponMicroSMG"),
#     (0x2E071B5A, "VehicleWeaponSawnoffShotgun"),
#     (0xA717F898, "VehicleWeaponGrenade"),
#     (0x65A7D8E9, "VehicleWeaponSmokeGrenade"),
#     (0x2C804FE3, "VehicleWeaponStickyBomb"),
#     (0x84D676D4, "VehicleWeaponMolotov"),
#     (0x098D79EF, "VehicleHealth"),
#     (0x20796A82, "AmmoPistol"),
#     (0x116FC4E6, "AmmoSMG"),
#     (0xDE58E0B3, "AmmoMG"),
#     (0xE4BD2FC6, "AmmoRifle"),
#     (0x77F3F2DD, "AmmoShotgun"),
#     (0xC02CF125, "AmmoSniper"),
#     (0x881AB0A8, "AmmoGrenadeLauncher"),
#     (0x84837FD7, "AmmoRPG"),
#     (0xF25A01B9, "AmmoMinigun"),
#     (0xF99E15D0, "AmmoMissileMP"),
#     (0x550447A9, "AmmoBulletMP"),
#     (0x1069C3B8, "AmmoGrenadeLauncherMP")
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
    (0x802C0025, "IgnoreLights"),
    (0x000C00AB, "Normal (typically used by the game)"),
    (0x00000005, "Sometimes Overtake traffic"),
    (0x400C0025, "Rushed"),
    (0x000C0024, "Avoid traffic"),
    (0x00000006, "Avoid traffic extreme"),
    (0x00000034, "Avoid everything"),
    (0x00000023, "Careful driving"),
)


WEATHER_LIST = (
    ("EXTRASUNNY", "阳光明媚"),
    ("CLEAR", "晴朗"),
    ("CLOUDS", "多云"),
    ("SMOG", "霾"),
    ("FOGGY", "雾"),
    ("OVERCAST", "阴"),
    ("RAIN", "雨"),
    ("THUNDER", "雷阵雨"),
    ("CLEARING", "太阳雨"),
    ("NEUTRAL", "酸雨"),
    ("SNOW", "雪 (无光照)"),
    ("BLIZZARD", "暴风雪 (无光照)"),
    ("SNOWLIGHT", "雪"),
    ("XMAS", "圣诞雪"),
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
    (DIRECTION_FRONT, "前"),
    (DIRECTION_BACK, "后"),
    (DIRECTION_LEFT, "左"),
    (DIRECTION_RIGHT, "右"),
    (DIRECTION_ABOVE, "上"),
)
