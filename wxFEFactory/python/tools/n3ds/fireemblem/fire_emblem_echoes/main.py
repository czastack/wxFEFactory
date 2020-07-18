import abc
from functools import partial
from lib import ui
from lib.hack.forms import (
    Group, StaticGroup, ModelCheckBox, ModelInput, ModelAddrInput, ModelSelect, ModelFlagWidget, Choice, ChoiceWidget
)
from lib.ui.components import Pagination
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
        self.version = '1.0'

    def render_main(self):
        _global = (self._global, models.Global_1_0)
        with Group("global", "全局", _global, cols=4):
            self.render_global()

        self.lazy_group(Group("player", "角色", (self._person, models.InGameCharacter), cols=4), self.render_person)

        self.lazy_group(Group("convoy1", "行囊(阿鲁姆)", _global, cols=4),
            partial(self.render_convoy, leader='alm'))

        self.lazy_group(Group("convoy2", "行囊(赛莉卡)", _global, cols=4),
            partial(self.render_convoy, leader='celica'))

    def render_global(self):
        self.version_view = Choice("版本", datasets.VERSIONS, self.on_version_change)
        with self.active_widgets:
            ModelCheckBox("control_enemy")
            ModelCheckBox("inf_move")
            ModelCheckBox("exchange_enemy")
            ModelCheckBox("prepare_anyone")
            ModelCheckBox("anyone_bag")
            ModelCheckBox("quick_info")
            ModelCheckBox("critical_100")
            ModelCheckBox("custom_exp")
            ModelInput("custom_exp_value")
            ModelCheckBox("growth_rate_add")
            ModelInput("growth_rate_add_value")
            ModelCheckBox("add_all_attr")
            ModelCheckBox("gold_coin_996")
            ModelCheckBox("silver_coin_9984")
            ModelCheckBox("break_keep")
            ModelCheckBox("item_keep")
            ModelCheckBox("inf_mila")
            ModelCheckBox("no_battle_3d")
            ModelCheckBox("first_turn_retreat")
            ModelCheckBox("well_no_driy")
            ModelCheckBox("support_talk_now")
            ModelCheckBox("inf_hp")
            ModelCheckBox("instant_kill_inf_hp")
            ModelCheckBox("instant_kill")
            ModelCheckBox("range_100")
            ModelCheckBox("move_max")
            ModelCheckBox("all_weapon_equipment")
            ModelCheckBox("all_support_a")
            ModelCheckBox("all_attr_max_99")
            ModelCheckBox("quick_get_battle_skill")
            ModelSelect("dean_sonya_event", choices=datasets.DEAN_SONYA_EVENT)
            ModelSelect("system.difficulty", "难易度", choices=datasets.DIFFICULTY)
            ModelInput("system.renown", "名声值")

    def render_person(self):
        self.chars_view = ChoiceWidget("角色", (), self.on_char_change)
        with self.chars_view.container:
            ui.Button(label="读取列表", class_="button", onclick=self.read_chars)
        ModelAddrInput()
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
        ModelInput("win")
        ModelInput("pro")
        ModelSelect("item.item", "所携物品", choices=datasets.ITEMS)
        ModelInput("item.star", "物品星级")
        ModelInput("charname", "角色", readonly=True)
        ModelInput("profname", "职业", readonly=True)

    def render_convoy(self, leader):
        group = Group.active_group()
        with ModelSelect.choices_cache:
            for i in range(self.CONVOY_PAGE_LENGTH):
                item_path = "convoy.{0}.{1}+{0}_offset".format(leader, i)
                ModelSelect(item_path + ".item", "", choices=datasets.ITEMS)
                with ModelInput(item_path + ".star", "星级").container:
                    ui.Button(label="复制", extra={"tooltip": "复制到行囊"}, class_="button",
                              onclick=partial(self.copy_item, source=item_path, leader=leader))
        with Group.active_group().footer:
            Pagination(partial(self.on_convoy_page, leader=leader, group=group), self.CONVOY_PAGE_TOTAL)

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

    def onattach(self):
        super().onattach()
        if self.version == '1.0':
            if self._global_ins.system.addr & 0xFFFF == 0xFF00:
                self.version_view.set_selection(1, True)

    def _person(self):
        self._person_ins.addr = self._global_ins.chars.addr_at(self.person_index)
        return self._person_ins

    person = property(_person)

    def on_version_change(self, lb):
        self.version = lb.text
        self._global_ins = models.SPECIFIC_GLOBALS[self.version](0, self.handler)

    def _global(self):
        return self._global_ins

    def on_char_change(self, lb):
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
            choices.append('{:02d}-{}'.format(i + 1, charname))
        self.chars_view.Set(choices)

    # def read_chars(self, _):
    #     """读取角色列表调用"""
    #     choices = self._read_chars()
    #     if not choices:
    #         # 尝试动态查找
    #         find_start = 0x328B0000
    #         start_1 = self.handler.find_bytes(datasets.CHARID_ALM, find_start, find_start + 0x80000)
    #         start_2 = self.handler.find_bytes(datasets.CHARID_CELICA, find_start, find_start + 0x80000)
    #         for start in (start_1, start_2):
    #             if start > 0:
    #                 start = start - 0x408
    #                 character = models.InGameCharacter(start, self.handler)
    #                 if character.index == 1:
    #                     self._global_ins.field('chars').offset = start
    #                     self._read_chars()

    def copy_item(self, _, source, leader):
        """复制物品到行囊"""
        convoy = getattr(self._global_ins.convoy, leader)
        source = getattr(self._global_ins, source)
        for item in convoy:
            if item.item == 0:
                item.copy_from(source)
                print('复制成功: ', datasets.ITEMS[source.item])
                break

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

    def on_convoy_page(self, page, leader, group):
        """行囊翻页"""
        setattr(self._global_ins.convoy, leader + '_offset', (page - 1) * self.CONVOY_PAGE_LENGTH)
        group.read()
