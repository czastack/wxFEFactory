from ..base import BaseGbaHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
import fefactory_api
ui = fefactory_api.ui


class FeTool(BaseGbaHack):

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self._personins = self.models.Person(0, self.handler)
    
    def render_main(self):
        datasets = self.datasets
        
        with Group("global", "全局", self._global):
            ModelInput("money", "金钱")
            ModelInput("turns", "回合")
            ModelInput("random", "乱数").view.setToolTip("设成0: 招招命中、必杀、贯通等，升级7点成长")
            ModelSelect("chapter", "章节", choices=datasets.CHAPTERS)

        with Group("player", "角色", self._person, cols=4):
            ModelInput("addr_hex", "地址", readonly=True)
            ModelInput("no", "序号")
            ModelSelect("prof", "职业", choices=datasets.PROFESSIONS, values=datasets.PROFESSION_VALUES)
            ModelInput("level", "等级")
            ModelInput("exp", "经验")
            ModelCheckBox("moved", "已行动", enableData=1, disableData=0)
            ModelInput("posx", "X坐标")
            ModelInput("posy", "Y坐标")
            ModelInput("hpmax", "HP最大值")
            ModelInput("hp", "ＨＰ")
            ModelInput("power", "力量")
            ModelInput("skill", "技术")
            ModelInput("speed", "速度")
            ModelInput("defensive", "守备")
            ModelInput("magicdef", "魔防")
            ModelInput("lucky", "幸运")
            ModelInput("physical_add", "体格+")
            ModelInput("move_add", "移动+")
            ModelSelect("status", "状态种类", choices=datasets.STATUS)
            ModelInput("status_turn", "状态持续")
            for i, label in enumerate(("剑", "枪", "斧", "弓", "杖", "理", "光", "暗")):
                ModelInput("proficiency.%d" % i, "%s熟练度" % label).view.setToolTip("E级:1 D级:31 C级:71 B级:121 A级:181 S级:251")

        with Group("items", "角色物品", self._person, cols=4):
            for i in range(5):
                ModelSelect("items.%d" % i, "物品%d" % (i + 1), choices=datasets.ITEMS)
                ModelInput("items_count.%d" % i, "数量")

        self.lazy_group(Group("train_items", "运输队", self._global, cols=4), self.render_train_items)

    def render_train_items(self):
        datasets = self.datasets
        for i in range(100):
            ModelSelect("train_items.%d" % i, "物品%03d" % (i + 1), choices=datasets.ITEMS)
            ModelInput("train_items_count.%d" % i, "数量")

    def get_hotkeys(self):
        return (
            ('continue_move', MOD_ALT, getVK('m'), self.continue_move),
            ('move_to_cursor', MOD_ALT, getVK('g'), self.move_to_cursor),
        )

    def _person(self):
        person_addr = self._global.person_addr
        if person_addr:
            self._personins.addr = person_addr
            return self._personins

    person = property(_person)

    def continue_move(self, _=None):
        """再移动"""
        self.person.moved = False

    def move_to_cursor(self, _=None):
        person = self.person
        _global = self._global
        person.posx = _global.curx
        person.posy = _global.cury
