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

VEHICLE_LIST = (
    ("超级跑车", (
        ("培罗 T20", 0x6322B39A), # T20
        ("佩嘉西 奥西里斯", 0x767164D6), # OSIRIS
        ("旋风 狂雷", 0x9F4B77BE), # VOLTIC
        ("古罗帝 猎豹", 0xB1D95DA0), # CHEETAH
        ("古罗帝 披治 R", 0x185484E1), # TURISMOR
        ("傲弗拉 本质 XF", 0xB2FE5CF9), # ENTITYXF
        ("佩嘉西 炼狱魔", 0x18F25AC7), # INFERNUS
        ("佩嘉西 狂牛", 0x142E0DC3), # VACCA
        ("佩嘉西 桑托劳", 0xAC5DF515), # ZENTORNO
        ("特卢菲 灵蛇", 0xB779A091), # ADDER
        ("威皮 子弹", 0x9AE6DDA1), # BULLET
        ("卡林王者 RS", "SULTANRS"),
        ("冒险家 女妖900R", "BANSHEE2"),
    )),
    ("古惑跳跳车", (
        ("亚班尼 风流海盗改装版", 0xC397F748), # BUCCANEER2
        ("威皮 奇诺改装版", 0xAED64A63), # CHINO2
        ("威乐 宗派", 0x81A9CDDF), # FACTION
        ("威乐 宗派改装款", 0x95466BDB), # FACTION2
        ("威乐 宗派巨轮改装款", "FACTION3"),
        ("绝致 月光", 0x1F52A43F), # MOONBEAM
        ("绝致 月光改装款", 0x710A2B9B), # MOONBEAM2
        ("亚班尼 初代改装款", 0x86618EDA), # PRIMO2
        ("绝致 巫毒改装款", 0x779B4F2D), # VOODOO
        ("威皮 迷你厢行车改装款", "MINIVAN2"),
        ("绝緻 涡轮剑齿虎改装款", "SABREGT2"),
        ("威皮 帮派厢型车改装款", "SLAMVAN3"),
        ("绝致 旋风改装款", "TORNADO5"),
        ("亚班尼 室女2", "VIRGO2"),
        ("亚班尼 室女改装款", "VIRGO3"),
    )),
    ("跑车", (
        ("古罗帝 汗血宝马 硬顶敞篷版", 0x7B8AB45F), # CARBONIZZARE
        ("亚班尼 爱快", 0x2DB8D1AA), # ALPHA
        ("爱尼仕 輓歌 RH8", 0xDE3D9D22), # ELEGY2
        ("贝飞特 飞特者", 0x8911B9F5), # FELTZER2
        ("贝飞特 史瓦泽", 0xD37B7976), # SCHWARZER
        ("贝飞特 速雷", 0x16E478C1), # SURANO
        ("冒险家 女妖", 0xC1E908D2), # BANSHEE
        ("冒险家 猛牛", 0xEDD516C6), # BUFFALO
        ("冒险家 探险猛牛 S", 0x2BEC3CBE), # BUFFALO2
        ("冒险家 霜碧猛牛 S 赛车版", 0xE2C013E), # BUFFALO3
        ("浪子 马沙高", 0xF77ADE32), # MASSACRO
        ("浪子 马沙高 赛车版", 0xDA5819A3), # MASSACRO2
        ("浪子 疾速 GT", 0x8CB29A14), # RAPIDGT
        ("浪子 疾速 GT 敞篷版", 0x679450AF), # RAPIDGT2
        ("丁卡 小型旅行家", 0x3DEE5EDA), # BLISTA2
        ("丁卡 衝衝猴旅行家", 0xDCBC1C3B), # BLISTA3
        ("丁卡 小丑", 0xB2A716A3), # JESTER
        ("丁卡 小丑 赛车版", 0xBE0E6126), # JESTER2
        ("海角 变色龙", 0x206D1B68), # KHAMELION
        ("非凡 风情", 0x067BC037), # COQUETTE
        ("卡林 福多", 0x7836CE2F), # FUTO
        ("卡林 骷髅马", 0xAE2BFE94), # KURUMA
        ("卡林 骷髅马 (附装甲)", 0x187D938D), # KURUMA2
        ("卡林 王者", 0x39DA2754), # SULTAN
        ("兰帕达提 复仇女神 GT", 0xBF1691E0), # FUROREGT
        ("麦霸子 半影使者", 0xE9805550), # PENUMBRA
        ("奥北 9F", 0x3D8FA25C), # NINEF
        ("奥北 9F 敞篷版", 0xA8E38B01), # NINEF2
        ("菲斯特 陆上彗星", 0xC1AE4D16), # COMET2
        ("赛乐斯特 眩光", 0x1DC0BA53), # FUSILADE
    )),
    ("轿跑车", (
        ("埃努斯 温德莎", 0x5E4327C8), # WINDSOR
        ("埃努斯 至尊慧眼 硬顶敞篷版", 0x13B57D8A), # COGCABRIO
        ("绝品 卫士", 0x50732C82), # SENTINEL
        ("绝品 卫士 XS 硬顶敞篷版", 0x3412AE2D), # SENTINEL2
        ("兰帕达提 恶龙", 0xE8A8BDA8), # FELON
        ("兰帕达提 恶龙 GT 敞篷版", 0xFAAD85EE), # FELON2
        ("绝品 锡安", 0xBD1B39C3), # ZION
        ("绝品 天堂 敞篷版", 0xB8E2AE18), # ZION2
        ("浪子 典范", 0xFFB15B5E), # EXEMPLAR
        ("欧斯洛 F620", 0xDCBCBE48), # F620
        ("欧斯洛 豺狼", 0xDAC67112), # JACKAL
    )),
    ("经典跑车", (
        ("贝飞特 史特灵 GT", 0xA29D6D10), # FELTZER3
        ("亚班尼 明日之星", 0x81634188), # MANANA
        ("亚班尼 罗斯福", 0x06FF6914), # BTYPE
        ("勇气 罗斯福3", "BTYPE3"),
        ("勇气 罗斯福2", 0xCE6B35A4), # BTYPE2
        ("绝緻 旋风", 0x1BB290BC), # TORNADO
        ("绝緻 旋风 破旧版", 0x690A4153), # TORNADO3
        ("绝緻 旋风 敞篷版", 0x5B42A5C4), # TORNADO2
        ("绝緻 旋风 敞篷 破旧版", 0x86CF7CDD), # TORNADO4
        ("浪子 JB 700", 0x3EAB5555), # JB700
        ("古罗帝 史汀格", 0x5C23AF9B), # STINGER
        ("古罗帝 史汀格 GT", 0x82E499FA), # STINGERGT
        ("非凡 风情经典", 0x3C4E2113), # COQUETTE2
        ("兰帕达提 佳士可", 0x3822BDFE), # CASCO
        ("兰帕达提 皮卡乐", 0x404B6381), # PIGALLE
        ("佩嘉西 门罗", 0xE62B361B), # MONROE
        ("特卢菲 Z-Type", "ZTYPE"),
        ("威皮 佩优特", 0x6D19CCBC), # PEYOTE
    )),
    ("美式肌肉车", (
        ("威皮 奇诺", 0x14D69010), # CHINO
        ("非凡 风情黑鳍", 0x2EC385FE), # COQUETTE3
        ("亚班尼 室女", 0xE2504942), # VIRGO
        ("亚班尼 风流海盗", 0xD756460C), # BUCCANEER
        ("冒险家 铁腕", 0x94B395C5), # GAUNTLET
        ("冒险家 红木牌铁腕 赛车版", 0x14D22159), # GAUNTLET2
        ("雪佛 斗牛士", 0x59E0FBF3), # PICADOR
        ("绝緻 涡轮剑齿虎", 0x9B909C94), # SABREGT
        ("绝緻 公马", 0x72A4C31E), # STALION
        ("绝緻 吃得饱汉堡公马 赛车版", 0xE80F67EE), # STALION2
        ("绝緻 活力够", 0xCEC6B9B7), # VIGERO
        ("绝緻 巫毒", 0x1F3766E3), # VOODOO2
        ("英奔堤 死亡公爵", 0xEC8F7094), # DUKES2
        ("英奔堤 公爵", 0x2B26F456), # DUKES
        ("英奔堤 不死鸟", 0x831A21D5), # PHOENIX
        ("英奔堤 灭世暴徒", 0xF26CEFF9), # RUINER
        ("威皮 刀片", 0xB820ED5E), # BLADE
        ("威皮 统治者", 0x04CE68AC), # DOMINATOR
        ("威皮 统治者 赛车版", 0xC96B73D9), # DOMINATOR2
        ("威皮 热情使徒", 0x0239E390), # HOTKNIFE
        ("威皮 斯拉姆万", 0x2B7F9DE3), # SLAMVAN
        ("威皮 失落摩托车斯拉姆万", 0x31ADBBFC), # SLAMVAN2
    )),
    ("越野车", (
        ("旋风 斗殴者", 0xA7CE1BC5), # BRAWLER
        ("贝飞特 迪布达 6x6", 0xB6410173), # DUBSTA3
        ("毕福 必浮塔", 0xEB298297), # BIFTA
        ("毕福 沙丘征服者", 0x432AA566), # BFINJECTION
        ("毕福 沙丘魔宝", 0x9CF21E0F), # DUNE
        ("冒险家 越野游侠", 0x698521E3), # DLOADER
        ("冒险家 星际码头", 0x1FD824AF), # DUNE2
        ("卡尼斯 万用行者", 0xAA699BB6), # BODHI2
        ("卡尼斯 喀拉哈里", 0x05852838), # KALAHARI
        ("卡尼斯 岩魔", 0x84F42E51), # MESA3
        ("雪佛 马绍尔", 0x49863E9C), # MARSHALL
        ("绝緻 蓝彻 XL", 0x6210CBB0), # RANCHERXL
        ("绝緻 蓝彻 XL 雪地版", 0x7341576B), # RANCHERXL2
        ("HVY 叛乱分子", 0x7B7E56F0), # INSURGENT2
        ("HVY 叛乱分子 (带机枪)", 0x9114EADA), # INSURGENT
        ("卡林 叛逆男女", 0x8612B64B), # REBEL2
        ("卡林 叛逆男女 破旧版", 0xB802DD46), # REBEL
        ("卡林 铁尼高 (带机枪)", 0x83051506), # TECHNICAL
        ("长崎 烈焰", 0x8125BCF9), # BLAZER
        ("长崎 火爆烈焰骑士", 0xB44F0582), # BLAZER3
        ("长崎 烈焰救生型", 0xFD231729), # BLAZER2
        ("威皮 守护者", 0x825A9F4C), # GUARDIAN
        ("威皮 大脚霸王 SWB", 0x3AF8C345), # SANDKING2
        ("威皮 大脚霸王 XL", 0xB9210FD0), # SANDKING
        ("威皮 解放者 (美国旗帜)", 0xCD93A7DB), # MONSTER
    )),
    ("运动休旅车", (
        ("亚班尼 骑兵", 0x779F23AA), # CAVALCADE
        ("亚班尼 骑兵 Mk2", 0xD0EB2BE5), # CAVALCADE2
        ("贝飞特 迪布达", 0x462FE277), # DUBSTA
        ("贝飞特 迪布达 (亚光黑)", 0xE882E5F6), # DUBSTA2
        ("贝飞特 瑟雷诺", 0x4FB1A214), # SERRANO
        ("冒险家 情欲猎手", 0xA3FC0F4D), # GRESLEY
        ("卡尼斯岩魔", 0x36848602), # MESA
        ("卡尼斯岩魔 雪地版", 0xD36A4B44), # MESA2
        ("卡尼斯 陆上专家", 0x48CECED3), # SEMINOLE
        ("绝緻 屌王", 0x9628879C), # GRANGER
        ("敦追里 追捕者", 0x4BA4E8DC), # LANDSTALKER
        ("皇霸天 哈拔尼禄", 0x34B7390F), # HABANERO
        ("埃努斯 肯特利 S", 0x1D06D681), # HUNTLEY
        ("深水 FQ 2", 0xBC32A33B), # FQ2
        ("悠游 行者 (大) (路虎)", 0xCFCA3668), # BALLER
        ("悠游 行者 (小) (路虎)", 0x08852855), # BALLER2
        ("卡林 碧杰 XL", 0x32B29A4B), # BJXL
        ("巨象 爱国者", 0xCFCFEB3B), # PATRIOT
        ("奥北 小辣椒", 0x7F5C91F1), # ROCOTO
        ("威皮 辐光", 0x9D96B45B), # RADI
    )),
    ("轿车", (
        ("亚班尼 皇霸天", 0xD7278283), # EMPEROR
        ("亚班尼 皇霸天 破旧版", 0x8FC3AADC), # EMPEROR2
        ("亚班尼 皇霸天 雪地版", 0xB5FCF74E), # EMPEROR3
        ("亚班尼 初代", 0xBB6B404F), # PRIMO
        ("亚班尼 加长型礼车", 0x8B13F083), # STRETCH
        ("亚班尼 华盛顿", 0x69F06B57), # WASHINGTON
        ("贝飞特 格伦戴尔", 0x047A6BC1), # GLENDALE
        ("贝飞特 莎夫特", 0xB52B5113), # SCHAFTER2
        ("烈火马 钢骨灵车", 0x2560B2FC), # ROMERO
        ("万圣节 闹鬼灵车", 0x7B47A6A7), # LURCHER
        ("雪佛 流星", 0x71CB2FFB), # FUGITIVE
        ("雪佛 奔腾", 0x8F0E3594), # SURGE
        ("绝緻 海致", 0x94204D89), # ASEA
        ("绝緻 海致 雪地版", 0x9441D8D5), # ASEA2
        ("绝緻 统领", 0x8FB66F9B), # PREMIER
        ("敦追里 女皇", 0xFF22D208), # REGINA
        ("埃努斯 金钻耀星", 0x42F2ED16), # SUPERD
        ("卡林 爱硕普", 0x8E9254FB), # ASTEROPE
        ("卡林 入侵者", 0x34DD8AA1), # INTRUDER
        ("奥北 密探", 0xC3DDFDCE), # TAILGATER
        ("绝品 先知", 0x506434F6), # ORACLE
        ("绝品 先知 Mk2", 0xE18195B2), # ORACLE2
        ("威皮 史塔尼亚", 0xA7EDE74D), # STANIER
        ("威皮 (计程车)", 0xC703DB5F), # TAXI
        ("福狮 英卡特", 0xB3206692), # INGOT
        ("福狮 守护星", 0x51D83328), # WARRENER
        ("赛柯尼安 地层先锋", 0x66B4FC45), # STRATUM
    )),
    ("小型汽车", (
        ("贝飞特 哑剧", 0xE644E480), # PANTO
        ("包洛坎 原野行者", 0xA988D3A2), # PRAIRIE
        ("绝緻 狂想曲", 0x322CF98F), # RHAPSODY
        ("丁卡 旅行家", 0xEB70965F), # BLISTA
        ("卡林 爱快名人油电车", 0xBC993509), # DILETTANTE
        ("卡林 爱快名人油电车 (FlyUS)", 0x64430650), # DILETTANTE2
        ("威尼 天威", 0xB9CB3B69), # ISSI2
    )),
    ("皮卡", (
        ("冒险家 野牛", 0xFEFD644F), # BISON
        ("冒险家 野牛 (带后备架)", 0x67B3F020), # BISON3
        ("冒险家 野牛 (Construction)", 0x7B8297C5), # BISON2
        ("冒险家 老爷货车", 0xDCE1D9F7), # RATLOADER2
        ("冒险家 老爷货车 破旧版", 0xD83C13CE), # RATLOADER
        ("威皮 熊猫 XL", 0x3FC5D440), # BOBCATXL
        ("威皮 沙德勒", 0xDC434E51), # SADLER
        ("威皮 沙德勒 雪地版", 0x2BC345D1), # SADLER2
    )),
    ("厢型车", (
        ("毕福 乘风", 0x29B0DA97), # SURFER
        ("毕福 乘风 破旧版", 0xB1D80E06), # SURFER2
        ("冒险家 天堂", 0x58B3979C), # PARADISE
        ("冒险家 澜波 (Deludamol)", 0x961AFEF7), # RUMPO2
        ("冒险家 澜波 (Weazel News)", 0x4543B74D), # RUMPO
        ("冒险家 游侠", 0x03E5F6B8), # YOUGA
        ("威霸 露营车", 0x6FD95F68), # CAMPER
        ("威霸 小马 (商务)", 0xF8DE29A8), # PONY
        ("威霸 小马 (大麻商店)", 0x38408341), # PONY2
        ("玉米饼餐车", 0x744CA80D), # TACO
        ("绝緻 屌客", 0x98171BD3), # BURRITO3
        ("绝致 屌客 (Bug Stars)", 0xC9E8FF76), # BURRITO2
        ("绝致 屌客 (Construction)", 0x353B561D), # BURRITO4
        ("绝致 屌客帮派版 (Gang)", 0x11AA0E14), # GBURRITO2
        ("绝致 屌客 (Graphics)", 0xAFBB2CA4), # BURRITO
        ("绝致 屌客 雪地版", 0x437CF2A0), # BURRITO5
        ("绝致 屌客帮派版 (The Lost)", 0x97FA4F36), # GBURRITO
        ("威皮 迷你厢型车", 0xED7EADA4), # MINIVAN
        ("威皮 劲速", 0xCFB3870C), # SPEEDO
        ("威皮 小丑花车", 0x2B6DC64A), # SPEEDO2
        ("赛柯尼安 安旅者", 0xF8D48E7A), # JOURNEY
    )),
    ("商用、工业车", (
        ("威霸 厢村 (Go Postal)", 0xF21B33BE), # BOXVILLE2
        ("威霸 厢村 (Humane Labs)", 0x07405E08), # BOXVILLE3
        ("威霸 厢村 (Post OP)", 0x1A79847A), # BOXVILLE4
        ("威霸 厢村 (Water & Power)", 0x898ECCEA), # BOXVILLE
        ("威霸 拦截者", 0x6827CF72), # STOCKADE
        ("威霸 拦截者 (Snow)", 0xF337AB36), # STOCKADE3
        ("威霸 工地倾卸车 (Axle)", 0x02E19879), # TIPTRUCK
        ("威霸 工地倾卸车 (Axle2)", 0xC7824E5E), # TIPTRUCK2
        ("HVY 钻洞机", 0xC3FBA120), # CUTTER
        ("码头装卸车", 0x1A7FCEFA), # HANDLER
        ("码头拖车", 0xCB44B1CA), # DOCKTUG
        ("HVY 矿石搬运车", 0x810369E2), # DUMP
        ("HVY 倾卸车", 0x32B91AE8), # BIFF
        ("乔氏 搬运者", 0x5A82F9AE), # HAULER
        ("乔氏 魅影", 0x809AA4CB), # PHANTOM
        ("乔氏 砂通天", 0x9A5B1DCC), # RUBBLE
        ("麦霸子 猛骡 (外观 1)", 0x35ED670B), # MULE
        ("麦霸子 猛骡 (外观 2)", 0xC1632BEB), # MULE2
        ("麦霸子 猛骡 (普通)", 0x85A5B471), # MULE3
        ("HVY 混凝土搅拌车", 0xD138A6BB), # MIXER
        ("HVY 混凝土搅拌车 (带滚轮)", 0x1C534995), # MIXER2
        ("MTL 平板拖车", 0x50B0215A), # FLATBED
        ("MTL 车辆运送车", 0x21EEE87D), # PACKER
        ("MTL 跑德", 0x7DE35E7D), # POUNDER
        ("威皮 班森", 0x7A61B330), # BENSON
        ("废五金回收车", 0x9A9FD3DF), # SCRAP
        ("拖吊车", 0xB12314E0), # TOWTRUCK
        ("拖吊车 破旧版", 0xE5A2D6C6), # TOWTRUCK2
    )),
    ("服务类", (
        ("行李拖车", 0x5D0AAC8F), # AIRTUG
        ("机场巴士", 0x4C80EB0E), # AIRBUS
        ("巴士 (City Bus)", 0xD577C962), # BUS
        ("租用接驳巴士", 0xBE819C63), # RENTALBUS
        ("旅游巴士", 0x73B1C3CB), # TOURBUS
        ("缆车 (Mt. Chilliad)", 0xC6C3242D), # CABLECAR
        ("白狗巴士", 0x84718D34), # COACH
        ("HVY 推土机", 0x7074F39D), # BULLDOZER
        ("HVY 推高机", 0x58E49664), # FORKLIFT
        ("垃圾大王", 0xB527915C), # TRASH2
        ("垃圾大王 破旧版", 0x72435A19), # TRASH
        ("高尔夫球车 露天版", 0xDFF0594C), # CADDY2
        ("高尔夫球车", 0x44623884), # CADDY
        ("机场牵引车", 0xCD935EF9), # RIPLEY
        ("史丹利 农耕机", 0x843B73DE), # TRACTOR2
        ("史丹利 农耕机 雪地版", 0x562A97BD), # TRACTOR3
        ("割草车", 0x6A4BD8F6), # MOWER
        ("牵引机 破旧版", 0x61D6BA8C), # TRACTOR
        ("威皮 公共作业卡车", 0x7F2153DF), # UTILLITRUCK3
        ("威皮 公共作业卡车 Plus", 0x34E6BF6B), # UTILLITRUCK2
        ("威皮 高空作业车", 0x1ED0A534), # UTILLITRUCK
    )),
    ("拖车", (
        ("军用半挂拖车 (空)", 0xA7FF33F5), # ARMYTRAILER
        ("军用半挂拖车 (带钻洞机)", 0x9E6B14D6), # ARMYTRAILER2
        ("军用半挂拖车 油罐", 0xB8081009), # ARMYTANKER
        ("船拖车 小", 0x1F3D44B5), # BOATTRAILER
        ("船拖车 大 (带帆船)", 0x6A59902D), # TR3
        ("车辆运输拖车 (带超跑)", 0x7CAB34D0), # TR4
        ("车辆运输拖车 (空)", 0x7BE032C6), # TR2
        ("商业拖车 (Graphics 1)", 0xA1DA3C91), # TRAILERS2
        ("商业拖车 (Graphics 2)", 0x8548036D), # TRAILERS3
        ("集装箱拖车", 0x806EFBEE), # DOCKTRAILER
        ("集装箱拖车 (Fame or Shame)", 0x967620BE), # TVTRAILER
        ("平板拖车1", 0xD1ABB666), # FREIGHTTRAILER
        ("平板拖车2", 0xAF62F6B2), # TRFLAT
        ("粮用拖车", 0x3CC7F596), # GRAINTRAILER
        ("甘草捆专用拖车", 0xE82AE656), # BALETRAILER
        ("木材拖车", 0x782A236D), # TRAILERLOGS
        ("冰毒实验室拖车", 0x153E1B0A), # PROPTRAILER
        ("油罐拖车 (普通)", 0x74998082), # TANKER2
        ("油罐拖车 易燃 (RON)", 0xD46F4737), # TANKER
        ("普通拖车", 0xCBB2BE0E), # TRAILERS
        ("耙车", 0x174CB172), # RAKETRAILER
        ("小型拖车", 0x2A72BEAB), # TRAILERSMALL
    )),
    ("紧急车辆", (
        ("警用公路巡逻车 雪地版", 0x95F4C618), # POLICEOLD2
        ("救护车", 0x45D56ADA), # AMBULANCE
        ("军用部队运输车", 0xCEEA3F4B), # BARRACKS
        ("军用拖头", 0x4008EABB), # BARRACKS2
        ("FIB 公务车", 0x432EA949), # FBI
        ("警用防暴车", 0xB822A1AA), # RIOT
        ("卡斯尼 傲世铁骑 (迷彩)", 0x132D5A1A), # CRUSADER
        ("FIB 公务车 长", 0x9DC66994), # FBI2
        ("沙滩急救车", 0x1BF8D381), # LGUARD
        ("国家公园警用车", 0x2C33B46E), # PRANGER
        ("警用吉普车 雪地版", 0xA46462F7), # POLICEOLD1
        ("警用运输车", 0x1B38E955), # POLICET
        ("警用SUV", 0x72935408), # SHERIFF2
        ("消防车", 0x73920F8E), # FIRETRUK
        ("移监巴士", 0x885F3671), # PBUS
        ("犀式坦克", 0x2EA68690), # RHINO
        ("警用巡逻车1", 0x9F05F101), # POLICE2
        ("警用巡逻车2", 0x79FBB0C5), # POLICE
        ("警用巡逻车3", 0x71FA16EA), # POLICE3
        ("威皮 警长专用车", 0x9BAA707C), # SHERIFF
        ("威皮 无标志巡逻车", 0x8A63C7B9), # POLICE4
        ("警用机车", 0xFDEFAEC3), # POLICEB
    )),
    ("火车", (
        ("火车集装箱 1", 0x36DCFF98), # FREIGHTCONT1
        ("火车集装箱 2", 0x0E512E79), # FREIGHTCONT2
        ("火车车托", 0x0AFD22A6), # FREIGHTCAR
        ("火车车头", 0x3D6AAA9B), # FREIGHT
        ("火车货柜", 0x264D9262), # FREIGHTGRAIN
        ("电车 (一半)", 0x33C9E158), # METROTRAIN
        ("油罐", 0x22EDDC30), # TANKERCAR
    )),
    ("摩托车", (
        ("丁卡 装甲战车", 0xAF599F01), # VINDICATOR
        ("丁卡 街头恶魔", 0x63ABADE7), # AKUMA
        ("丁卡 双 T", 0x9C669788), # DOUBLE
        ("丁卡 恩迪罗", 0x6882FA73), # ENDURO
        ("丁卡 猛衝", 0x6D6F8F43), # THRUST
        ("LCC 迷魅光轮", 0x11F76C14), # HEXER
        ("LCC 创新", 0xF683EACA), # INNOVATION
        ("麦霸子 桑切斯", 0xA960B13E), # SANCHEZ2
        ("麦霸子 桑切斯 赛车版", 0x2EF89E46), # SANCHEZ
        ("长崎 碳纤 RS 型", 0x00ABB0C0), # CARBONRS
        ("佩嘉西 801 巴提", 0xF9300CC5), # BATI
        ("佩嘉西 801RR 巴提 赛车版", 0xCADD5D2D), # BATI2
        ("佩嘉西 恶霸", 0xCABD11E8), # RUFFIAN
        ("准则 雷克托", 0x26321E67), # LECTRO
        ("准则 复仇女神", 0xDA288376), # NEMESIS
        ("准则 费甲欧", 0x0350D1AB), # FAGGIO2
        ("诗津 白鸟", 0x4B6C568A), # HAKUCHOU
        ("诗津 PCJ 600", 0xC9CEAF06), # PCJ
        ("诗津 威德", 0xF79A00F7), # VADER
        ("西部 驮兽", 0x806B9CC3), # BAGGER
        ("西部 恶魔", 0x77934CEE), # DAEMON
        ("西部 君主", 0x2C509634), # SOVEREIGN
    )),
    ("飞机", (
        ("白金汉 乐梭豪华版", 0xB79F589E), # LUXOR2
        ("货机 An-225", 0x15F27762), # CARGOPLANE
        ("喷射机 B747", 0x3F119114), # JET
        ("白金汉 乐梭", 0x250B0C5E), # LUXOR
        ("白金汉 军用喷射机", 0x09D80F93), # MILJET
        ("白金汉 夏玛尔客机", 0xB79C1BF5), # SHAMAL
        ("白金汉 威斯特拉", 0x4FF77E37), # VESTRA
        ("乔氏 天行巨兽", 0x97E55D11), # MAMMATUS
        ("乔氏 P-996 天煞 战机", 0xB39B0AE6), # LAZER
        ("乔氏 梅杜莎 (4座)", 0x9C429B6A), # VELUM
        ("乔氏 梅杜莎 (5座)", 0x403820E8), # VELUM2
        ("巨象 都都鸟 水空两栖", 0xCA495705), # DODO
        ("巨象 九头蛇喷射机 武装", 0x39D6E83F), # HYDRA
        ("巨象 泰坦号 运输机", 0x761E2AD3), # TITAN
        ("西部 雀鹰 喷射型", 0x6CBD1D6D), # BESRA
        ("西部 古邦 800", 0xD9927FE3), # CUBAN800
        ("西部 洒药机", 0x39D6779E), # DUSTER
        ("特技飞机", 0x81794C70), # STUNT
    )),
    ("直升机", (
        ("白金汉 斯威夫特豪华版", 0x4019CB4C), # SWIFT2
        ("原子飞船", 0xF7004C86), # BLIMP
        ("希罗飞船", 0xDB6B4924), # BLIMP2
        ("白金汉 武装直升机", 0xFB133A17), # SAVAGE
        ("白金汉 斯威夫特", 0xEBC24DF2), # SWIFT
        ("白金汉 女武神 附机枪", 0xA09E15FD), # VALKYRIE
        ("HVY 吊挂直升机", 0x3E48BF23), # SKYLIFT
        ("麦霸子 穿梭者", 0x2C634FBD), # FROGGER
        ("麦霸子 穿梭者 (TPE/FIB)", 0x742E9AC0), # FROGGER2
        ("长崎 兀鹰直升机 (非武装)", 0x2C75F0DD), # BUZZARD2
        ("长崎 兀鹰攻击直升机", 0x2F03547B), # BUZZARD
        ("西部 歼灭者", 0x31F0B376), # ANNIHILATOR
        ("西部 运兵直升机 迷彩", 0xFCFCB68B), # CARGOBOB
        ("西部 运兵直升机 喷气式", 0x60A7EA10), # CARGOBOB2
        ("西部 运兵直升机 (TPE)", 0x53174EEF), # CARGOBOB3
        ("西部 小蛮牛", 0x9D0450CA), # MAVERICK
        ("西部 小蛮牛 (警用)", 0x1517D4D9), # POLMAV
    )),
    ("船舶", (
        ("兰帕达提 公牛", 0x3FD5AA2F), # TORO
        ("丁卡 水上侯爵", 0xC1CE1183), # MARQUIS
        ("克洛肯 潜水艇", 0xC07107EE), # SUBMERSIBLE2
        ("长崎 救生艇 (2座)", 0x107F392C), # DINGHY2
        ("长崎 救生艇 (4座 黑色)", 0x1E5E54EA), # DINGHY3
        ("长崎 救生艇 (4座 红色)", 0x3D961290), # DINGHY
        ("佩嘉西 飙速号", 0x0DC60D2B), # SPEEDER
        ("诗津 极限快艇", 0x33581161), # JETMAX
        ("诗津 警用追猎快艇", 0xE2E7D4AB), # PREDATOR
        ("诗津 思快乐快艇", 0x17DF5EC2), # SQUALO
        ("诗津 向阳号", 0xEF2295C9), # SUNTRAP
        ("诗津 烈阳号", 0x1149422F), # TROPIC
        ("水上枭雄 小海鲨", 0xC2974024), # SEASHARK
        ("水上枭雄 小海鲨 (救援)", 0xDB4388E4), # SEASHARK2
        ("潜水艇", 0x2DFF622F), # SUBMERSIBLE
    )),
    ("自行车", (
        ("BMX", 0x43779C54), # BMX
        ("巡航者", 0x1ABA13B5), # CRUISER
        ("Endurex 竞速车", 0xB67597EC), # TRIBIKE2
        ("费斯特", 0xCE23D3BF), # FIXTER
        ("先驱者", 0xF4E1AA15), # SCORCHER
        ("Tri-Cycles 竞速车", 0xE823FB48), # TRIBIKE3
        ("Whippet 竞速车", 0x4339CD69), # TRIBIKE
    )),
    ("进出口大亨 DLC", (
        ("长崎 水陆烈焰 越野车", "blazer5"),
        ("装甲厢村 厢型车", "boxville5"),
        ("菲斯特 陆上彗星仿古改装版 跑车", "comet3"),
        ("准则 蒂雅布罗 机车", "diablous"),
        ("准则 蒂雅布罗改装版 机车", "diablous2"),
        ("跳台魔宝改装版 越野车", "dune4"),
        ("跳台魔宝 越野车", "dune5"),
        ("卡林 水陆铁尼高 越野车", "technical2"),
        ("佩嘉西 泰皮斯达 超级跑车", "tempesta"),
        ("爱尼仕 挽歌仿古改装版 跑车", "elegy"),
        ("佩嘉西FCR 1000 机车", "fcr"),
        ("佩嘉西FCR 1000改装版 机车", "fcr2"),
        ("培罗 义塔力 GTB 超级跑车", "italigtb"),
        ("培罗 义塔力 GTB改装版 超级跑车", "italigtb2"),
        ("特卢菲 尼罗 超级跑车", "nero"),
        ("特卢菲 尼罗改装版 超级跑车", "nero2"),
        ("欧斯洛 摧花辣手 超级跑车", "penetrator"),
        ("浪子 史必特 跑车", "specter"),
        ("浪子 史必特改装版 跑车", "specter2"),
        ("旋风 火箭狂雷 超级跑车", "voltic2"),
        ("MTL 开慌者", "wastelander"),
        ("减世狂徒 跑车", "ruiner2"),
        ("减世狂徒破烂版 跑车", "ruiner3"),
    )),
    ("狂野车手 DLC", (
        ("LCC 阿瓦勒斯", "avarus"),
        ("长崎 街头烈焰", "blazer4"),
        ("长崎 奇美拉", "chimera"),
        ("恶魔", "daemon2"),
        ("诗津 亵渎者", "defiler"),
        ("爱时吉", "esskey"),
        ("佩嘉西 费甲欧现代版", "faggio"),
        ("佩嘉西 费甲欧摩登版", "faggio3"),
        ("诗津 白鸟竟速版", "hakuchou2"),
        ("麦霸子 曼切兹", "manchez"),
        ("西部 暗夜魅影", "nightblade"),
        ("猛禽", "raptor"),
        ("西部 破烂机车", "ratbike"),
        ("圣者之行", "sanctus"),
        ("正太郎", "shotaro"),
        ("西部 破烂科学怪人", "tornado6"),
        ("猛冲", "vortex"),
        ("西部 狂狼克星", "wolfsbane"),
        ("经典游侠", "youga2"),
        ("西部 捶尸者", "zombiea"),
        ("西部 斩尸者", "zombieb"),
    )),
    ("情人节&万圣节 DLC", (
        ("亚班尼 罗斯福勇气", "btype3"),
        ("冒险家 女妖900R", "banshee2"),
        ("卡林 王者 RS", "sultanrs"),
        ("亚班尼 科学怪人", "btype2"),
        ("亚班尼 闹鬼灵车", "lurcher"),
    )),
    ("低底盘跳跳车 DLC", (
        ("威皮 奇诺改装款", "chino2"),
        ("威皮 迷你厢型车改装款", "minivan2"),
        ("威皮 斯拉姆万改装款", "slamvan3"),
        ("绝緻 涡轮剑齿虎改装款", "sabregt2"),
        ("绝緻 旋风改装款", "tornado5"),
        ("绝緻 月光改装款", "moonbeam2"),
        ("绝緻 巫毒改装款", "voodoo"),
        ("敦追里 经典室女改装款", "virgo2"),
        ("敦追里 经典室女", "virgo3"),
        ("威勒 宗派改装巨轮款", "faction3"),
        ("威勒 宗派改装款", "faction2"),
        ("亚班尼 风流海盗改装款", "buccaneer2"),
        ("亚班尼 初代改装款", "primo2"),
    )),
    ("炫炮特技 DLC", (
        ("长崎 BF400", "bf400"),
        ("古罗帝 精力霸 R/A", "brioso"),
        ("西部 高潮", "cliffhanger"),
        ("威皮 争夺者", "contender"),
        ("西部 石像兽", "gargoyle"),
        ("爱尼仕 RE-7B", "le7b"),
        ("欧斯洛 山猫", "lynx"),
        ("奥北 全路线尊者", "omnis"),
        ("MTL 山丘", "rallytruck"),
        ("皇霸天 ETR1", "sheava"),
        ("绝致 甩尾坦帕", "tampa2"),
        ("威皮 越野卡车", "trophytruck"),
        ("威皮 沙漠突击", "trophytruck2"),
        ("兰帕达提 脱普斯拉力", "tropos"),
        ("培罗 泰勒斯", "tyrus"),
    )),
    ("富贵险中求", (
        ("新式直升飞机", "volatus"),
        ("古罗帝 X80 概念款", "prototipo"),
        ("佩嘉西  死神", "reaper"),
        ("冒险家 澜波改装款", "rumpo3"),
        ("浪子 柒-70", "seven70"),
        ("拖船 ", "tug"),
        ("埃努斯 温莎德开蓬板", "windsor2"),
        ("古罗帝 猛兽 GTS", "bestiagts"),
        ("HVY 贝凯迪", "brickade"),
        ("威皮 FMJ", "fmj"),
        ("白金汉 尼姆巴思", "nimbus"),
        ("菲斯特 811", "pfister811"),
        ("贝飞特 XLS", "xls"),
        ("贝飞特 XLS（附装甲）", "xls2"),
    )),
    ("权贵天下", (
        ("悠游 行者 LE", "baller3"),
        ("悠游 行者 LE 长轴车", "baller4"),
        ("悠游 行者 LE (附装甲）", "baller5"),
        ("悠游 行者 LE 长轴车 (附装甲）", "baller6"),
        ("埃努斯 至尊慧眼 55", "cog55"),
        ("埃努斯 至尊慧眼 55 (附装甲）", "cog552"),
        ("埃努斯 至尊慧眼", "cognoscenti"),
        ("埃努斯 至尊慧眼 (附装甲）", "cognoscenti2"),
        ("贝菲特 莎夫特 V12", "schafter3"),
        ("贝菲特 莎夫特长轴车", "schafter4"),
        ("贝菲特 莎夫特 V12 (附装甲）", "schafter5"),
        ("贝菲特 莎夫特长轴车 (附装甲）", "schafter6"),
        ("贝菲特 武装礼车", "limo2"),
        ("冒险家 迷失者", "verlierer2"),
        ("绝致 曼巴", "mamba"),
        ("英奔堤 暗夜魅影", "nightshade"),
        ("运兵 直升机", "cargobob4"),
        ("女武神 原装版", "valkyrie2"),
        ("白金汉 超级伏里托碳几型", "supervolito2"),
        ("白金汉 超级伏里托", "supervolito"),
        ("长崎 救生艇", "dinghy4"),
        ("水上枭雄 小鱼鲨", "seashark3"),
        ("佩嘉西 飙速号", "speeder2"),
        ("诗津 烈阳号", "tropic2"),
    )),
)


