from ..base import BasePs2Hack
from lib.hack.forms import Group, StaticGroup, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, ModelChoiceDisplay, Choice
from lib.win32.keys import VK
from lib import exui
from lib.exui.components import Pagination
from lib.lazy import ClassLazy
from functools import partial
from . import models, datasets
import fefactory_api
ui = fefactory_api.ui


class Main(BasePs2Hack):
    HUMEN_ITEMS_PAGE_LENGTH = 16
    HUMEN_ITEMS_PAGE_TOTAL = 4
    datasets = datasets

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self._global.human_items_offset = 0
        self.person = models.Person(0, self.handler)
        self.person_grow = models.PersonGrow(0, self.handler)
        self.chariot = models.Chariot(0, self.handler)
        self.static_item = models.StaticItem(0, self.handler)
        self.item_info = models.ItemInfo(0, self.handler)
        self.enemy = models.Enemy(0, self.handler)
    
    def render_main(self):
        person = self.person
        chariot = self.chariot
        with Group("global", "全局", self._global):
            ModelInput("money")
            ModelInput("battlein")
            ModelCheckBox("no_battle")
            ModelInput("battle_count")
            ModelInput("win_count")
            ModelInput("die_count")
            ModelInput("escape_count")

        with Group("player", "角色", person, cols=4):
            Choice("角色", datasets.PERSONS, self.on_person_change)
            ModelInput("level")
            ModelInput("exp")
            ModelInput("hpmax")
            ModelInput("hp")
            ModelInput("atk")
            ModelInput("defense")
            ModelInput("drive")
            ModelInput("title")
            ModelInput("prof")
            # ModelInput("status")

        self.lazy_group(Group("person_grow", "角色成长", self.person_grow, cols=4), self.render_person_grow)
        self.lazy_group(Group("person_equips", "角色装备", person), self.render_person_equips)
        self.human_items_group = Group("human_items", "人类道具", self._global, cols=4)
        self.lazy_group(self.human_items_group, self.render_human_items)
        self.lazy_group(Group("chariot", "战车", chariot, cols=4), self.render_chariot)
        self.lazy_group(Group("chariot_items", "战车装备/物品", chariot, cols=4), self.render_chariot_items)
        self.lazy_group(Group("wanted", "赏金首", self._global, cols=4), self.render_wanted)

        with StaticGroup("快捷键"):
            with ui.ScrollView(className="fill"):
                ui.Text("左移(目标战车坐标): alt+left")
                ui.Text("右移: alt+right")
                ui.Text("上移: alt+up")
                ui.Text("下移: alt+right")
                ui.Text("恢复HP: alt+h")

    def render_person_grow(self):
        ModelInput("hp_init")
        ModelInput("hp_grow")
        ModelInput("atk_init")
        ModelInput("atk_grow")
        ModelInput("def_init")
        ModelInput("def_grow")
        ModelInput("drive_init")
        ModelInput("drive_grow")

    def render_person_equips(self):
        sources = (datasets.EQUIP_WEAPON, datasets.EQUIP_HEAD, datasets.EQUIP_BODY, datasets.EQUIP_HAND, datasets.EQUIP_FOOT, datasets.EQUIP_ORN)
        for i, label in enumerate(('武器', '头部', '躯干', '手臂', '脚部', '胸甲')):
            prop = "equips.%d" % i
            select = ModelChoiceDisplay(prop + ".item", label, choices=sources[i].choices, values=sources[i].values)
            with select.container:
                ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_item_info, self.weak, 
                    ins=self.person, prop=prop))

    def render_human_items(self):
        for i in range(self.HUMEN_ITEMS_PAGE_LENGTH):
            prop = "items.%d+human_items_offset" % i
            select = ModelSelect(prop + ".item", "物品%d" % (i + 1), 
                choices=datasets.HUMEN_ITEMS.choices, values=datasets.HUMEN_ITEMS.values)
            with select.container:
                ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_item_info, self.weak, 
                    ins=self._global, prop=prop))
        with Group.active_group().footer:
            Pagination(self.on_human_items_page, self.HUMEN_ITEMS_PAGE_TOTAL)

    def on_human_items_page(self, page):
        self._global.human_items_offset = (page - 1) * self.HUMEN_ITEMS_PAGE_LENGTH
        self.human_items_group.read()

    def render_chariot(self):
        Choice("战车", datasets.CHARIOTS, self.on_chariot_change)
        ModelInput("sp")
        ModelInput("defense")
        ModelInput("weight")
        ModelInput("bullet")

        # for i in range(self.chariot.hole_type.length):
        #     ModelSelect("hole_type.%d" % i, "炮穴%d类型" % (i + 1), 
        #         choices=datasets.HOLE_TYPES, values=datasets.HOLE_TYPE_VALUES)

        # ModelInput("position", hex=True)

    def render_chariot_items(self):
        # detail_keep_click = lambda key: partial(__class__.show_chariot_equip_info, self.weak, key=key, read=False)
        # detail_click = lambda key: partial(__class__.show_chariot_equip_info, self.weak, key=key)
        # preset_click = lambda key: partial(__class__.show_chariot_equip_preset, self.weak, key=key)

        for i in range(self.chariot.equips.length):
            prop = "equips.%d" % i
            select = ModelSelect(prop + ".item", "", choices=datasets.CHARIOT_ALL_ITEM.choices, values=datasets.CHARIOT_ALL_ITEM.values)
            with select.container:
                ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_item_info, self.weak, 
                    ins=self.chariot, prop=prop))
            # exui.Label("装备%d" % (i + 1))
            # with ui.Horizontal(className="right"):
            #     ui.Button("上次", className="btn_sm", onclick=detail_keep_click("equips.%d" % i))
            #     ui.Button("详情", className="btn_sm", onclick=detail_click("equips.%d" % i))
            #     ui.Button("预设", className="btn_sm", onclick=preset_click("equips.%d" % i))

    def render_wanted(self):
        for i, name in enumerate(datasets.WANTED_LIST):
            ModelSelect("wanted_status.%d" % i, name, choices=datasets.WANTED_STATUS, values=datasets.WANTED_STATUS_VALUES)

    def get_hotkeys(self):
        this = self.weak
        return (
            # (VK.MOD_ALT, VK.LEFT, this.move_left),
            # (VK.MOD_ALT, VK.RIGHT, this.move_right),
            # (VK.MOD_ALT, VK.UP, this.move_up),
            # (VK.MOD_ALT, VK.DOWN, this.move_down),
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    @ClassLazy
    def dictionary(self):
        from lib.gba.dictionary import Dictionary
        import os
        return Dictionary(os.path.join(os.path.dirname(__file__), 'dict.txt'), low_range=(0x81, 0x98), use_ascii=True)

    def get_item_info_dialog(self):
        """物品信息对话框"""
        name = 'item_info_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(name, "物品详情", self.item_info, cols=1,
                    dialog_style={'width': 600, 'height': 1200}, closable=False, horizontal=False, button=False) as dialog:
                # ModelInput("item")
                ModelInput("attr1")
                ModelInput("status")
                ModelInput("atk_addition")
                ModelInput("str_addition")
                ui.Button("种类详情", onclick=self.show_static_item)

            setattr(self, name, dialog)
        return dialog

    def get_static_item_dialog(self):
        """静态物品对话框"""
        name = 'static_item_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(None, "静态物品", self.static_item, cols=1,
                    dialog_style={'width': 600, 'height': 1200}, closable=False, horizontal=False, button=False) as dialog:
                ModelChoiceDisplay("item", choices=datasets.ITEMS, ins=self.item_info)
                ModelInput("weight")
                ModelInput("load")
                ModelInput("atk")
                ModelInput("defense")
                ModelInput("strength")

            setattr(self, name, dialog)
        return dialog

    def get_chariot_preset_dialog(self, name, label, head, items):
        """战车物品预设对话框"""
        dialog = getattr(self, name, None)
        if dialog is None:
            with exui.StdDialog(label, style={'width': 1100, 'height': 900}, closable=False) as dialog:
                with ui.Horizontal(className="expand"):
                    dialog.search = ui.ComboBox(type="dropdown", className="fill", 
                        onselect=partial(__class__.on_chariot_item_preset_search_select, self.weak, dialog=dialog))
                    ui.Button("搜索", onclick=partial(__class__.on_chariot_item_preset_search, self.weak, dialog=dialog))
                dialog.listview = listview = ui.ListView(className="fill")
                with ui.Horizontal(className="expand"):
                    dialog.use_weight = ui.CheckBox(label="重量", className="vcenter", checked=True)
                    dialog.use_attr2 = ui.CheckBox(label="武器弹舱/C装置回避", className="vcenter", checked=True)
                dialog.listview.appendColumns(*head)

                listview.insertItems(items)
                listview.setOnItemActivated(partial(__class__.on_chariot_item_preset_selected, self.weak, dialog=dialog))
            setattr(self, name, dialog)
        return dialog

    @property
    def chariot_equip_preset_dialog(self):
        return self.get_chariot_preset_dialog('_chariot_equip_preset_dialog', '战车装备',
            datasets.CHARIOT_EQUIP_HEADS, datasets.CHARIOT_EQUIP_INFOS)
    
    def on_chariot_item_preset_selected(self, view, event, dialog):
        """战车物品预设选中处理"""
        equip = event.index
        data = datasets.CHARIOT_EQUIP_INFOS[equip]
        item_type = models.Chariot.item_type(equip)
        ins = self.chariot_equip_info
        ins.equip = equip
        ins.defense = data[1]
        if dialog.use_weight.checked:
            ins.weight = data[2]
        ins.attr1 = data[3]
        if dialog.use_attr2.checked:
            if item_type != 'engine':
                attr2 = ins.attr2 = data[4]
                if item_type == 'weapon':
                    ins.ammo = attr2

        dialog.endModal()
    
    def on_chariot_item_preset_search(self, _, dialog):
        """预设搜索"""
        value = dialog.search.value
        choices = []
        values = []
        dialog.search_values = values
        i = 0
        for item in datasets.CHARIOT_EQUIP_INFOS:
            if value in item[0]:
                choices.append(item[0])
                values.append(i)
            i += 1
        dialog.search.setItems(choices)
        dialog.search.popup()
    
    def on_chariot_item_preset_search_select(self, view, dialog):
        """点击搜索项定位"""
        list_index = dialog.search_values[view.index]
        dialog.listview.clearSelected()
        dialog.listview.selectItem(list_index)
        dialog.listview.focused_item = list_index

    def show_item_info(self, view, ins, prop):
        """显示物品详情对话框"""
        item = getattr(ins, prop)
        self.item_info.addr = item.addr
        dialog = self.get_item_info_dialog()
        dialog.read()
        dialog.show()

    def show_static_item(self, view):
        """显示静态物品对话框"""
        if self.item_info.addr:
            index = self.item_info.item
            item = self._global.static_items[index - 1]
            self.static_item.addr = item.addr
            dialog = self.get_static_item_dialog()
            dialog.read()
            dialog.show()

    def show_chariot_equip_preset(self, view, key=None):
        """显示预设对话框"""
        item = getattr(self.chariot, key)
        self.chariot_equip_info.addr = item.addr
        dialog = self.chariot_equip_preset_dialog
        equip = self.chariot_equip_info.equip
        if equip < 0x7F:
            dialog.listview.clearSelected()
            dialog.listview.selectItem(equip)
            dialog.listview.focused_item = equip
        dialog.showModal()

    def on_person_change(self, lb):
        index = lb.index
        self.person.set_addr_by_index(index)
        self.person_grow.set_addr_by_index(index)

    def on_chariot_change(self, lb):
        self.chariot.set_addr_by_index(lb.index)

    def on_storage_page(self, page):
        self._global.storage_offset = (page - 1) * self.STORAGE_PAGE_LENGTH
        self.storage_group.read()

    def persons(self):
        person = models.Person(0, self.handler)
        for i in range(len(datasets.PERSONS)):
            person.set_addr_by_index(i)
            yield person

    def chariots(self):
        chariot = models.chariot(0, self.handler)
        for i in range(len(datasets.CHARIOTS)):
            chariot.set_addr_by_index(i)
            yield chariot

    def move_left(self, _):
        self.chariot.posx -= 24

    def move_right(self, _):
        self.chariot.posx += 24

    def move_up(self, _):
        self.chariot.posy -= 24

    def move_down(self, _):
        self.chariot.posy += 24

    def pull_through(self, _):
        for person in self.persons():
            person.hp = person.hpmax

    def equip_all(self, _):
        self.person.equip_all()