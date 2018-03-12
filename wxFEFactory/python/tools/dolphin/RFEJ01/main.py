from functools import partial
from ..base import BaseDolphinHack
from . import models, datasets
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseDolphinHack):

    def __init__(self):
        super().__init__()
        self._ram = models.Ram(0, self.handler)
    
    def render_main(self):
        person = self._person
        with Group("global", "全局", self._ram):
            ModelInput("money1", "小队1金钱")
            ModelInput("money2", "小队2金钱")
            ModelInput("money3", "小队3金钱")
            ModelInput("exp1", "据点1分配经验值")
            ModelInput("exp2", "据点2分配经验值")
            ModelInput("exp3", "据点3分配经验值")

        with Group("player", "角色", person, cols=4):
            ModelInput("addr_hex", "地址", readonly=True)
            ModelInput("no", "角色编号", readonly=True)
            ModelSelect("prof", "职业", None, None, datasets.PROFESSIONS, 
                tuple(0x80989A70 + i * 0x11C for i in range(len(datasets.PROFESSIONS))))
            ModelInput("hp", "当前HP")
            ModelInput("level", "等级")
            ModelInput("exp", "经验")
            ModelInput("posx", "横坐标")
            ModelInput("posy", "纵坐标")
            ModelInput("physical_add", "体格/重量+")
            ModelInput("move_add", "移动+")
            ModelInput("hp_add", "HP+")
            ModelInput("power_add", "力+")
            ModelInput("magic_add", "魔力+")
            ModelInput("skill_add", "技术+")
            ModelInput("speed_add", "速+")
            ModelInput("lucky_add", "幸运+")
            ModelInput("defensive_add", "守备+")
            ModelInput("magicdef_add", "魔防+")
            ModelCheckBox("moved", "已行动", enableData=1, disableData=0)

        self.lazy_group(Group("skills", "角色技能", person), self.render_skills)
        self.lazy_group(Group("items", "角色物品", person, handler=self.handler), self.render_items)

    def render_skills(self):
        skill_values = (0,) + tuple(0x807F09E0 + i * 0x2C for i in range(len(datasets.SKILLS) - 1))
        for i in range(18):
            ModelSelect("skills.%d" % i, "技能%d" % (i + 1), None, None, datasets.SKILLS, skill_values)

    def render_items(self):
        item_values = (0,) + tuple(0x80995870 + i * 0x50 for i in range(len(datasets.ITEMS) - 1))
        for i in range(7):
            ModelSelect("items.%d" % i, "物品%d" % (i + 1), None, None, datasets.ITEMS, item_values)
            ModelInput("items_count.%d" % i, "数量")

    def get_hotkeys(self):
        return (
            ('continue_move', MOD_ALT, getVK('m'), self.continue_move),
            ('move_to_cursor', MOD_ALT, getVK('g'), self.move_to_cursor),
        )

    def _person(self):
        pedid = self._ram.pedid
        if pedid:
            return self._ram.persons[pedid]

    person = property(_person)

    def continue_move(self, _=None):
        """再移动"""
        self.person.moved = False

    def move_to_cursor(self, _=None):
        person = self.person
        ram = self._ram
        person.posx = ram.curx
        person.posy = ram.cury