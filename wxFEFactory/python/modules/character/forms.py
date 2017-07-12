from lib.form import fm, BaseForm

class CharacterForm(BaseForm):
    addr = 0x00858288
    title = "角色"

    fields = [
        fm.Uint("addr", "地址", 0),
        fm.Text("name", "名字", 2),
        fm.Text("title", "R键说明", 2),
        fm.Uint("id", "人物ID", 1),
        # fm.SimpleSelect("profession", "职业", 1),
        fm.Uint("bigPortrait", "大头像", 1),
        fm.Uint("unknown1", "未知", 1),
        fm.Uint("smallPortrait", "小头像", 1),
        # fm.SimpleSelect("attribute", "属性", 1),
        fm.Uint("unknown2", "未知", 1),

        fm.Group("initial", "初始能力值", [
            fm.Uint("level", "等级", 1),
            fm.Uint("hp", "HP", 1),
            fm.Uint("power", "力/魔力", 1),
            fm.Uint("skill", "技术", 1),
            fm.Uint("speed", "速度", 1),
            fm.Uint("defense", "防御", 1),
            fm.Uint("magicDef", "魔防", 1),
            fm.Uint("lucky", "幸运", 1),
            fm.Uint("physique", "体格+", 1),
        ]),

        fm.Group("prof", "武器熟练度", [
            fm.Uint("sword", "剑", 1),
            fm.Uint("spear", "枪", 1),
            fm.Uint("axe", "斧", 1),
            fm.Uint("arch", "弓", 1),
            fm.Uint("wand", "杖", 1),
            fm.Uint("physics", "理", 1),
            fm.Uint("light", "光", 1),
            fm.Uint("dark", "暗", 1),
        ]),

        fm.Group("growth", "职业成长率", [
            fm.Uint("hp", "HP", 1),
            fm.Uint("power", "力/魔", 1),
            fm.Uint("skill", "技术", 1),
            fm.Uint("speed", "速度", 1),
            fm.Uint("defense", "防御", 1),
            fm.Uint("magicDef", "魔防", 1),
            fm.Uint("lucky", "幸运", 1),
        ]),

        fm.Uint("lowLevelProfColor", "低级职业配色方案", 1),
        fm.Uint("highLevelProfColor", "高级职业配色方案", 1),
        fm.Uint("lowLevelProfMode", "低级职业战斗造型", 1),
        fm.Uint("highLevelProfMode", "高级职业战斗造型", 1),
        fm.Uint("unknown3", "未知", 1),
        # fm.FlagSelect("ability1", "能力1", 1),
        # fm.FlagSelect("ability2", "能力2", 1),
        # fm.FlagSelect("ability3", "能力3", 1),
        # fm.FlagSelect("ability4", "能力4", 1),
        fm.Bytes("supportPtr", "支援指针", 4),
        fm.Uint("unknown4", "未知", 1),
        fm.Uint("unknown5", "未知", 1),
        fm.Uint("unknown6", "未知", 1),
        fm.Uint("unknown7", "未知", 1),
    ]
