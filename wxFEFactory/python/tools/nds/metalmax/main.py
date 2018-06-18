from ..base import BaseNdsHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelMultiCheckBox, ModelInput, ModelSelect, ModelFlagWidget, DialogGroup
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
from fefactory_api import ui
from functools import partial


class MetalMaxHack(BaseNdsHack):
    IREM_PAGE_LENGTH = 9

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self._global.train_items_offset = 0
        self.person = self.models.Person(0, self.handler)
        self.chariot = self.models.Chariot(0, self.handler)
        self.chariot_item_info = self.models.ChariotItemInfo(0, self.handler)
        self.item_index = 1
    
    def render_main(self):
        datasets = self.datasets
        weak = self.weak
        
        with Group("global", "全局", self._global, cols=4):
            ModelInput("money")
            ModelInput("exp")
            ModelInput("stamp")
            ModelInput("game_time")
            ModelInput("after_money")
            ModelInput("after_exp")
            ModelSelect("after_money_rate", choices=datasets.RATE, values=datasets.RATE_VALUES)
            ModelSelect("after_exp_rate", choices=datasets.RATE, values=datasets.RATE_VALUES)
            ModelCheckBox("quick_switch")
            ModelCheckBox("quick_move")
            ModelCheckBox("must_winning")
            ModelCheckBox("tool_count_keep")
            ModelCheckBox("ammo_keep")
            ModelMultiCheckBox("level_up_max")
            ModelMultiCheckBox("weight_zero")
            ModelMultiCheckBox("equip_limit_remove")
            ModelMultiCheckBox("without_material")
            ModelCheckBox("twin_engines")
            ModelCheckBox("drop_item_three_star")
            ModelCheckBox("no_battle")
            ModelCheckBox("must_drop_item")
            ModelCheckBox("must_first")
            ModelMultiCheckBox("through_wall")

        with Group("player", "角色", self.person, cols=4):
            ui.Text("角色", className="input_label expand")
            ui.Choice(className="fill", choices=datasets.PERSONS, onselect=self.on_person_change).setSelection(0)
            ModelInput("hp")
            ModelInput("hpmax")
            ModelInput("battle_level")
            ModelInput("drive_level")
            ModelInput("power")
            ModelInput("strength")
            ModelInput("speed")
            ModelInput("spirit")
            ModelInput("scar")
            ModelInput("level_max")
            ModelSelect("subprof", choices=datasets.SUBPROFS)
            ModelSelect("weapon_1", choices=datasets.EQUIP_WEAPON.choices, values=datasets.EQUIP_WEAPON.values)
            ModelSelect("weapon_2", choices=datasets.EQUIP_WEAPON.choices, values=datasets.EQUIP_WEAPON.values)
            ModelSelect("weapon_3", choices=datasets.EQUIP_WEAPON.choices, values=datasets.EQUIP_WEAPON.values)
            ModelSelect("equip_head", choices=datasets.EQUIP_HEAD.choices, values=datasets.EQUIP_HEAD.values)
            ModelSelect("equip_body", choices=datasets.EQUIP_BODY.choices, values=datasets.EQUIP_BODY.values)
            ModelSelect("equip_hand", choices=datasets.EQUIP_HAND.choices, values=datasets.EQUIP_HAND.values)
            ModelSelect("equip_foot", choices=datasets.EQUIP_FOOT.choices, values=datasets.EQUIP_FOOT.values)
            ModelSelect("equip_orn", choices=datasets.EQUIP_ORN.choices, values=datasets.EQUIP_ORN.values)

        self.lazy_group(Group("chariot", "战车", self.chariot), self.render_chariot)
        self.lazy_group(Group("chariot_items", "战车物品", self.chariot), self.render_chariot_items)

        self.render_package_group()

        with DialogGroup("chariot_item_info", "战车物品详情", self.chariot_item_info, cols=1,
                dialog_style={'width': 600, 'height': 1200}, horizontal=False, button=False) as chariot_item_info_dialog:
            ModelInput("chaneg")
            ModelInput("ammo")
            ModelInput("level")
            ModelInput("defensive")
            ModelInput("attr1")
            ModelInput("attr2")
            ModelInput("weight")

            self.chariot_item_info_dialog = chariot_item_info_dialog

    def render_chariot(self):
        datasets = self.datasets
        ui.Text("战车", className="input_label expand")
        ui.Choice(className="fill", choices=datasets.CHARIOTS, onselect=self.on_chariot_change).setSelection(0)
        ModelInput("sp")
        ModelSelect("chassis", choices=datasets.CHARIOT_CHASSIS.choices, values=datasets.CHARIOT_CHASSIS.values)
        ModelSelect("double_type", choices=datasets.DOUBLE_TYPE)
        with ModelSelect("equips.0.equip", "C装置", choices=datasets.CHARIOT_CONTROL.choices, values=datasets.CHARIOT_CONTROL.values).container:
            ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_chariot_item_info, self.weak, key="equips.0"))
        with ModelSelect("equips.1.equip", "引擎", choices=datasets.CHARIOT_ENGINE.choices, values=datasets.CHARIOT_ENGINE.values).container:
            ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_chariot_item_info, self.weak, key="equips.1"))
        with ModelSelect("equips.2.equip", "C装置2/引擎2", choices=datasets.CHARIOT_CONTROL_ENGINE.choices, values=datasets.CHARIOT_CONTROL_ENGINE.values).container:
            ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_chariot_item_info, self.weak, key="equips.2"))
        for i in range(5):
            ui.Text("炮穴%d" % (i + 1), className="input_label expand")
            with ui.Horizontal(className="fill"):
                ModelSelect("hole_type.%d" % i, "类型", choices=datasets.HOLE_TYPE, values=datasets.HOLE_TYPE_VALUES)
                ModelSelect("equips.%d.equip" % (i + 3), "装备", choices=datasets.CHARIOT_WEAPON.choices, values=datasets.CHARIOT_WEAPON.values)
                ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_chariot_item_info, self.weak, key="equips.%d" % (i + 3)))

    def render_chariot_items(self):
        datasets = self.datasets
        for i in range(self.chariot.items.length):
            with ModelSelect("items.%d.item" % i, "物品%d" % (i + 1), choices=datasets.CHARIOT_ALL_ITEM.choices, values=datasets.CHARIOT_ALL_ITEM.values).container:
                ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_chariot_item_info, self.weak, key="items.%d" % i))

    def render_package_group(self):
        datasets = self.datasets

        def on_page_change(self, page, item=None):
            setattr(self._global, "{}_offset".format(item['key']), (page - 1) * self.IREM_PAGE_LENGTH)
            item['group'].read()

        def render_items(self, item=None):
            for i in range(self.IREM_PAGE_LENGTH):
                ModelSelect("{0}.{1}+{0}_offset.item".format(item['key'], i), "", choices=item['source'].choices, values=item['source'].values)
                ModelInput("{0}.{1}+{0}_offset.count".format(item['key'], i), "数量")
            with Group.active_group().footer:
                Pagination(partial(on_page_change, self.weak, item=item), item['page_count'])

        for item in (
            {'key': 'humen_items', 'label': '道具', 'source': datasets.HUMEN_ITEM, 'page_count': 25},
            {'key': 'potions', 'label': '恢复道具', 'source': datasets.POTION, 'page_count': 3},
            {'key': 'battle_items', 'label': '战斗道具', 'source': datasets.BATTLE_ITEM, 'page_count': 6},
            {'key': 'equips', 'label': '装备', 'source': datasets.ALL_EQUIP, 'page_count': 45},
        ):
            item['group'] = Group(item['key'], item['label'], self._global, cols=4)
            self.lazy_group(item['group'], partial(render_items, self.weak, item=item))
            setattr(self._global, "{}_offset".format(item['key']), 0)

    def get_hotkeys(self):
        this = self.weak
        return (
            ('pull_through', MOD_ALT, getVK('h'), this.pull_through),
        )

    def on_person_change(self, lb):
        self.person.set_addr_by_index(lb.index)

    def on_chariot_change(self, lb):
        self.chariot.set_addr_by_index(lb.index)

    def show_chariot_item_info(self, view, key=None):
        item = getattr(self.chariot, key)
        self.chariot_item_info.addr = item.addr
        self.chariot_item_info_dialog.read()
        self.chariot_item_info_dialog.showModal()

    def pull_through(self, _):
        for person in self._global.persons:
            person.set_with('hp', 'hpmax')
        for chariot in self._global.chariots:
            chariot.health()