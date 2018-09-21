from ..base import BaseNdsHack
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, Label
from lib.win32.keys import VK
from lib.exui.components import Pagination
from fefactory_api import ui


class FeHack(BaseNdsHack):
    TRAIN_ITEMS_PAGE_LENGTH = 10
    TRAIN_ITEMS_PAGE_TOTAL = 20

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self._global.train_items_offset = 0
        self._personins = self.models.Person(0, self.handler)
        self.item_index = 1

    def render_main(self):
        datasets = self.datasets
        weak = self.weak

        with Group("global", "全局", self._global, cols=4):
            ModelInput("money", "金钱", instance=weak._config)
            ModelInput("turns", "回合")
            ModelCheckBox("ourturn", "总是我方回合")
            ModelCheckBox("control_enemy", "可控制敌人")
            ModelCheckBox("upgrade_max", "升级能力值最大")
            ModelCheckBox("upgrade_all", "升级全能力提升")
            ModelCheckBox("lv1_can_transfer", "Lv1即可转职")
            ModelCheckBox("can_train", "都可用运输队")
            ModelCheckBox("can_visit", "都可访问村庄")
            ModelCheckBox("can_holddown", "都可压制")
            ModelCheckBox("use_enemy_prof", "使用敌专用兵种不死机")
            ModelCheckBox("infinite_refine", "武器屋炼成无限次")
            ModelCheckBox("item_consume", "道具耐久不减")
            ModelCheckBox("enemy_item_drop", "敌人全道具掉落")
            ModelSelect("exp_rate", "经验值倍数", choices=datasets.RATE, values=datasets.EXP_RATE_VALUES)
            ModelSelect("pro_rate", "熟练度倍数", choices=datasets.RATE, values=datasets.PRO_RATE_VALUES)
            # ModelInput("random", "乱数").view.setToolTip("设成0: 招招命中、必杀、贯通等，升级7点成长")
            # ModelSelect("chapter", "章节", choices=datasets.CHAPTERS)

        self.lazy_group(Group("config", "配置", weak._config, cols=4), self.render_config)
        self.lazy_group(Group("player", "角色", weak._person, cols=4), self.render_person)
        self.lazy_group(Group("items", "角色物品", weak._person, cols=4), self.render_items)
        self.lazy_group(Group("iteminfos", "武器属性", weak._iteminfo), self.render_iteminfos)

        self.train_items_group = Group("train_items", "运输队", self._global, cols=4)
        self.lazy_group(self.train_items_group, self.render_train_items)

    def render_config(self):
        datasets = self.datasets
        ModelSelect("difficulty", "难易度", choices=datasets.DIFFICULTY, values=datasets.DIFFICULTY_VALUES)
        ModelSelect("character_gender", "主人公性别", choices=datasets.CHARACTER_GENDER)
        ModelSelect("character_hair_style", "主人公发色", choices=datasets.CHARACTER_HAIR_STYLE)
        ModelSelect("character_hair_color", "主人公发型", choices=datasets.CHARACTER_HAIR_COLOR)
        ModelSelect("character_eye", "主人公眼睛", choices=datasets.CHARACTER_EYE)
        ModelSelect("character_cloth", "主人公服装", choices=datasets.CHARACTER_CLOTH)

    def render_person(self):
        datasets = self.datasets
        ModelInput("addr_hex", "地址", readonly=True)
        ModelInput("no", "序号")
        ModelSelect("prof", "职业", choices=datasets.PROFESSIONS, values=datasets.PROFESSION_VALUES)
        ModelInput("level", "等级")
        ModelInput("exp", "经验")
        ModelCheckBox("moved", "已行动", enableData=1, disableData=0)
        ModelInput("posx", "X坐标")
        ModelInput("posy", "Y坐标")
        ModelInput("hpmax", "HP上限+")
        ModelInput("hp", "ＨＰ")
        ModelInput("power", "力量+")
        ModelInput("magic", "魔力+")
        ModelInput("skill", "技术+")
        ModelInput("speed", "速度+")
        ModelInput("defense", "守备+")
        ModelInput("magicdef", "魔防+")
        ModelInput("lucky", "幸运+")
        ModelInput("physical_add", "体格+")
        ModelInput("move_add", "移动+")
        # ModelSelect("status", "状态种类", choices=datasets.STATUS)
        # ModelInput("status_turn", "状态持续")
        for i, label in enumerate(("剑", "枪", "斧", "弓", "书", "杖")):
            ModelInput("proficiency.%d" % i, "%s熟练度+" % label).view.setToolTip(datasets.PROFICIENCY_HINT)

    def render_items(self):
        datasets = self.datasets
        for i in range(5):
            ModelSelect("items.%d.item" % i, "物品%d" % (i + 1), choices=datasets.ITEMS)
            ModelInput("items.%d.count" % i, "数量")

    def render_iteminfos(self):
        datasets = self.datasets
        Choice("物品", datasets.ITEMS, self.on_item_change)
        Label("复制属性")
        with ui.Horizontal(className="fill"):
            self.copy_iteminfo_view = ui.Choice(className="fill", choices=datasets.ITEMS)
            ui.Button("复制", onclick=self.copy_iteminfo)
        ModelInput("addr_hex", "地址", readonly=True)
        ModelInput("name_ptr", "名称指针", hex=True)
        ModelInput("desc_ptr", "介绍文本", hex=True)
        ModelInput("icon", "图标序号")
        ModelSelect("type", "类型", choices=datasets.WEAPONTYPES)
        ModelInput("level", "要求熟练度", hex=True, size=1).view.setToolTip(datasets.PROFICIENCY_HINT)
        ModelInput("power", "威力")
        ModelInput("hit", "命中")
        ModelInput("kill", "必杀")
        ModelInput("weight", "重量")
        ModelInput("range_min", "最小射程")
        ModelInput("range_max", "最大射程")
        ModelInput("move_add", "移动+")
        ModelInput("hp_add", "HP+")
        ModelInput("power_add", "力量+")
        ModelInput("magic_add", "魔力+")
        ModelInput("skill_add", "技巧+")
        ModelInput("speed_add", "速度+")
        ModelInput("lucky_add", "幸运+")
        ModelInput("defense_add", "防御+")
        ModelInput("magicdef_add", "魔防+")

        i = 0
        for item in datasets.ITEM_ATTRS:
            hint, labels = item
            i += 1
            ModelFlagWidget("attr%d" % i, hint or "属性%d" % i, labels=labels)

    def render_train_items(self):
        datasets = self.datasets
        for i in range(10):
            ModelSelect("train_items.%d+train_items_offset.item" % i, "", choices=datasets.ITEMS)
            ModelInput("train_items.%d+train_items_offset.count" % i, "数量")
        with Group.active_group().footer:
            Pagination(self.on_train_items_page, self.TRAIN_ITEMS_PAGE_TOTAL)

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.M, this.continue_move),
            (VK.MOD_ALT, VK.G, this.move_to_cursor),
            (VK.MOD_ALT, VK.LEFT, this.move_left),
            (VK.MOD_ALT, VK.RIGHT, this.move_right),
            (VK.MOD_ALT, VK.UP, this.move_up),
            (VK.MOD_ALT, VK.DOWN, this.move_down),
        )

    def _person(self):
        person_addr = self._global.person_addr
        if person_addr:
            self._personins.addr = person_addr
            return self._personins

    person = property(_person)

    def _config(self):
        return self._global.config

    def on_item_change(self, lb):
        self.item_index = lb.index

    def _iteminfo(self):
        if self.item_index > 0:
            return self._global.iteminfos[self.item_index - 1]

    def copy_iteminfo(self, _=None):
        index = self.copy_iteminfo_view.index
        if index > 0:
            item_from = self._global.iteminfos[index - 1]
            self.handler.write(self._global.iteminfos.addr_at(self.item_index - 1), item_from.to_bytes())

    def continue_move(self):
        """再移动"""
        self.person.moved = False

    def move_to_cursor(self):
        person = self.person
        _global = self._global
        person.posx = _global.curx
        person.posy = _global.cury

    def move_left(self):
        self.person.posx -= 1

    def move_right(self):
        self.person.posx += 1

    def move_up(self):
        self.person.posy -= 1

    def move_down(self):
        self.person.posy += 1

    def on_train_items_page(self, page):
        self._global.train_items_offset = (page - 1) * self.TRAIN_ITEMS_PAGE_LENGTH
        self.train_items_group.read()
