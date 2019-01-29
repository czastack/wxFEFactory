from ..base import BaseGbaHack
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.win32.keys import VK
from lib.exui.components import Pagination
from fefactory_api import ui


class FeHack(BaseGbaHack):
    TRAIN_ITEMS_PAGE_LENGTH = 10
    TRAIN_ITEMS_PAGE_TOTAL = 10

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self._global.train_items_offset = 0
        self._person_ins = self.models.Person(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            self.render_global()

        self.lazy_group(Group("player", "角色", self._person, cols=4), self.render_char)
        self.lazy_group(Group("items", "角色物品", self._person, cols=4), self.render_char_items)
        self.lazy_group(Group("support", "角色支援", self._person, cols=4), self.render_char_support)

        self.train_items_group = Group("train_items", "运输队", self._global, cols=4)
        self.lazy_group(self.train_items_group, self.render_train_items)

    def render_global(self):
        ModelInput("money", "金钱")
        ModelInput("turns", "回合")
        ModelInput("random", "乱数").set_help("设成0: 招招命中、必杀、贯通等，升级7点成长")
        ModelSelect("chapter", "章节", choices=self.datasets.CHAPTERS)
        ModelCheckBox("inf_move", "无限行动")
        ModelCheckBox("item_count_keep", "武器耐久度不减")
        ModelCheckBox("proficiency_max", "武器熟练度最大")
        ModelCheckBox("ability_up_1", "全能力成长1点")
        ModelCheckBox("ability_up_2", "全能力成长2点")
        ModelCheckBox("got_100exp", "战后升级")
        ModelCheckBox("support_quickly", "好感度快速提升")

    def render_char(self):
        datasets = self.datasets
        ModelInput("addr_hex", "R键地址", readonly=True).set_help("R键人物详情中人物属性")
        ModelInput("no", "序号")
        ModelSelect("prof", "职业", choices=datasets.PROFESSIONS, values=datasets.PROFESSION_VALUES)
        ModelInput("level", "等级")
        ModelInput("exp", "经验")
        ModelCheckBox("moved", "已行动", enable=1, disable=0)
        ModelInput("posx", "X坐标")
        ModelInput("posy", "Y坐标")
        ModelInput("hpmax", "HP最大值")
        ModelInput("hp", "ＨＰ")
        ModelInput("power", "力量")
        ModelInput("skill", "技术")
        ModelInput("speed", "速度")
        ModelInput("defense", "守备")
        ModelInput("magicdef", "魔防")
        ModelInput("lucky", "幸运")
        ModelInput("physical_add", "体格+")
        ModelInput("move_add", "移动+")
        ModelSelect("status", "状态种类", choices=datasets.STATUS)
        ModelInput("status_turn", "状态持续")
        for i, label in enumerate(("剑", "枪", "斧", "弓", "杖", "理", "光", "暗")):
            ModelInput("proficiency.%d" % i, "%s熟练度" % label).set_help(
                "E级:1 D级:31 C级:71 B级:121 A级:181 S级:251")

    def render_char_items(self):
        datasets = self.datasets
        with ModelSelect.choices_cache:
            for i in range(5):
                ModelSelect("items.%d.item" % i, "物品%d" % (i + 1), choices=datasets.ITEMS)
                ModelInput("items.%d.count" % i, "数量")

    def render_char_support(self):
        for i in range(self._person_ins.support.length):
            ModelInput("support.%d" % i, "好感度%d" % (i + 1)).set_help('80~160: C, 160~240: B, 240~255: A')

    def render_train_items(self):
        datasets = self.datasets
        with ModelSelect.choices_cache:
            for i in range(10):
                ModelSelect("train_items.%d+train_items_offset.item" % i, "", choices=datasets.ITEMS)
                ModelInput("train_items.%d+train_items_offset.count" % i, "数量")
        with Group.active_group().footer:
            Pagination(self.on_train_items_page, self.TRAIN_ITEMS_PAGE_TOTAL)

    def get_hotkeys(self):
        return (
            (0, VK.H, self.pull_through),
            (0, VK.M, self.continue_move),
            (0, VK.G, self.move_to_cursor),
            (0, VK.T, self.toggle_random),
            (0, VK.R, self.reload_ammo),
            (0, VK.N, self.remove_weapon),
            (0, VK.LEFT, self.move_left),
            (0, VK.RIGHT, self.move_right),
            (0, VK.UP, self.move_up),
            (0, VK.DOWN, self.move_down),
            (0, VK._0, self.hp_zero),
            (0, VK.DELETE, self.delete_unit),
        )

    def _person(self):
        person_addr = self._global.person_addr
        if person_addr and (person_addr & 0xFFFF0000 == 0x02020000):
            self._person_ins.addr = person_addr
        if self._person_ins.addr:
            return self._person_ins

    person = property(_person)

    def pull_through(self):
        """再移动"""
        self.person.set_with('hp', 'hpmax')

    def continue_move(self):
        """再移动"""
        self.person.moved = False

    def move_to_cursor(self):
        person = self.person
        _global = self._global
        person.posx = _global.curx
        person.posy = _global.cury

    def toggle_random(self):
        """切换乱数"""
        last_random = self._global.random
        if last_random != 0:
            self.last_random = last_random
            self._global.random = 0
        else:
            self._global.random = self.last_random

    def reload_ammo(self):
        """恢复耐久"""
        for item in self._person().items:
            if not item.item:
                break
            item.count = 99

    def remove_weapon(self):
        """移除物品"""
        for item in self._person().items:
            if not item.item:
                break
            item.value = 0

    def move_left(self):
        self.person.posx -= 1

    def move_right(self):
        self.person.posx += 1

    def move_up(self):
        self.person.posy -= 1

    def move_down(self):
        self.person.posy += 1

    def hp_zero(self):
        self.person.hp = 1

    def delete_unit(self):
        unit = self.person
        if unit.no >= 64:
            unit.unkonw_ptr = 0
            unit.prof = 0
            unit.moved = 1
            unit.hp = 0

    def on_train_items_page(self, page):
        self._global.train_items_offset = (page - 1) * self.TRAIN_ITEMS_PAGE_LENGTH
        self.train_items_group.read()