# 角色模型
PLAYER_MODEL = (
    ("主角", (
        ("麦克", "player_zero"),
        ("富兰克林", "player_one"),
        ("崔佛", "player_two"),
    )),
    
    ("动物", (
        ("野猪", "a_c_boar"),
        ("家猪", "a_c_pig"),
        
        ("黑猩猩", "a_c_chimp"),
        ("恒河猴", "a_c_rhesus"),
        
        ("母牛", "a_c_cow"),
        ("鹿", "a_c_deer"),
        
        ("小查", "a_c_chop"),
        ("狼", "a_c_coyote"),
        ("哈士奇", "a_c_husky"),
        ("猎犬", "a_c_retriever"),
        ("德国牧羊犬", "a_c_shepherd"),
        ("贵宾犬", "a_c_poodle"),
        ("巴哥犬", "a_c_pug"),
        ("罗威那", "a_c_rottweiler"),
        ("西高地白梗", "a_c_westy"),
        
        ("鱼", "a_c_fish"),
        ("海豚", "a_c_dolphin"),
        ("座头鲸", "a_c_humpback"),
        ("逆戟鲸", "a_c_killerwhale"),
        ("鎚头鲨", "a_c_sharkhammer"),
        ("虎鲨", "a_c_sharktiger"),
        ("黄貂鱼", "a_c_stingray"),
        
        ("猫", "a_c_cat_01"),
        ("山狮", "a_c_mtlion"),
        
        ("老鼠", "a_c_rat"),
        ("兔子", "a_c_rabbit_01"),
        
        ("鹰", "a_c_chickenhawk"),
        ("鸬鹚", "a_c_cormorant"),
        ("乌鸦", "a_c_crow"),
        ("鸽子", "a_c_pigeon"),
        ("海鸥", "a_c_seagull"),
        ("母鸡", "a_c_hen"),
    )),
    
    ("FIB IAA", (
        ("安德列斯·桑切斯 FIB探员 (CS)", "cs_andreas"),
        ("安德列斯·桑切斯 FIB探员 (IG)", "ig_andreas"),
        ("戴夫·诺顿 FIB探员 (CS)", "cs_davenorton"),
        ("戴夫·诺顿 FIB探员 (IG)", "ig_davenorton"),
        ("FIB 探员", "u_m_m_fibarchitect"),
        ("FIB 抢劫犯", "u_m_y_fibmugger_01"),
        ("FIB 办公人员1", "s_m_m_fiboffice_01"),
        ("FIB 办公人员2", "s_m_m_fiboffice_02"),
        ("FIB 保安人员", "mp_m_fibsec_01"),
        ("FIB 制服男 (CS)", "cs_fbisuit_01"),
        ("FIB 制服男 (IG)", "ig_fbisuit_01"),
        ("蜜雪儿(凯伦) IAA特工 (CS)", "cs_michelle"),
        ("蜜雪儿(凯伦) IAA特工 (IG)", "ig_michelle"),
        ("斯蒂夫·海因斯 FIB探员 (CS)", "cs_stevehains"),
        ("斯蒂夫·海因斯 FIB探员 (IG)", "ig_stevehains"),
        ("UL.Paper IAA特工 (CS)", "cs_paper"),
        ("UL.Paper IAA特工 (IG)", "ig_paper"),
    )),

    ("按区域划分", (
        ("亚美尼亚老板", "g_m_m_armboss_01"),
        ("亚美尼亚打手1", "g_m_m_armgoon_01"),
        ("亚美尼亚打手2", "g_m_y_armgoon_02"),
        ("亚美尼亚中年男子", "g_m_m_armlieut_01"),
        ("海滩救援队 女队员", "s_f_y_baywatch_01"),
        ("海滩救援队 男队员", "s_m_y_baywatch_01"),
        ("海滩女", "a_f_m_beach_01"),
        ("海滩男1", "a_m_m_beach_01"),
        ("海滩男2", "a_m_m_beach_02"),
        ("海滩肌肉男1", "a_m_y_musclbeac_01"),
        ("海滩肌肉男2", "a_m_y_musclbeac_02"),
        ("海滩的老头", "a_m_o_beach_01"),
        ("海滩流浪女", "a_f_m_trampbeac_01"),
        ("海滩流浪汉", "a_m_m_trampbeac_01"),
        ("海滩少女", "a_f_y_beach_01"),
        ("海滩男青年1", "a_m_y_beach_01"),
        ("海滩男青年2", "a_m_y_beach_02"),
        ("海滩男青年3", "a_m_y_beach_03"),
        ("贝芙丽山庄的女性1", "a_f_m_bevhills_01"),
        ("贝芙丽山庄的女性2", "a_f_m_bevhills_02"),
        ("贝芙丽山庄的男性1", "a_m_m_bevhills_01"),
        ("贝芙丽山庄的男性2", "a_m_m_bevhills_02"),
        ("贝芙丽山庄的年轻女性1", "a_f_y_bevhills_01"),
        ("贝芙丽山庄的年轻女性2", "a_f_y_bevhills_02"),
        ("贝芙丽山庄的年轻女性3", "a_f_y_bevhills_03"),
        ("贝芙丽山庄的年轻女性4", "a_f_y_bevhills_04"),
        ("贝芙丽山庄的年轻男性1", "a_m_y_bevhills_01"),
        ("贝芙丽山庄的年轻男性2", "a_m_y_bevhills_02"),
        ("街头黑人男子1", "a_m_y_stbla_01"),
        ("街头黑人男子2", "a_m_y_stbla_02"),
        ("华人老板", "g_m_m_chiboss_01"),
        ("华人打手", "g_m_m_chigoon_01"),
        ("华人打手", "csb_chin_goon"),
        ("华人打手2", "g_m_m_chigoon_02"),
        ("老牌的华人打手", "g_m_m_chicold_01"),
        ("市中心的女性", "a_f_m_downtown_01"),
        ("市中心的男性", "a_m_y_downtown_01"),
        ("SA东部女性1", "a_f_m_eastsa_01"),
        ("SA东部女性2", "a_f_m_eastsa_02"),
        ("SA东部男性1", "a_m_m_eastsa_01"),
        ("SA东部男性2", "a_m_m_eastsa_02"),
        ("SA东部年轻女性1", "a_f_y_eastsa_01"),
        ("SA东部年轻女性2", "a_f_y_eastsa_02"),
        ("SA东部年轻女性3", "a_f_y_eastsa_03"),
        ("SA东部年轻男性1", "a_m_y_eastsa_01"),
        ("SA东部年轻男性2", "a_m_y_eastsa_02"),
        ("街边老太", "a_f_o_genstreet_01"),
        ("街边老头", "a_m_o_genstreet_01"),
        ("意大利裔美国年轻男性", "u_m_y_guido_01"),
        ("印度男性", "a_m_m_indian_01"),
        ("印度老年女性", "a_f_o_indian_01"),
        ("印度年轻女性", "a_f_y_indian_01"),
        ("印度年轻男性", "a_m_y_indian_01"),
        ("韩国老板", "g_m_m_korboss_01"),
        ("韩国女性", "a_f_m_ktown_01"),
        ("韩国妇女", "a_f_m_ktown_02"),
        ("韩国西装男", "g_m_y_korlieut_01"),
        ("韩国中年男子", "a_m_m_ktown_01"),
        ("韩国老太", "a_f_o_ktown_01"),
        ("韩国老头", "a_m_o_ktown_01"),
        ("韩国男青年", "g_m_y_korean_01"),
        ("韩国男青年", "a_m_y_ktown_01"),
        ("韩国男青年2", "g_m_y_korean_02"),
        ("韩国男青年2", "a_m_y_ktown_02"),
        ("拉丁裔男勤杂工", "s_m_m_lathandy_01"),
        ("拉丁裔街头男子", "a_m_m_stlat_02"),
        ("拉丁裔街头男青年", "a_m_y_stlat_01"),
        ("拉丁裔男青年", "a_m_y_latino_01"),
        ("马里布青年", "a_m_m_malibu_01"),
        ("墨西哥男子", "csb_ramp_mex"),
        ("墨西哥男子 (IG)", "ig_ramp_mex"),
        ("墨西哥老板1", "g_m_m_mexboss_01"),
        ("墨西哥老板2", "g_m_m_mexboss_02"),
        ("墨西哥团伙成员", "g_m_y_mexgang_01"),
        ("墨西哥打手1", "g_m_y_mexgoon_01"),
        ("墨西哥打手2", "g_m_y_mexgoon_02"),
        ("墨西哥打手3", "g_m_y_mexgoon_03"),
        ("墨西哥工人", "a_m_m_mexlabor_01"),
        ("墨西哥农民", "a_m_m_mexcntry_01"),
        ("墨西哥暴徒", "a_m_y_mexthug_01"),
        ("波利尼西亚人", "a_m_m_polynesian_01"),
        ("波利尼西亚的打手1", "g_m_y_pologoon_01"),
        ("波利尼西亚的打手2", "g_m_y_pologoon_02"),
        ("波利尼西亚的青年", "a_m_y_polynesian_01"),
        ("俄罗斯醉汉 (CS)", "cs_russiandrunk"),
        ("俄罗斯醉汉 (IG)", "ig_russiandrunk"),
        ("索尔顿女性", "a_f_m_salton_01"),
        ("索尔顿男子1", "a_m_m_salton_01"),
        ("索尔顿男子2", "a_m_m_salton_02"),
        ("索尔顿男子3", "a_m_m_salton_03"),
        ("索尔顿男子4", "a_m_m_salton_04"),
        ("索尔顿老年女性", "a_f_o_salton_01"),
        ("索尔顿老年男性", "a_m_o_salton_01"),
        ("索尔顿男青年", "a_m_y_salton_01"),
        ("萨尔瓦多老板", "g_m_y_salvaboss_01"),
        ("萨尔瓦多打手1", "g_m_y_salvagoon_01"),
        ("萨尔瓦多打手2", "g_m_y_salvagoon_02"),
        ("萨尔瓦多打手3", "g_m_y_salvagoon_03"),
        ("贫民窟的女性", "a_f_m_skidrow_01"),
        ("贫民窟的男性", "a_m_m_skidrow_01"),
        ("中南部女性1", "a_f_m_soucent_01"),
        ("中南部女性2", "a_f_m_soucent_02"),
        ("中南部拉丁裔男", "a_m_m_socenlat_01"),
        ("中南部男性1", "a_m_m_soucent_01"),
        ("中南部男性2", "a_m_m_soucent_02"),
        ("中南部男性3", "a_m_m_soucent_03"),
        ("中南部男性4", "a_m_m_soucent_04"),
        ("中南部MC女性", "a_f_m_soucentmc_01"),
        ("中南部老年女性1", "a_f_o_soucent_01"),
        ("中南部老年女性2", "a_f_o_soucent_02"),
        ("中南部老年男性1", "a_m_o_soucent_01"),
        ("中南部老年男性2", "a_m_o_soucent_02"),
        ("中南部老年男性3", "a_m_o_soucent_03"),
        ("中南部年轻女性1", "a_f_y_soucent_01"),
        ("中南部年轻女性2", "a_f_y_soucent_02"),
        ("中南部年轻女性3", "a_f_y_soucent_03"),
        ("中南部年轻男性1", "a_m_y_soucent_01"),
        ("中南部年轻男性2", "a_m_y_soucent_02"),
        ("中南部年轻男性3", "a_m_y_soucent_03"),
        ("中南部年轻男性4", "a_m_y_soucent_04"),
        ("威斯普奇海滩男1", "a_m_y_beachvesp_01"),
        ("威斯普奇海滩男2", "a_m_y_beachvesp_02"),
        ("好麦坞讨厌鬼", "a_m_y_vindouche_01"),
        ("好麦坞女性1", "a_f_y_vinewood_01"),
        ("好麦坞女性2", "a_f_y_vinewood_02"),
        ("好麦坞女性3", "a_f_y_vinewood_03"),
        ("好麦坞女性4", "a_f_y_vinewood_04"),
        ("好麦坞男性1", "a_m_y_vinewood_01"),
        ("好麦坞男性2", "a_m_y_vinewood_02"),
        ("好麦坞男性3", "a_m_y_vinewood_03"),
        ("好麦坞男性4", "a_m_y_vinewood_04"),
    )),

    ("角色", (
        ("艾比盖尔", "csb_abigail"),
        ("艾比盖尔 (IG)", "ig_abigail"),
        ("霍洛维兹 医生", "u_m_y_abner"),
        ("非洲裔男子", "a_m_m_afriamer_01"),
        ("艾尔·迪·拿波里", "u_m_m_aldinapoli"),
        ("亚曼达·迪圣塔 (CS)", "cs_amandatownley"),
        ("亚曼达·迪圣塔 (IG)", "ig_amandatownley"),
        ("安妮塔·门多萨", "csb_anita"),
        ("安东·鲍德雷 导演", "csb_anton"),
        ("安东·鲍德雷 导演", "u_m_y_antonb"),
        ("阿什利·巴特勒 (CS)", "cs_ashley"),
        ("阿什利·巴特勒 (IG)", "ig_ashley"),
        ("巴瑞 (CS)", "cs_barry"),
        ("巴瑞 (IG)", "ig_barry"),
        ("最好的男人 (IG)", "ig_bestmen"),
        ("比佛利 新闻狗仔 (CS)", "cs_beverly"),
        ("比佛利 新闻狗仔 (IG)", "ig_beverly"),
        ("布莱德·斯奈德 (CS)", "cs_brad"),
        ("布莱德·斯奈德 (IG)", "ig_brad"),
        ("布莱德的上半身尸体 (CS)", "cs_bradcadaver"),
        ("新娘", "csb_bride"),
        ("新娘 (IG)", "ig_bride"),
        ("Car 3 Guy 1", "csb_car3guy1"),
        ("Car 3 Guy 1 (IG)", "ig_car3guy1"),
        ("Car 3 Guy 2", "csb_car3guy2"),
        ("Car 3 Guy 2 (IG)", "ig_car3guy2"),
        ("克劳德·斯皮德", "mp_m_claude_01"),
        ("克雷·杰克逊 (说唱歌手PG) (IG)", "ig_claypain"),
        ("克雷·西蒙斯 (The Lost) (CS)", "cs_clay"),
        ("克雷·西蒙斯 (The Lost) (IG)", "ig_clay"),
        ("克莱", "csb_cletus"),
        ("克莱 (IG)", "ig_cletus"),
        ("戴尔 (CS)", "cs_dale"),
        ("戴尔 (IG)", "ig_dale"),
        ("戴博拉 (CS)", "cs_debra"),
        ("丹妮斯 (CS)", "cs_denise"),
        ("丹妮斯 (IG)", "ig_denise"),
        ("丹尼斯的朋友", "csb_denise_friend"),
        ("德凡·韦斯顿 亿万富翁 (CS)", "cs_devin"),
        ("德凡·韦斯顿 亿万富翁 (IG)", "ig_devin"),
        ("德凡的保镖", "s_m_y_devinsec_01"),
        ("多姆(唐姆)·比斯利 (CS)", "cs_dom"),
        ("多姆(唐姆)·比斯利 (IG)", "ig_dom"),
        ("费兰德 心理医生 (CS)", "cs_drfriedlander"),
        ("费兰德 心理医生 (IG)", "ig_drfriedlander"),
        ("法比恩 瑜伽教练 (CS)", "cs_fabien"),
        ("法比恩 瑜伽教练 (IG)", "ig_fabien"),
        ("费迪南·科廖夫 K先生 (CS)", "cs_mrk"),
        ("费迪南·科廖夫 K先生 (IG)", "ig_mrk"),
        ("弗洛伊德 (CS)", "cs_floyd"),
        ("弗洛伊德 (IG)", "ig_floyd"),
        ("自由言论代表", "csb_fos_rep"),
        ("G", "csb_g"),
        ("格裡夫", "u_m_m_griff_01"),
        ("新郎", "csb_groom"),
        ("新郎 (IG)", "ig_groom"),
        ("格洛夫街的交易者", "csb_grove_str_dlr"),
        ("Guadalope (CS)", "cs_guadalope"),
        ("Gurk (CS)", "cs_gurk"),
        ("阿浩", "csb_hao"),
        ("阿浩 (IG)", "ig_hao"),
        ("休·威尔斯 (枪手)", "csb_hugh"),
        ("伊姆兰", "csb_imran"),
        ("简", "u_f_y_comjane"),
        ("珍妮特 (CS)", "cs_janet"),
        ("珍妮特 (IG)", "ig_janet"),
        ("杰·诺裡斯 (IG)", "ig_jay_norris"),
        ("杰斯科·怀特 乡下的踢踏舞者", "u_m_o_taphillbilly"),
        ("耶稣", "u_m_m_jesus_01"),
        ("珠宝抢劫案的司机", "hc_driver"),
        ("珠宝抢劫案的枪手", "hc_gunman"),
        ("珠宝抢劫案的骇客", "hc_hacker"),
        ("珠宝窃贼", "u_m_m_jewelthief"),
        ("珠宝商保安人员", "u_m_m_jewelsec_01"),
        ("吉米·波士顿 (CS)", "cs_jimmyboston"),
        ("吉米·波士顿 (IG)", "ig_jimmyboston"),
        ("吉米·迪圣塔 (CS)", "cs_jimmydisanto"),
        ("吉米·迪圣塔 (IG)", "ig_jimmydisanto"),
        ("约翰·马斯顿 荒野大镖客乱入", "mp_m_marston_01"),
        ("强尼·克雷比兹 (CS)", "cs_johnnyklebitz"),
        ("强尼·克雷比兹 (IG)", "ig_johnnyklebitz"),
        ("约瑟夫 (CS)", "cs_josef"),
        ("约瑟夫 (IG)", "ig_josef"),
        ("贾许 (CS)", "cs_josh"),
        ("贾许 (IG)", "ig_josh"),
        ("凯莉·麦金塔 (IG)", "ig_kerrymcintosh"),
        ("拉玛·戴维斯 (CS)", "cs_lamardavis"),
        ("拉玛·戴维斯 (IG)", "ig_lamardavis"),
        ("雷兹罗 (CS)", "cs_lazlow"),
        ("雷兹罗 (IG)", "ig_lazlow"),
        ("莱斯特·克雷斯 (CS)", "cs_lestercrest"),
        ("莱斯特·克雷斯 (IG)", "ig_lestercrest"),
        ("爱拳威利 (团体成员)", "u_m_m_willyfist"),
        ("摩尼 (头顶墨西哥大圆帽)", "u_m_y_mani"),
        ("Manuel (CS)", "cs_manuel"),
        ("Manuel (IG)", "ig_manuel"),
        ("墨西哥流浪乐队艺人", "s_m_m_mariachi_01"),
        ("马克·佛森", "u_m_m_markfost"),
        ("玛妮·艾伦 (CS)", "cs_marnie"),
        ("玛妮·艾伦 (IG)", "ig_marnie"),
        ("马丁·马德拉索 (CS)", "cs_martinmadrazo"),
        ("玛丽安·奎因 (CS)", "cs_maryann"),
        ("玛丽安·奎因 (IG)", "ig_maryann"),
        ("茉德夫人", "csb_maude"),
        ("茉德夫人 (IG)", "ig_maude"),
        ("米尔顿 (CS)", "cs_milton"),
        ("米尔顿 (IG)", "ig_milton"),
        ("民兵 乔伊 (CS)", "cs_joeminuteman"),
        ("民兵 乔伊 (IG)", "ig_joeminuteman"),
        ("米兰达", "u_f_m_miranda"),
        ("米丝蒂", "mp_f_misty_01"),
        ("茉莉 (CS)", "cs_molly"),
        ("茉莉 (IG)", "ig_molly"),
        ("电影中的宇航员", "s_m_m_movspace_01"),
        ("电影导演", "u_m_m_filmdirector"),
        ("电影首映礼女主", "s_f_y_movprem_01"),
        ("电影首映礼女主 (CS)", "cs_movpremf_01"),
        ("电影首映礼男主", "s_m_m_movprem_01"),
        ("电影首映礼男主 (CS)", "cs_movpremmale"),
        ("电影女明星", "u_f_o_moviestar"),
        ("菲利普夫人 (CS)", "cs_mrsphillips"),
        ("菲利普夫人 (IG)", "ig_mrsphillips"),
        ("桑希尔夫人 (CS)", "cs_mrs_thornhill"),
        ("桑希尔夫人 (IG)", "ig_mrs_thornhill"),
        ("娜塔莉亚 黑帮女 (CS)", "cs_natalia"),
        ("娜塔莉亚 黑帮女 (IG)", "ig_natalia"),
        ("紧张的罗恩 (CS)", "cs_nervousron"),
        ("紧张的罗恩 (IG)", "ig_nervousron"),
        ("奈吉 (CS)", "cs_nigel"),
        ("奈吉 (IG)", "ig_nigel"),
        ("尼克·贝里克 (4代主角)", "mp_m_niko_01"),
        ("OG 老板", "a_m_m_og_boss_01"),
        ("奥米伽 (CS)", "cs_omega"),
        ("奥米伽 (IG)", "ig_omega"),
        ("欧尼尔兄弟 (IG)", "ig_oneil"),
        ("欧铁佳", "csb_ortega"),
        ("欧铁佳 (IG)", "ig_ortega"),
        ("奥斯卡 (墨西哥佬)", "csb_oscar"),
        ("派翠莎 (CS)", "cs_patricia"),
        ("派翠莎 (IG)", "ig_patricia"),
        ("彼得·德莱弗森 (CS)", "cs_dreyfuss"),
        ("彼得·德莱弗森 (IG)", "ig_dreyfuss"),
        ("波比·米雪尔", "u_f_y_poppymich"),
        ("色情男", "csb_porndudes"),
        ("公主", "u_f_y_princess"),
        ("序章的司机", "u_m_y_proldriver_01"),
        ("序章的司机", "csb_prologuedriver"),
        ("序章的女主", "a_f_m_prolhost_01"),
        ("序章的男主", "a_m_m_prolhost_01"),
        ("序章的老年妇女", "u_f_o_prolhost_01"),
        ("序章的葬礼服女性", "u_f_m_promourn_01"),
        ("序章的葬礼服男性", "u_m_m_promourn_01"),
        ("共和党的太空游侠", "u_m_y_rsranger_01"),
        ("洛克·佩洛西", "csb_roccopelosi"),
        ("洛克·佩洛西 (IG)", "ig_roccopelosi"),
        ("西蒙·叶特裡恩 车行老板 (CS)", "cs_siemonyetarian"),
        ("西蒙·叶特裡恩 车行老板 (IG)", "ig_siemonyetarian"),
        ("所罗门·理查德 (CS)", "cs_solomon"),
        ("所罗门·理查德 (IG)", "ig_solomon"),
        ("史崔奇 (CS)", "cs_stretch"),
        ("史崔奇 (IG)", "ig_stretch"),
        ("塔丽娜 (IG)", "ig_talina"),
        ("塔妮莎 小富前女友 (CS)", "cs_tanisha"),
        ("塔妮莎 小富前女友 (IG)", "ig_tanisha"),
        ("陈涛 (CS)", "cs_taocheng"),
        ("陈涛 (IG)", "ig_taocheng"),
        ("陈涛的翻译员 (CS)", "cs_taostranslator"),
        ("陈涛的翻译员 (IG)", "ig_taostranslator"),
        ("泰瑞 (CS)", "cs_terry"),
        ("泰瑞 (IG)", "ig_terry"),
        ("汤姆 (CS)", "cs_tom"),
        ("谭雅", "csb_tonya"),
        ("谭雅 (IG)", "ig_tonya"),
        ("崔西(特雷西)·迪圣塔 (CS)", "cs_tracydisanto"),
        ("崔西(特雷西)·迪圣塔 (IG)", "ig_tracydisanto"),
        ("泰勒狄克逊 (IG)", "ig_tylerdix"),
        ("韦德 (CS)", "cs_wade"),
        ("韦德 (IG)", "ig_wade"),
        ("陈伟 (CS)", "cs_chengsr"),
        ("陈伟 (IG)", "ig_chengsr"),
        ("Zimbor (CS)", "cs_zimbor"),
        ("Zimbor (IG)", "ig_zimbor"),
        ("丧尸", "u_m_y_zombie_01"),
    )),

    ("军警", (
        ("武装国度 市级弹药员", "s_m_y_ammucity_01"),
        ("武装国度 村级弹药员", "s_m_m_ammucountry"),
        ("装甲车保安人员", "mp_s_m_armoured_01"),
        ("装甲车保安人员", "s_m_m_armoured_01"),
        ("装甲车保安人员2", "s_m_m_armoured_02"),
        ("陆军机械师", "s_m_y_armymech_01"),
        ("黑色行动 士兵1", "s_m_y_blackops_01"),
        ("黑色行动 士兵2", "s_m_y_blackops_02"),
        ("保镖", "s_m_m_bouncer_01"),
        ("僱佣警卫 Casey (CS)", "cs_casey"),
        ("僱佣警卫 Casey (IG)", "ig_casey"),
        ("男警员", "csb_cop"),
        ("年轻女警察", "s_f_y_cop_01"),
        ("年轻男警察", "s_m_y_cop_01"),
        ("退役军人", "mp_m_exarmy_01"),
        ("烧伤的退役军人", "u_m_y_militarybum"),
        ("消防员", "s_m_y_fireman_01"),
        ("Grip", "s_m_y_grip_01"),
        ("高级保镖1", "s_m_m_highsec_01"),
        ("高级保镖2", "s_m_m_highsec_02"),
        ("高速公路警员", "s_m_y_hwaycop_01"),
        ("IAA保安人员", "s_m_m_ciasec_01"),
        ("海军1", "csb_ramp_marine"),
        ("海军2", "s_m_m_marine_01"),
        ("海军长官", "s_m_m_marine_02"),
        ("年轻海军士兵1", "s_m_y_marine_01"),
        ("年轻海军士兵2", "s_m_y_marine_02"),
        ("年轻海军士兵3", "s_m_y_marine_03"),
        ("梅利威瑟僱佣兵", "csb_mweather"),
        ("战斗机飞行员1", "s_m_y_pilot_01"),
        ("战斗机飞行员2", "s_m_m_pilot_02"),
        ("监狱看守", "s_m_m_prisguard_01"),
        ("序章的保安1", "csb_prolsec"),
        ("序章的保安1", "u_m_m_prolsec_01"),
        ("序章的保安2 (CS)", "cs_prolsec_02"),
        ("序章的保安2 (IG)", "ig_prolsec_02"),
        ("女警员", "s_f_y_ranger_01"),
        ("男警员", "s_m_y_ranger_01"),
        ("保安", "s_m_m_security_01"),
        ("女警官", "s_f_y_sheriff_01"),
        ("男警官", "s_m_y_sheriff_01"),
        ("雪地男员警", "s_m_m_snowcop_01"),
        ("SWAT特警", "s_m_y_swat_01"),
        ("交通协警", "csb_trafficwarden"),
        ("交通协警 (IG)", "ig_trafficwarden"),
        ("美国海岸警卫队员", "s_m_y_uscg_01"),
    )),

    ("某一类群体", (
        ("男舞者", "a_m_y_breakdance_01"),
        ("商务休閒男", "a_m_y_busicas_01"),
        ("商务女士2", "a_f_m_business_02"),
        ("商务男子", "a_m_m_business_01"),
        ("商务年轻女性1", "a_f_y_business_01"),
        ("商务年轻女性2", "a_f_y_business_02"),
        ("商务年轻女性3", "a_f_y_business_03"),
        ("商务年轻女性4", "a_f_y_business_04"),
        ("商务年轻男性1", "a_m_y_business_01"),
        ("商务年轻男性2", "a_m_y_business_02"),
        ("商务年轻男性3", "a_m_y_business_03"),
        ("街头艺人", "s_m_o_busker_01"),
        ("买车的人 (CS)", "cs_carbuyer"),
        ("Chip", "u_m_y_chip"),
        ("客人", "csb_customer"),
        ("毒品贩子", "s_m_y_dealer_01"),
        ("门卫", "s_m_y_doorman_01"),
        ("时髦女性", "a_f_y_scdressy_01"),
        ("肥胖的黑人女性", "a_f_m_fatbla_01"),
        ("裸露的胖女人", "a_f_m_fatcult_01"),
        ("肥胖的拉丁裔男", "a_m_m_fatlatin_01"),
        ("肥胖的白人女性", "a_f_m_fatwhite_01"),
        ("健身操女性1", "a_f_y_fitness_01"),
        ("健身操女性2", "a_f_y_fitness_02"),
        ("同性恋男子1", "a_m_y_gay_01"),
        ("同性恋男子2", "a_m_y_gay_02"),
        ("男胖子1", "a_m_m_genfat_01"),
        ("男胖子2", "a_m_m_genfat_02"),
        ("辣妹", "a_f_y_genhot_01"),
        ("大街上的青年1", "a_m_y_genstreet_01"),
        ("大街上的青年2", "a_m_y_genstreet_02"),
        ("高尔夫球男子", "u_m_m_glenstank_01"),
        ("高尔夫男子", "a_m_m_golfer_01"),
        ("高尔夫年轻女子", "a_f_y_golfer_01"),
        ("高尔夫年轻男子", "a_m_y_golfer_01"),
        ("枪支供应商", "u_m_y_gunvend_01"),
        ("乡巴佬", "csb_ramp_hic"),
        ("乡巴佬 (IG)", "ig_ramp_hic"),
        ("乡下男1", "a_m_m_hillbilly_01"),
        ("乡下男2", "a_m_m_hillbilly_02"),
        ("嬉皮女", "a_f_y_hippie_01"),
        ("嬉皮男", "u_m_y_hippie_01"),
        ("嬉皮男", "a_m_y_hippy_01"),
        ("时髦男", "csb_ramp_hipster"),
        ("时髦男 (IG)", "ig_ramp_hipster"),
        ("时髦的女性1", "a_f_y_hipster_01"),
        ("时髦的女性2", "a_f_y_hipster_02"),
        ("时髦的女性3", "a_f_y_hipster_03"),
        ("时髦的女性4", "a_f_y_hipster_04"),
        ("时髦的男性1", "a_m_y_hipster_01"),
        ("时髦的男性2", "a_m_y_hipster_02"),
        ("时髦的男性3", "a_m_y_hipster_03"),
        ("时髦美女", "u_f_y_hotposh_01"),
        ("看门人", "csb_janitor"),
        ("看门人", "s_m_m_janitor"),
        ("神经质女性", "a_f_y_juggalo_01"),
        ("神经质男性", "a_m_y_juggalo_01"),
        ("品红染髮女 (CS)", "cs_magenta"),
        ("品红染髮女 (IG)", "ig_magenta"),
        ("瘾君子", "a_m_y_methhead_01"),
        ("外来女工", "s_f_y_migrant_01"),
        ("外来男工", "s_m_m_migrant_01"),
        ("默剧艺术家", "s_m_y_mime"),
        ("情妇", "u_f_y_mistress"),
        ("老人1 (CS)", "cs_old_man1a"),
        ("老人1 (IG)", "ig_old_man1a"),
        ("老人2 (CS)", "cs_old_man2"),
        ("老人2 (IG)", "ig_old_man2"),
        ("派对主人", "u_m_m_partytarget"),
        ("派对上的男子", "u_m_y_party_01"),
        ("囚犯", "s_m_y_prisoner_01"),
        ("囚犯", "u_m_y_prisoner_01"),
        ("囚犯 (肌肉)", "s_m_y_prismuscl_01"),
        ("面罩男", "mp_g_m_pros_01"),
        ("土匪 (劫匪)", "s_m_y_robber_01"),
        ("农村吸毒女", "a_f_y_rurmeth_01"),
        ("农村吸毒男", "a_m_m_rurmeth_01"),
        ("店主", "mp_m_shopkeep_01"),
        ("单身派对的新郎", "u_m_y_staggrm_01"),
        ("街头表演者", "s_m_m_strperf_01"),
        ("街头传教士", "s_m_m_strpreach_01"),
        ("街头朋克1", "g_m_y_strpunk_01"),
        ("街头朋克2", "g_m_y_strpunk_02"),
        ("街头小贩", "s_m_m_strvend_01"),
        ("年轻的街头小贩", "s_m_y_strvend_01"),
        ("晒日光浴的男性", "a_m_y_sunbathe_01"),
        ("观光女", "a_f_m_tourist_01"),
        ("观光男", "a_m_m_tourist_01"),
        ("观光女青年1", "a_f_y_tourist_01"),
        ("观光女青年2", "a_f_y_tourist_02"),
        ("流浪女", "a_f_m_tramp_01"),
        ("流浪汉", "a_m_m_tramp_01"),
        ("流浪的老头2", "u_m_o_tramp_01"),
        ("流浪的老头2", "a_m_o_tramp_01"),
        ("街头白人男子1", "a_m_y_stwhi_01"),
        ("街头白人男子2", "a_m_y_stwhi_02"),
    )),

    ("特殊、奇葩", (
        ("外星人", "s_m_m_movalien_01"),
        ("小D (肌肉猛男)", "u_m_y_babyd"),
        ("大脚猩猩 (CS)", "cs_orleans"),
        ("大脚猩猩 (IG)", "ig_orleans"),
        ("年轻女性尸体1", "u_f_y_corpse_01"),
        ("年轻女性尸体2", "u_f_y_corpse_02"),
        ("死去的妓女", "mp_f_deadhooker"),
        ("女性模型", "mp_f_freemode_01"),
        ("男性模型", "mp_m_freemode_01"),
        ("超级英雄 (无能狂怒人)", "u_m_y_imporage"),
        ("变性人", "u_m_y_justin"),
        ("猴子POGO", "u_m_y_pogo_01"),
        ("露胸女", "a_f_y_topless_01"),
        ("异装癖男性1", "a_m_m_tranvest_01"),
        ("异装癖男性2", "a_m_m_tranvest_02"),
    )),

    ("运动", (
        ("骑自行车的时尚女性", "u_f_y_bikerchic"),
        ("体形健硕的女人", "a_f_m_bodybuild_01"),
        ("自行车极限运动车手", "a_m_y_dhill_01"),
        ("女漫步者", "a_f_y_hiker_01"),
        ("男漫步者", "a_m_y_hiker_01"),
        ("女慢跑者", "a_f_y_runner_01"),
        ("男慢跑者1", "a_m_y_runner_01"),
        ("男慢跑者2", "a_m_y_runner_02"),
        ("摩托车手1", "a_m_y_motox_01"),
        ("摩托车手2", "a_m_y_motox_02"),
        ("公路自行车选手", "a_m_y_roadcyc_01"),
        ("滑板女青年", "a_f_y_skater_01"),
        ("滑板的男子", "a_m_m_skater_01"),
        ("滑板青年1", "a_m_y_skater_01"),
        ("滑板青年2", "a_m_y_skater_02"),
        ("衝浪者", "a_m_y_surfer_01"),
        ("瑜伽女", "a_f_y_yoga_01"),
        ("瑜伽男", "a_m_y_yoga_01"),
    )),

    ("职业群体", (
        ("空姐", "s_f_y_airhostess_01"),
        ("航空工作人员", "s_m_y_airworker"),
        ("尸体解剖员", "s_m_y_autopsy_01"),
        ("汽车店员工1", "s_m_m_autoshop_01"),
        ("汽车店员工2", "s_m_m_autoshop_02"),
        ("银行经理 (CS)", "cs_bankman"),
        ("银行经理 (IG)", "ig_bankman"),
        ("银行经理，男", "u_m_m_bankman"),
        ("女理髮师", "s_f_m_fembarber"),
        ("酒保", "s_m_y_barman_01"),
        ("女酒保", "s_f_y_bartender_01"),
        ("农村酒保", "s_m_m_cntrybar_01"),
        ("出租自行车的男子", "u_m_m_bikehire_01"),
        ("汉堡店职员", "csb_burgerdrug"),
        ("汉堡店职员", "u_m_y_burgerdrug_01"),
        ("吧台男", "s_m_y_busboy_01"),
        ("厨师", "s_m_y_chef_01"),
        ("厨师 (CS)", "csb_chef"),
        ("厨师 (IG)", "ig_chef"),
        ("化工厂安全人员", "s_m_m_chemsec_01"),
        ("化工厂工作者", "g_m_m_chemwork_01"),
        ("小丑", "s_m_y_clown_01"),
        ("建筑工人1", "s_m_y_construct_01"),
        ("建筑工人2", "s_m_y_construct_02"),
        ("产房护士", "u_f_m_corpse_01"),
        ("自行车骑手2", "a_m_y_cyclist_01"),
        ("自行车骑手2", "u_m_y_cyclist_01"),
        ("码头工人", "s_m_m_dockwork_01"),
        ("码头工人", "s_m_y_dockwork_01"),
        ("医生", "s_m_m_doctor_01"),
        ("DW机场工作人员1", "s_m_y_dwservice_01"),
        ("DW机场工作人员2", "s_m_y_dwservice_02"),
        ("加工厂女职工", "s_f_y_factory_01"),
        ("加工厂男职工", "s_m_y_factory_01"),
        ("农民", "a_m_m_farmer_01"),
        ("金融师", "u_m_o_finguru_01"),
        ("装修工", "s_m_m_gaffer_01"),
        ("垃圾工", "s_m_y_garbage"),
        ("园丁", "s_m_m_gardener_01"),
        ("理髮师", "s_m_m_hairdress_01"),
        ("妓女1", "s_f_y_hooker_01"),
        ("妓女2", "s_f_y_hooker_02"),
        ("妓女3", "s_f_y_hooker_03"),
        ("医院工作的女性", "s_f_y_scrubs_01"),
        ("猎人 (CS)", "cs_hunter"),
        ("猎人 (IG)", "ig_hunter"),
        ("汽艇驾驶员", "a_m_y_jetski_01"),
        ("珠宝商助理", "u_f_y_jewelass_01"),
        ("珠宝商助理 (CS)", "cs_jewelass"),
        ("珠宝商助理 (IG)", "ig_jewelass"),
        ("侵入生活公司员工 (CS)", "cs_lifeinvad_01"),
        ("侵入生活公司员工 (IG)", "ig_lifeinvad_01"),
        ("侵入生活公司员工2 (IG)", "ig_lifeinvad_02"),
        ("侵入生活公司男职员 (IG)", "s_m_m_lifeinvad_01"),
        ("厨师", "s_m_m_linecook"),
        ("LS地铁工人男", "s_m_m_lsmetro_01"),
        ("女僕", "s_f_m_maid_01"),
        ("机修师1", "s_m_y_xmech_01"),
        ("机修师2", "s_m_y_xmech_02"),
        ("狗仔队男", "a_m_m_paparazzi_01"),
        ("狗仔队男青年", "u_m_y_paparazzi"),
        ("护理人员", "s_m_m_paramedic_01"),
        ("害虫防治人员", "s_m_y_pestcont_01"),
        ("机长", "s_m_m_pilot_01"),
        ("邮政员工1", "s_m_m_postal_01"),
        ("邮政员工2", "s_m_m_postal_02"),
        ("牧师 (CS)", "cs_priest"),
        ("牧师 (IG)", "ig_priest"),
        ("男记者", "csb_reporter"),
        ("竞争的狗仔队", "u_m_m_rivalpap"),
        ("销售员 (高级)", "s_f_m_shop_high"),
        ("销售员 (普通)", "s_f_y_shop_low"),
        ("销售员 (面具店)", "s_m_y_shop_mask"),
        ("销售员 (Mid-Price)", "s_f_y_shop_mid"),
        ("科学家", "s_m_m_scientist_01"),
        ("编剧", "csb_screen_writer"),
        ("编剧 (IG)", "ig_screen_writer"),
        ("自行车运动员", "u_m_y_sbike"),
        ("间谍演员", "u_m_m_spyactor"),
        ("间谍演员 女", "u_f_y_spyactress"),
        ("脱衣舞女", "csb_stripper_01"),
        ("脱衣舞女", "s_f_y_stripper_01"),
        ("脱衣舞女2", "csb_stripper_02"),
        ("脱衣舞女2", "s_f_y_stripper_02"),
        ("脱衣舞女 Lite", "s_f_y_stripperlite"),
        ("脱衣舞女 Lite", "mp_f_stripperlite"),
        ("血汗工厂的工人", "s_f_m_sweatshop_01"),
        ("血汗工厂的年轻工人", "s_f_y_sweatshop_01"),
        ("纹身艺术家", "u_m_y_tattoo_01"),
        ("网球教练 (CS)", "cs_tenniscoach"),
        ("网球教练 (IG)", "ig_tenniscoach"),
        ("网球女选手", "a_f_y_tennis_01"),
        ("网球男选手", "a_m_m_tennis_01"),
        ("运输工人男", "s_m_m_gentransport"),
        ("卡车司机", "s_m_m_trucker_01"),
        ("UPS快递司机1", "s_m_m_ups_01"),
        ("UPS快递司机2", "s_m_m_ups_02"),
        ("代泊车服务员", "s_m_y_valet_01"),
        ("服务员", "s_m_y_waiter_01"),
        ("窗户清洁工", "s_m_y_winclean_01"),
    )),

    ("宗教、帮派", (
        ("利他邪教的暴露男", "a_m_m_acult_01"),
        ("利他邪教 裸露的老年男子1", "a_m_o_acult_01"),
        ("利他邪教 裸露的老年男子2", "a_m_o_acult_02"),
        ("利他邪教 裸露的年轻男子1", "a_m_y_acult_01"),
        ("利他邪教 裸露的年轻男子2", "a_m_y_acult_02"),
        ("阿兹提克帮派男子", "g_m_y_azteca_01"),
        ("巴勒帮东部青年", "g_m_y_ballaeast_01"),
        ("巴勒帮派女子", "g_f_y_ballas_01"),
        ("巴勒帮老大 D", "csb_ballasog"),
        ("巴勒帮老大 D (IG)", "ig_ballasog"),
        ("巴勒帮派男性 (IG)", "g_m_y_ballaorig_01"),
        ("巴勒帮南方青年", "g_m_y_ballasout_01"),
        ("克裡斯 埃普西隆教主 (CS)", "cs_chrisformage"),
        ("克裡斯 埃普西隆教主 (IG)", "ig_chrisformage"),
        ("埃普西隆邪教 女成员", "a_f_y_epsilon_01"),
        ("埃普西隆邪教 男成员1", "a_m_y_epsilon_01"),
        ("埃普西隆邪教 男成员2", "a_m_y_epsilon_02"),
        ("埃普西隆邪教 汤姆 (CS)", "cs_tomepsilon"),
        ("埃普西隆邪教 汤姆 (IG)", "ig_tomepsilon"),
        ("CA家族男性", "g_m_y_famca_01"),
        ("DD家族男性", "mp_m_famdd_01"),
        ("DNF家族男性", "g_m_y_famdnf_01"),
        ("某家族女性", "g_f_y_families_01"),
        ("FOR家族男性", "g_m_y_famfor_01"),
        ("家族成员", "csb_ramp_gang"),
        ("家族成员 (IG)", "ig_ramp_gang"),
        ("哈西德教派 犹太男", "a_m_m_hasjew_01"),
        ("哈西德教派 年轻犹太男", "a_m_y_hasjew_01"),
        ("至高基辅隆 教徒", "u_m_y_baygor"),
        ("失落摩托车队 女", "g_f_y_lost_01"),
        ("失落摩托车队 男1", "g_m_y_lost_01"),
        ("失落摩托车队 男2", "g_m_y_lost_02"),
        ("失落摩托车队 男3", "g_m_y_lost_03"),
        ("维戈斯帮派女子", "g_f_y_vagos_01"),
    )),
)


OBJECT_MODEL = (
    ('易爆物体', (
        ('气泵a', 'prop_gas_pump_1a'),
        ('气泵b', 'prop_gas_pump_1b'),
        ('气泵c', 'prop_gas_pump_1c'),
        ('气泵d', 'prop_gas_pump_1d'),
        ('气缸01a', 'prop_gas_tank_01a'),
        ('气缸02a', 'prop_gas_tank_02a'),
        ('气缸02b', 'prop_gas_tank_02b'),
        ('气缸04a', 'prop_gas_tank_04a'),
        ('气罐01a', 'prop_gascyl_01a'),
        ('气罐02a', 'prop_gascyl_02a'),
        ('气罐02b', 'prop_gascyl_02b'),
        ('气罐03a', 'prop_gascyl_03a'),
        ('气罐03b', 'prop_gascyl_03b'),
        ('气罐04a', 'prop_gascyl_04a'),
    )),
)


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