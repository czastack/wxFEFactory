RATE = ('1', '2', '4', '8', '16', '32', '64', '128')
EXP_RATE_VALUES = ()
PRO_RATE_VALUES = ()

STATUS = ('无', '毒', '睡', '沉默', '狂暴')

ITEMS = ()

CHAPTERS = ()

PROFESSIONS = ()
PROFESSION_VALUES = tuple(0x022716DC + i * 0x5C for i in range(len(PROFESSIONS)))

PROFICIENCYS = ('S级', 'A级', 'B级', 'C级', 'D级', 'E级', '-级')
PROFICIENCY_VALUES = (0xFB, 0xC9, 0x88, 0x4C, 0x1F, 0x01, 0x00)
PROFICIENCY_HINT = "00: -, 01: E, 1F: D, 4C: C, 88: B"

DIFFICULTY = ('正常', '难(1星)', '很难(2星)', '超难(3星)', '隐藏难度(4星)')
DIFFICULTY_VALUES = (0, 3, 4, 5, 6)

WEAPONTYPES = ("剑", "枪", "斧", "弓", "魔", "杖", "龙石", "弩车", "物品")


ITEM_ATTRS = (

)
