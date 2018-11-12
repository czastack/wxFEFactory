# 无弹药数的武器分组
SLOT_NO_AMMO = [0, 1]

WEAPON_NONE = (0, 0, "无")

WEAPON_LIST = [
    [
        # (id, model, name)
        WEAPON_NONE,
    ],
    [
        # MELEE = 1
        WEAPON_NONE,
        (1, 0, "棒球棍"),
        (2, 0, "桌球杆"),
        (3, 0, "小刀"),
    ],
    [
        # HANDGUN = 2
        WEAPON_NONE,
        (7, 0, "手枪"),
        (9, 0, "沙漠之鹰"),
    ],
    [
        # SHOTGUN = 3
        WEAPON_NONE,
        (10, 0, "短管猎枪"),
        (11, 0, "贝雷塔猎枪"),
    ],
    [
        # SMG = 4
        WEAPON_NONE,
        (12, 0, "乌兹微冲"),
        (13, 0, "MP5"),
    ],
    [
        # RIFLE = 5
        WEAPON_NONE,
        (14, 0, "AK47"),
        (15, 0, "M4"),
    ],
    [
        # SNIPER = 6
        WEAPON_NONE,
        (16, 0, "狙击步枪"),
        (17, 0, "M40A1"),
    ],
    [
        # HEAVY = 7
        WEAPON_NONE,
        (18, 0, "火箭发射器"),
        (20, 0, "机枪"),
    ],
    [
        # THROWN = 8
        WEAPON_NONE,
        (4, 0, "手雷"),
        (5, 0, "燃烧瓶"),
    ],
]


