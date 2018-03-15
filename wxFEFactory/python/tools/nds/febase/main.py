from ..base import BaseNdsHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
import fefactory_api
ui = fefactory_api.ui


class FeTool(BaseNdsHack):

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self.item_index = 1
    
    def render_main(self):
        datasets = self.datasets
        
        with Group("global", "全局", self._global, cols=4):
            ModelInput("money", "金钱")
            ModelInput("turns", "回合")
            ModelCheckBox("ourturn", "总是我方回合", enableData=0xE3A01001, disableData=0xE5D01000)
            ModelCheckBox("control_enemy", "可控制敌人", enableData=0xE1500000, disableData=0xE1510000)
            ModelCheckBox("upgrade_max", "升级能力值最大", enableData=0xB1A06004, disableData=0xB2866001)
            ModelCheckBox("upgrade_all", "升级全能力提升", enableData=0xE1A00000, disableData=0xAA000009)
            ModelCheckBox("lv1_can_transfer", "Lv1即可转职", enableData=0x00000001, disableData=0xE350000A)
            ModelCheckBox("can_train", "都可用运输队", enableData=0xE3A00002, disableData=0xEBF98E8F)
            ModelCheckBox("can_visit", "都可访问村庄", enableData=0xE3A00002, disableData=0xEBF98B4C)
            ModelCheckBox("can_holddown", "都可压制", enableData=0xE3A00002, disableData=0xEBF98F1B)
            ModelCheckBox("use_enemy_prof", "使用敌专用兵种不死机", enableData=0xEA000022, disableData=0x1A000022)
            ModelCheckBox("infinite_refine", "武器屋炼成无限次", enableData=0, disableData=0xE3)
            ModelCheckBox("item_consume", "道具耐久不减", enableData=0x12400000, disableData=0x12400001)
            ModelCheckBox("item_consume", "敌人全道具掉落", enableData=0xE3500000E1D006B0, disableData=0xE3100020E5D00063)
            ModelSelect("exp_rate", "经验值倍数", None, None, datasets.RATE, datasets.EXP_RATE_VALUES)
            ModelSelect("pro_rate", "熟练度倍数", None, None, datasets.RATE, datasets.PRO_RATE_VALUES)
            # ModelInput("random", "乱数").view.setToolTip("设成0: 招招命中、必杀、贯通等，升级7点成长")
            # ModelSelect("chapter", "章节", None, None, datasets.CHAPTERS)

        with Group("player", "配置", self._config, cols=4):
            ModelSelect("difficulty", "难易度", None, None, datasets.DIFFICULTY, datasets.DIFFICULTY_VALUES)
            ModelSelect("character_gender", "主人公性别", None, None, datasets.CHARACTER_GENDER)
            ModelSelect("character_hair_style", "主人公发色", None, None, datasets.CHARACTER_HAIR_STYLE)
            ModelSelect("character_hair_color", "主人公发型", None, None, datasets.CHARACTER_HAIR_COLOR)
            ModelSelect("character_eye", "主人公眼睛", None, None, datasets.CHARACTER_EYE)
            ModelSelect("character_cloth", "主人公服装", None, None, datasets.CHARACTER_CLOTH)

        with Group("player", "角色", self._person, cols=4):
            ModelInput("addr_hex", "地址", readonly=True)
            ModelInput("no", "序号")
            ModelSelect("prof", "职业", None, None, datasets.PROFESSIONS, datasets.PROFESSION_VALUES)
            ModelInput("level", "等级")
            ModelInput("exp", "经验")
            ModelCheckBox("moved", "已行动", enableData=1, disableData=0)
            ModelInput("posx", "X坐标")
            ModelInput("posy", "Y坐标")
            ModelInput("hpmax", "HP上限+")
            ModelInput("hp", "ＨＰ")
            ModelInput("power", "力量+")
            ModelInput("skill", "技术+")
            ModelInput("speed", "速度+")
            ModelInput("defensive", "守备+")
            ModelInput("magicdef", "魔防+")
            ModelInput("lucky", "幸运+")
            ModelInput("physical_add", "体格+")
            ModelInput("move_add", "移动+")
            # ModelSelect("status", "状态种类", None, None, datasets.STATUS)
            # ModelInput("status_turn", "状态持续")
            for i, label in enumerate(("剑", "枪", "斧", "弓", "书", "杖")):
                ModelInput("proficiency.%d" % i, "%s熟练度+" % label).view.setToolTip(datasets.PROFICIENCY_HINT)

        with Group("items", "角色物品", self._person, cols=4):
            for i in range(5):
                ModelSelect("items.%d" % i, "物品%d" % (i + 1), None, None, datasets.ITEMS)
                ModelInput("items_count.%d" % i, "数量")

        with Group("weapons", "武器属性", self._weapon):
            ui.Text("物品", className="label_left expand")
            with ui.Horizontal(className="fill"):
                ui.Choice(className="fill", choices=datasets.ITEMS, onselect=self.on_item_change).setSelection(1)
            ModelInput("name_ptr", "名称指针", hex=True)
            ModelInput("desc_ptr", "介绍文本", hex=True)
            ModelInput("icon", "图标序号")
            ModelSelect("type", "类型", None, None, datasets.WEAPONTYPES)
            ModelInput("level", "要求熟练度", hex=True, size=1).view.setToolTip(datasets.PROFICIENCY_HINT)
            ModelInput("power", "威力")
            ModelInput("hit", "命中")
            ModelInput("kill", "必杀")
            ModelInput("weight", "重量")
            ModelInput("range_min", "最小射程")
            ModelInput("range_max", "最大射程")
            ui.Text("复制属性", className="label_left expand")
            with ui.Horizontal(className="fill"):
                self.copy_weapon_view = ui.Choice(className="fill", choices=datasets.ITEMS)
                ui.Button("复制", onclick=self.copy_weapon)
            

        self.lazy_group(Group("train_items", "运输队", self._global, cols=4), self.render_train_items)

    def render_train_items(self):
        datasets = self.datasets
        for i in range(100):
            ModelSelect("train_items.%d" % i, "物品%03d" % (i + 1), None, None, datasets.ITEMS)
            ModelInput("train_items_count.%d" % i, "数量")

    def get_hotkeys(self):
        this = self.weak
        return (
            ('continue_move', MOD_ALT, getVK('m'), this.continue_move),
            ('move_to_cursor', MOD_ALT, getVK('g'), this.move_to_cursor),
            ('move_left', MOD_ALT, getVK('left'), this.move_left),
            ('move_right', MOD_ALT, getVK('right'), this.move_right),
            ('move_up', MOD_ALT, getVK('up'), this.move_up),
            ('move_down', MOD_ALT, getVK('down'), this.move_down),
        )

    def _person(self):
        person_addr = self._global.person_addr
        if person_addr:
            person = getattr(self, '_personins', None)
            if not person:
                person = self._personins = self.models.Person(person_addr, self.handler)
            elif person.addr != person_addr:
                person.addr = person_addr
            return person

    person = property(_person)

    def _config(self):
        return self._global.config

    def on_item_change(self, lb):
        self.item_index = lb.index

    def _weapon(self):
        if self.item_index > 0:
            return self._global.weapons[self.item_index - 1]

    def copy_weapon(self, _=None):
        index = self.copy_weapon_view.index
        if index > 0:
            item_from = self._global.weapons[index - 1]
            self.handler.write(self._global.weapons.addr_at(self.item_index - 1), item_from.to_bytes())

    def continue_move(self, _=None):
        """再移动"""
        self.person.moved = False

    def move_to_cursor(self, _=None):
        person = self.person
        _global = self._global
        person.posx = _global.curx
        person.posy = _global.cury

    def move_left(self, _=None):
        self.person.posx -= 1

    def move_right(self, _=None):
        self.person.posx += 1

    def move_up(self, _=None):
        self.person.posy -= 1

    def move_down(self, _=None):
        self.person.posy += 1