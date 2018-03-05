from functools import partial
from ..base import BaseDolphinHack
from . import models, datasets
from lib.hack.form import Group, StaticGroup, InputWidget, ModelCheckBoxWidget, ModelInputWidget, ModelSelectWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseDolphinHack):

    def __init__(self):
        super().__init__()
        self._ram = models.Ram(0, self.handler)
        self.count_data = {}
    
    def render_main(self):
        with Group("global", "全局", self._ram, handler=self.handler):
            ModelInputWidget("money1", "小队1金钱")
            ModelInputWidget("money2", "小队2金钱")
            ModelInputWidget("money3", "小队3金钱")
            ModelInputWidget("exp1", "据点1分配经验值")
            ModelInputWidget("exp2", "据点2分配经验值")
            ModelInputWidget("exp3", "据点3分配经验值")

        with Group("player", "角色", self._person, handler=self.handler, cols=4):
            ModelInputWidget("addr_hex", "地址", readonly=True)
            ModelInputWidget("no", "角色编号", readonly=True)
            ModelSelectWidget("prof", "职业", None, None, datasets.PROFESSIONS, 
                tuple(0x80989A70 + i * 0x11C for i in range(len(datasets.PROFESSIONS))))
            ModelInputWidget("hp", "当前HP")
            ModelInputWidget("level", "等级")
            ModelInputWidget("exp", "经验")
            ModelInputWidget("posx", "横坐标")
            ModelInputWidget("posy", "纵坐标")
            ModelInputWidget("physical_add", "体格/重量+")
            ModelInputWidget("move_add", "移动+")
            ModelInputWidget("hp_add", "HP+")
            ModelInputWidget("power_add", "力+")
            ModelInputWidget("magic_add", "魔力+")
            ModelInputWidget("skill_add", "技术+")
            ModelInputWidget("speed_add", "速+")
            ModelInputWidget("lucky_add", "幸运+")
            ModelInputWidget("defensive_add", "守备+")
            ModelInputWidget("magicdef_add", "魔防+")
            self.m = ModelCheckBoxWidget("moved", "已行动", enableData=1, disableData=0)

        self.lazy_group(Group("skills", "角色技能", self._person, handler=self.handler), self.render_skills)
        self.lazy_group(Group("items", "角色物品", self._person, handler=self.handler), self.render_items)

    def render_skills(self):
        skill_values = self.get_skill_values()
        for i in range(18):
            ModelSelectWidget("skills.%d" % i, "技能%d" % (i + 1), None, None, datasets.SKILLS, skill_values)

    def render_items(self):
        item_values = self.get_item_values()
        for i in range(7):
            ModelSelectWidget("items.%d" % i, "物品%d" % (i + 1), None, None, datasets.ITEMS, item_values)
            ModelInputWidget("items_count.%d" % i, "数量")

    def _person(self):
        pedid = self._ram.pedid
        if pedid:
            return self._ram.persons[pedid]

    person = property(_person)

    def get_skill_values(self):
        return (0,) + tuple(0x807F09E0 + i * 0x2C for i in range(len(datasets.SKILLS) - 1))

    def get_item_values(self):
        return (0,) + tuple(0x80995870 + i * 0x50 for i in range(len(datasets.ITEMS) - 1))

    def get_hotkeys(self):
        return (
            ('continue_move', MOD_ALT, getVK('m'), self.continue_move),
            ('move_to_cursor', MOD_ALT, getVK('g'), self.move_to_cursor),
        )

    def continue_move(self, _=None):
        """再移动"""
        self.person.moved = False

    def move_to_cursor(self, _=None):
        person = self.person
        ram = self._ram
        person.posx = ram.curx
        person.posy = ram.cury