VEHICLE_LIST = (
    ("汽车", (
        ("ADMIRAL", 0x4B5C5320),
        ("AIRTUG", 0x5D0AAC8F),
        ("AMBULANCE", 0x45D56ADA),
        ("BANSHEE", 0xC1E908D2),
        ("BENSON", 0x7A61B330),
        ("BIFF", 0x32B91AE8),
        ("BLISTA", 0xEB70965F),
        ("BOBCAT", 0x4020325C),
        ("BOXVILLE", 0x898ECCEA),
        ("BUCCANEER", 0xD756460C),
        ("BURRITO", 0xAFBB2CA4),
        ("BURRITO2", 0xC9E8FF76),
        ("BUS", 0xD577C962),
        ("CABBY", 0x705A3E41),
        ("CAVALCADE", 0x779F23AA),
        ("CHAVOS", 0xFBFD5B62),
        ("COGNOSCENTI", 0x86FE0B60),
        ("COMET", 0x3F637729),
        ("COQUETTE", 0x067BC037),
        ("DF8", 0x09B56631),
        ("DILETTANTE", 0xBC993509),
        ("DUKES", 0x2B26F456),
        ("E109", 0x8A765902),
        ("EMPEROR", 0xD7278283),
        ("EMPEROR2", 0x8FC3AADC),
        ("ESPERANTO", 0xEF7ED55D),
        ("FACTION", 0x81A9CDDF),
        ("FBI", 0x432EA949),
        ("FELTZER", 0xBE9075F1),
        ("FEROCI", 0x3A196CEA),
        ("FEROCI2", 0x3D285C4A),
        ("FIRETRUK", 0x73920F8E),
        ("FLATBED", 0x50B0215A),
        ("FORTUNE", 0x255FC509),
        ("FORKLIFT", 0x58E49664),
        ("FUTO", 0x7836CE2F),
        ("FXT", 0x28420460),
        ("HABANERO", 0x34B7390F),
        ("HAKUMAI", 0xEB9F21D3),
        ("HUNTLEY", 0x1D06D681),
        ("INFERNUS", 0x18F25AC7),
        ("INGOT", 0xB3206692),
        ("INTRUDER", 0x34DD8AA1),
        ("LANDSTALKER", 0x4BA4E8DC),
        ("LOKUS", 0xFDCAF758),
        ("MANANA", 0x81634188),
        ("MARBELLA", 0x4DC293EA),
        ("MERIT", 0xB4D8797E),
        ("MINIVAN", 0xED7EADA4),
        ("MOONBEAM", 0x1F52A43F),
        ("MRTASTY", 0x22C16A2F),
        ("MULE", 0x35ED670B),
        ("NOOSE", 0x08DE2A8B),
        ("NSTOCKADE", 0x71EF6313),
        ("ORACLE", 0x506434F6),
        ("PACKER", 0x21EEE87D),
        ("PATRIOT", 0xCFCFEB3B),
        ("PERENNIAL", 0x84282613),
        ("PERENNIAL2", 0xA1363020),
        ("PEYOTE", 0x6D19CCBC),
        ("PHANTOM", 0x809AA4CB),
        ("PINNACLE", 0x07D10BDC),
        ("PMP600", 0x5208A519),
        ("POLICE", 0x79FBB0C5),
        ("POLICE2", 0x9F05F101),
        ("POLPATRIOT", 0xEB221FC2),
        ("PONY", 0xF8DE29A8),
        ("PREMIER", 0x8FB66F9B),
        ("PRES", 0x8B0D2BA6),
        ("PRIMO", 0xBB6B404F),
        ("PSTOCKADE", 0x8EB78F5A),
        ("RANCHER", 0x52DB01E0),
        ("REBLA", 0x04F48FC4),
        ("RIPLEY", 0xCD935EF9),
        ("ROMERO", 0x2560B2FC),
        ("ROM", 0x8CD0264C),
        ("RUINER", 0xF26CEFF9),
        ("SABRE", 0xE53C7459),
        ("SABRE2", 0x4B5D021E),
        ("SABREGT", 0x9B909C94),
        ("SCHAFTER", 0xECC96C3F),
        ("SENTINEL", 0x50732C82),
        ("SOLAIR", 0x50249008),
        ("SPEEDO", 0xCFB3870C),
        ("STALION", 0x72A4C31E),
        ("STEED", 0x63FFE6EC),
        ("STOCKADE", 0x6827CF72),
        ("STRATUM", 0x66B4FC45),
        ("STRETCH", 0x8B13F083),
        ("SULTAN", 0x39DA2754),
        ("SULTANRS", 0xEE6024BC),
        ("SUPERGT", 0x6C9962A9),
        ("TAXI", 0xC703DB5F),
        ("TAXI2", 0x480DAF95),
        ("TRASH", 0x72435A19),
        ("TURISMO", 0x8EF34547),
        ("URANUS", 0x5B73F5B7),
        ("VIGERO", 0xCEC6B9B7),
        ("VIGERO2", 0x973141FC),
        ("VINCENT", 0xDD3BD501),
        ("VIRGO", 0xE2504942),
        ("VOODOO", 0x779B4F2D),
        ("WASHINGTON", 0x69F06B57),
        ("WILLARD", 0x737DAEC2),
        ("YANKEE", 0xBE6FF06A),
    )),

    ("摩托车", (
        ("BOBBER", 0x92E56A2C),
        ("FAGGIO", 0x9229E4EB),
        ("HELLFURY", 0x22DC8E7F),
        ("NRG900", 0x47B9138A),
        ("PCJ", 0xC9CEAF06),
        ("SANCHEZ", 0x2EF89E46),
        ("ZOMBIEB", 0xDE05FB87),
    )),

    ("直升机", (
        ("ANNIHILATOR", 0x31F0B376),
        ("MAVERICK", 0x9D0450CA),
        ("POLMAV", 0x1517D4D9),
        ("TOURMAV", 0x78D70477),
    )),

    ("船", (
        ("DINGHY", 0x3D961290),
        ("JETMAX", 0x33581161),
        ("MARQUIS", 0xC1CE1183),
        ("PREDATOR", 0xE2E7D4AB),
        ("REEFER", 0x68E27CB6),
        ("SQUALO", 0x17DF5EC2),
        ("TUGA", 0x3F724E66),
        ("TROPIC", 0x1149422F),
    )),

    ("列车(开不了)", (
        ("CABLECAR", 0xC6C3242D),
        ("SUBWAY_LO", 0x2FBC4D30),
        ("SUBWAY_HI", 0x8B887FDB),
    )),

    ("TBoGT 汽车", (
        ("SLAMVAN", 0x2B7F9DE3),
        ("CADDY", 0x44623884),
        ("APC", 0x2189D250),
        ("SUPERD", 0x42F2ED16),
        ("SUPERD2", 0x61A3B9BA),
        ("SERRANO", 0x4FB1A214),
        ("SERRANO2", 0x3EA948D6),
        ("BUFFALO", 0xEDD516C6),
        ("AVAN", 0xEF1E8F88),
        ("SCHAFTER2", 0xB52B5113),
        ("SCHAFTER3", 0xA774B5A6),
        ("BULLET", 0x9AE6DDA1),
        ("TAMPA", 0x39F9C898),
        ("CAVALCADE2", 0xD0EB2BE5),
        ("F620", 0xDCBCBE48),
        ("LIMO2", 0xF92AEC4D),
        ("POLICE3", 0x71FA16EA),
        ("POLICEW", 0x36299F36),
        ("POLICE4", 0x8A63C7B9),
        ("POLICEB", 0xFDEFAEC3),
    )),

    ("TBoGT 摩托车", (
        ("HEXER", 0x11F76C14),
        ("FAGGIO2", 0x0350D1AB),
        ("BATI2", 0xCADD5D2D),
        ("VADER", 0xF79A00F7),
        ("AKUMA", 0x63ABADE7),
        ("HAKUCHOU", 0x4B6C568A),
        ("DOUBLE", 0x9C669788),
    )),

    ("TBoGT 直升机", (
        ("BUZZARD", 0x2F03547B),
        ("SWIFT", 0xEBC24DF2),
        ("SKYLIFT", 0x3E48BF23),
    )),

    ("TBoGT 船", (
        ("SMUGGLER", 0x38527DEC),
        ("FLOATER", 0x98CC6F33),
        ("BLADE", 0xB820ED5E),
    )),

    ("TLAD 汽车", (
        ("GBURRITO", 0x97FA4F36),
        ("SLAMVAN", 0x2B7F9DE3),
        ("TOWTRUCK", 0xB12314E0),
        ("PACKER2", 0x0C5E290F),
        ("PBUS", 0x885F3671),
        ("YANKEE2", 0x8EDCFA90),
        ("RHAPSODY", 0x322CF98F),
        ("REGINA", 0xFF22D208),
        ("TAMPA", 0x39F9C898),
    )),

    ("TLAD 摩托车", (
        ("ANGEL", 0xDDF716D8),
        ("BATI", 0xF9300CC5),
        ("BATI2", 0xCADD5D2D),
        ("DAEMON", 0x77934CEE),
        ("DIABOLUS", 0xE7AD9DF9),
        ("DOUBLE", 0x9C669788),
        ("DOUBLE2", 0x971AB25B),
        ("HAKUCHOU", 0x4B6C568A),
        ("HAKUCHOU2", 0xF0C2A91F),
        ("HEXER", 0x11F76C14),
        ("INNOVATION", 0xF683EACA),
        ("LYCAN", 0x2FCECEB7),
        ("NIGHTBLADE", 0xA0438767),
        ("REVENANT", 0xEA9789D1),
        ("WAYFARER", 0xFB5D56B8),
        ("WOLFSBANE", 0xDB20A373),
    )),
)

EXPLOTION_TYPE = ('手榴弹', '燃烧瓶', '火箭弹', '摩托车', '汽车', '飞机')
