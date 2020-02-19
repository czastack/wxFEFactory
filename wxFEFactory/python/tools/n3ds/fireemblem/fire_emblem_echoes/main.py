import abc
from functools import partial
from lib import ui
from lib.ui.components import Pagination
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelFlagWidget, Choice, ChoiceWidget
from lib.win32.keys import VK
from tools.n3ds.base import BaseN3dsHack
from . import models, datasets


class Main(BaseN3dsHack):
    CONVOY_PAGE_LENGTH = 20
    CONVOY_PAGE_TOTAL = 12

    def __init__(self):
        super().__init__()
        self._global_ins = models.Global_1_0(0, self.handler)
        self._person_ins = models.InGameCharacter(0, self.handler)
        self.person_index = 0

    def render_main(self):
        _global = (self._global, models.Global_1_0)
        with Group("global", "全局", _global, cols=4):
            self.render_global()

        self.lazy_group(Group("player", "角色", (self._person, models.InGameCharacter), cols=4), self.render_person)

        self.lazy_group(Group("convoy1", "行囊(阿鲁姆)", _global, cols=4),
            partial(self.render_convoy, chapter='alm'))

        self.lazy_group(Group("convoy2", "行囊(赛莉卡)", _global, cols=4),
            partial(self.render_convoy, chapter='celica'))

    def render_global(self):
        Choice("版本", datasets.VERSIONS, self.on_version_change)
        with self.active_widgets:
            ModelCheckBox("control_enemy")
            ModelCheckBox("inf_move")
            ModelCheckBox("exchange_enemy")
            ModelCheckBox("prepare_enemy")
            ModelCheckBox("anyone_bag")
            ModelCheckBox("quick_info")
            ModelCheckBox("add_all_attr")
            ModelCheckBox("custom_exp")
            ModelInput("custom_exp_value")
            ModelCheckBox("growth_rate_add")
            ModelInput("growth_rate_add_value")
            ModelCheckBox("break_keep")
            ModelCheckBox("item_keep")
            ModelCheckBox("first_turn_withdraw")
            ModelCheckBox("no_battle_3d")
            ModelCheckBox("well_no_driy")
            ModelCheckBox("inf_mila")
            ModelCheckBox("support_talk_now")
            ModelCheckBox("inf_hp")
            ModelCheckBox("range_100")
            ModelCheckBox("move_max")
            ModelCheckBox("all_weapon_equipment")
            ModelCheckBox("all_support_a")
            ModelCheckBox("all_attr_max_99")
            ModelCheckBox("add_all_attr")
            ModelCheckBox("gold_coin_996")

    def render_person(self):
        self.chars_view = ChoiceWidget("角色", (), self.on_person_change)
        with self.chars_view.container:
            ui.Button(label="读取列表", class_="button", onclick=self.read_chars)
        ModelInput("addr_hex", "地址", readonly=True)
        ModelInput("index")
        ModelInput("level")
        ModelInput("exp")
        ModelInput("hp")
        ModelInput("pow")
        ModelInput("atk")
        ModelInput("tec")
        ModelInput("spd")
        ModelInput("luc")
        ModelInput("def_")
        ModelInput("res")
        ModelInput("mov")
        ModelInput("act")
        ModelInput("pro")
        ModelSelect("item.item", "所携物品", choices=datasets.ITEM_LABELS, values=datasets.ITEM_VALUES)
        ModelInput("item.star", "物品星级")
        ModelInput("charname", "角色", readonly=True)
        ModelInput("profname", "职业", readonly=True)

    def render_convoy(self, chapter):
        group = Group.active_group()
        with ModelSelect.choices_cache:
            for i in range(10):
                ModelSelect("convoy.{0}.{1}+{0}_offset.item".format(chapter, i), "",
                    choices=datasets.ITEM_LABELS, values=datasets.ITEM_VALUES)
                ModelInput("convoy.{0}.{1}+{0}_offset.star".format(chapter, i), "星级")
        with Group.active_group().footer:
            Pagination(partial(self.on_convoy_page, chapter=chapter, group=group), self.CONVOY_PAGE_TOTAL)

    def get_hotkeys(self):
        this = self.weak
        return (
            # (VK.MOD_ALT, VK.M, this.continue_move),
            # (VK.MOD_ALT, VK.G, this.move_to_cursor),
            # (VK.MOD_ALT, VK.LEFT, this.move_left),
            # (VK.MOD_ALT, VK.RIGHT, this.move_right),
            # (VK.MOD_ALT, VK.UP, this.move_up),
            # (VK.MOD_ALT, VK.DOWN, this.move_down),
        )

    def _person(self):
        self._person_ins.addr = self._global_ins.chars.addr_at(self.person_index)
        return self._person_ins

    person = property(_person)

    def on_version_change(self, lb):
        version = lb.text
        self._global_ins = models.SPECIFIC_GLOBALS[version](0, self.handler)

    def _global(self):
        return self._global_ins

    def on_person_change(self, lb):
        """角色切换"""
        self.person_index = lb.index

    def read_chars(self, _):
        """读取角色列表"""
        chars = self._global_ins.chars
        choices = []
        for i in range(chars.length):
            charname = chars[i].charname
            if not charname:
                break
            choices.append('%02d-%s' % (i + 1, charname))
        self.chars_view.Set(choices)

    def move_to_cursor(self):
        person = self.person
        _global = self._global_ins
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

    def on_convoy_page(self, page, chapter, group):
        """行囊翻页"""
        setattr(self._global_ins.convoy, chapter + '_offset', (page - 1) * self.CONVOY_PAGE_LENGTH)
        group.read()
