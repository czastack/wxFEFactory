from ..base import BaseNdsHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelMultiCheckBox, ModelInput, ModelSelect, ModelFlagWidget, DialogGroup
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib import exui
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
        self.enemy = self.models.Enemy(0, self.handler)
        self.item_index = 1
    
    def render_main(self):
        datasets = self.datasets
        weak = self.weak
        
        with Group("global", "全局", self._global, cols=4):
            ModelInput("money")
            ModelInput("exp")
            ModelInput("stamp")
            ModelInput("game_turn")
            ModelInput("game_time")
            ModelInput("after_money")
            ModelInput("after_exp")
            ModelInput("posx")
            ModelInput("posy")
            ModelSelect("difficulty", choices=datasets.DIFFICULTY)
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
            exui.Label("角色")
            ui.Choice(className="fill", choices=datasets.PERSONS, onselect=self.on_person_change).setSelection(0)
            ModelSelect("figure", choices=datasets.FIGURES)
            ModelInput("level")
            ModelInput("exp")
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
            ModelSelect("weapon_1", choices=datasets.EQUIP_WEAPON.choices, values=datasets.EQUIP_WEAPON.values)
            ModelSelect("weapon_2", choices=datasets.EQUIP_WEAPON.choices, values=datasets.EQUIP_WEAPON.values)
            ModelSelect("weapon_3", choices=datasets.EQUIP_WEAPON.choices, values=datasets.EQUIP_WEAPON.values)
            ModelSelect("equip_head", choices=datasets.EQUIP_HEAD.choices, values=datasets.EQUIP_HEAD.values)
            ModelSelect("equip_body", choices=datasets.EQUIP_BODY.choices, values=datasets.EQUIP_BODY.values)
            ModelSelect("equip_hand", choices=datasets.EQUIP_HAND.choices, values=datasets.EQUIP_HAND.values)
            ModelSelect("equip_foot", choices=datasets.EQUIP_FOOT.choices, values=datasets.EQUIP_FOOT.values)
            ModelSelect("equip_orn", choices=datasets.EQUIP_ORN.choices, values=datasets.EQUIP_ORN.values)
            ModelSelect("prof", choices=datasets.PROFS)
            ModelSelect("subprof", choices=datasets.SUBPROFS)

        self.lazy_group(Group("person_ext", "角色额外", self.person, cols=4), self.render_person_ext)
        self.lazy_group(Group("chariot", "战车", self.chariot), self.render_chariot)
        self.lazy_group(Group("chariot_special_bullets", "特殊炮弹", self.chariot), self.render_chariot_special_bullets)
        self.lazy_group(Group("enemy", "敌人", self.enemy, cols=4), self.render_enemy)

        self.render_package_group()

        with StaticGroup("功能"):
            self.render_functions(('enemy_weak',))

    def get_hotkeys(self):
        this = self.weak
        return (
            ('pull_through', MOD_ALT, getVK('h'), this.pull_through),
        )

    def render_person_ext(self):
        datasets = self.datasets
        for i, label in enumerate(datasets.SUBPROFS[1:]):
            ModelInput("subprof_levels.%d" % i, "%s等级" % label)
            ModelInput("subprof_exps.%d" % i, "%s经验" % label)
        for i in range(self.person.skill_counts.length):
            ModelInput("skill_counts.%d" % i, "技能%d次数" % (i + 1))
        for i in range(self.person.subskill_counts.length):
            ModelInput("subskill_counts.%d" % i, "副职业技能%d次数" % (i + 1))

    def render_chariot(self):
        datasets = self.datasets
        detail_keep_click = lambda key: partial(__class__.show_chariot_item_info, self.weak, key=key, read=False)
        detail_click = lambda key: partial(__class__.show_chariot_item_info, self.weak, key=key)
        preset_click = lambda key: partial(__class__.show_chariot_item_preset, self.weak, dialog_name='chariot_weapon_dialog', key=key)
        preset_ci_click = lambda key: partial(__class__.show_chariot_item_preset, self.weak, dialog_name='chariot_ci_dialog', key=key)

        exui.Label("战车")
        ui.Choice(className="fill", choices=datasets.CHARIOTS, onselect=self.on_chariot_change).setSelection(0)
        ModelInput("sp")
        ModelSelect("chassis", choices=datasets.CHARIOT_CHASSIS.choices, values=datasets.CHARIOT_CHASSIS.values)
        ModelSelect("double_type", choices=datasets.DOUBLE_TYPE)

        exui.Label("C装置")
        with ui.Horizontal(className="right"):
            ui.Button("上次", className="btn_sm", onclick=detail_keep_click("equips.0"))
            ui.Button("详情", className="btn_sm", onclick=detail_click("equips.0"))
            ui.Button("预设", className="btn_sm", onclick=preset_ci_click("equips.0"))
        exui.Label("引擎")
        with ui.Horizontal(className="right"):
            ui.Button("上次", className="btn_sm", onclick=detail_keep_click("equips.1"))
            ui.Button("详情", className="btn_sm", onclick=detail_click("equips.1"))
            ui.Button("预设", className="btn_sm", onclick=preset_ci_click("equips.1"))
        exui.Label("C装置2/引擎2")
        with ui.Horizontal(className="right"):
            ui.Button("上次", className="btn_sm", onclick=detail_keep_click("equips.2"))
            ui.Button("详情", className="btn_sm", onclick=detail_click("equips.2"))
            ui.Button("预设", className="btn_sm", onclick=preset_ci_click("equips.2"))
        for i in range(5):
            exui.Label("炮穴%d" % (i + 1))
            with ui.Horizontal(className="fill"):
                ModelSelect("hole_type.%d" % i, "类型", choices=datasets.HOLE_TYPE, values=datasets.HOLE_TYPE_VALUES)
                ui.Button("上次", className="btn_sm", onclick=detail_keep_click("equips.%d" % (i + 3)))
                ui.Button("详情", className="btn_sm", onclick=detail_click("equips.%d" % (i + 3)))
                ui.Button("预设", className="btn_sm", onclick=preset_click("equips.%d" % (i + 3)))
        for i in range(self.chariot.items.length):
            exui.Label("物品%d" % (i + 1))
            with ui.Horizontal(className="right"):
                ui.Button("上次", className="btn_sm", onclick=detail_keep_click("items.%d" % i))
                ui.Button("详情", className="btn_sm", onclick=detail_click("items.%d" % i))
                ui.Button("C装置/引擎预设", onclick=preset_ci_click("equips.2"))
                ui.Button("武器预设", onclick=preset_click("items.%d" % i))
        with Group.active_group().footer:
            ui.Button("导入字段", onclick=self.weak.load_chariot_fields)
            ui.Button("导出字段", onclick=self.weak.dump_chariot_fields)

    def render_chariot_special_bullets(self):
        datasets = self.datasets
        for i in range(self.chariot.special_bullets.length):
            exui.Label("特殊炮弹%d" % (i + 1))
            with ui.Horizontal(className="fill"):
                ModelSelect("special_bullets.%d.item" % i, "", choices=datasets.SPECIAL_BULLETS.choices, values=datasets.SPECIAL_BULLETS.values)
                ModelInput("special_bullets.%d.count" % i, "数量")

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

    def render_enemy(self):
        datasets = self.datasets
        exui.Label("敌人")
        ui.Choice(className="fill", choices=tuple("敌人%d" % i for i in range(1, 11)), onselect=self.on_enemy_change).setSelection(0)
        ModelSelect("race", choices=datasets.MONSTERS)
        ModelInput("level")
        ModelInput("hp")
        ModelInput("atk")
        ModelInput("defensive")
        ModelInput("hit")
        ModelInput("avoid")
        ModelInput("speed")
        for i, label in enumerate("物火光电音气冷"):
            ModelInput("resistance.%d" % i, "%s抗性" % label).view.setToolTip(">150:○, >100:空, >50:△, <=50:×")

        for i in range(4):
            ModelSelect("enemy_case.%d.race" % i, "种类%d" % (i + 1), ins=self._global, choices=datasets.MONSTERS)
            ModelInput("enemy_case.%d.count" % i, "数量", ins=self._global)

    def get_chariot_item_info_dialog(self):
        datasets = self.datasets
        dialog = getattr(self, 'chariot_item_info_dialog', None)
        if dialog is None:
            with DialogGroup("chariot_item_info", "战车物品详情", self.chariot_item_info, cols=1,
                    dialog_style={'width': 600, 'height': 1200}, horizontal=False, button=False) as dialog:
                ModelSelect("equip", choices=datasets.CHARIOT_ALL_ITEM.choices, values=datasets.CHARIOT_ALL_ITEM.values)
                ModelInput("chaneg")
                ModelInput("ammo")
                ModelInput("level")
                ModelInput("defensive")
                ModelInput("attr1")
                ModelInput("attr2")
                ModelInput("weight")
                ModelInput("status")

            self.chariot_item_info_dialog = dialog
        return dialog

    def get_chariot_item_dialog(self, name, label, head, items):
        """战车物品预设对话框"""
        dialog = getattr(self, name, None)
        if dialog is None:
            chariot_equips = self.chariot_equips
            datasets = self.datasets
            with exui.StdDialog(label, style={'width': 1400, 'height': 900}) as dialog:
                with ui.Horizontal(className="expand"):
                    dialog.search = ui.ComboBox(type="dropdown", className="fill", 
                        onselect=partial(__class__.on_chariot_item_preset_search_select, self.weak, dialog=dialog))
                    ui.Button("搜索", onclick=partial(__class__.on_chariot_item_preset_search, self.weak, dialog=dialog))
                dialog.listview = listview = ui.ListView(className="fill")
                with ui.Horizontal(className="expand"):
                    dialog.use_max = ui.CheckBox(label="最大", className="vcenter", checked=True)
                    dialog.use_weight = ui.CheckBox(label="重量", className="vcenter", checked=True)
                    dialog.use_attr2 = ui.CheckBox(label="武器弹舱/C装置回避", className="vcenter", checked=True)
                dialog.listview.appendColumns(*head)

                dialog.data_list = [] # 读取预设数据时的列表
                dialog.name_list = [] # 搜索时用的名称列表
                for item in items:
                    item_name = datasets.ITEMS[item[0]]
                    part_name = (item_name,) # 名称元祖
                    if isinstance(item[1], tuple):
                        # 多个星级
                        part_id = item[:1]
                        for sub in item[1]:
                            listview.insertItems([part_name + sub + item[2:]])
                            dialog.data_list.append(part_id + sub)
                            dialog.name_list.append(item_name)
                    else:
                        listview.insertItems([part_name + item[1:]])
                        dialog.data_list.append(item)
                        dialog.name_list.append(item_name)
                listview.setOnItemActivated(partial(__class__.on_chariot_item_preset_selected, self.weak, dialog=dialog))
            setattr(self, name, dialog)
        return dialog

    @property
    def chariot_weapon_dialog(self):
        return self.get_chariot_item_dialog('_chariot_weapon_dialog', '战车武器',
            self.chariot_equips.CHARIOT_WEAPON_HEAD, self.chariot_equips.CHARIOT_WEAPON_ITEMS)

    @property
    def chariot_ci_dialog(self):
        return self.get_chariot_item_dialog('_chariot_ci_dialog', '战车C装置/引擎',
            self.chariot_equips.CHARIOT_CI_HEAD, self.chariot_equips.CHARIOT_CI_ITEMS)
    
    def on_chariot_item_preset_selected(self, view, event, dialog):
        """战车物品预设选中处理"""
        data = dialog.data_list[event.index]
        ins = self.chariot_item_info
        use_max = dialog.use_max.checked
        ins.equip = data[0]
        ins.level = data[1]
        ins.attr1 = data[3] if use_max else data[2]
        ins.defensive = data[5] if use_max else data[4]
        if dialog.use_weight.checked:
            ins.weight = data[6]
        if dialog.use_attr2.checked:
            item_type = self.models.Chariot.item_type(data[0])
            if item_type != 'engine':
                attr2 = ins.attr2 = data[8] if use_max else data[7]
                if item_type == 'weapon':
                    # 武器弹舱
                    ins.ammo = attr2

        dialog.endModal()
    
    def on_chariot_item_preset_search(self, _, dialog):
        value = dialog.search.value
        choices = []
        values = []
        dialog.search_values = values
        i = 0
        for name in dialog.name_list:
            if value in name:
                choices.append(name)
                values.append(i)
            i += 1
        dialog.search.setItems(choices)
        dialog.search.popup()
    
    def on_chariot_item_preset_search_select(self, view, dialog):
        list_index = dialog.search_values[view.index]
        dialog.listview.clearSelected()
        dialog.listview.selectItem(list_index)
        dialog.listview.focused_item = list_index

    def show_chariot_item_info(self, view, key=None, read=True):
        """显示详情对话框"""
        item = getattr(self.chariot, key)
        self.chariot_item_info.addr = item.addr
        dialog = self.get_chariot_item_info_dialog()
        if read:
            dialog.read()
        dialog.show()

    def show_chariot_item_preset(self, view, dialog_name=None, key=None):
        """显示预设对话框"""
        item = getattr(self.chariot, key)
        self.chariot_item_info.addr = item.addr
        dialog = getattr(self, dialog_name)
        equip = self.chariot_item_info.equip
        if equip:
            i = 0
            for item in dialog.data_list:
                if item[0] == equip:
                    dialog.listview.clearSelected()
                    dialog.listview.selectItem(i)
                    dialog.listview.focused_item = i
                    break
                i += 1
        dialog.showModal()

    def on_person_change(self, lb):
        self.person.set_addr_by_index(lb.index)

    def on_chariot_change(self, lb):
        self.chariot.set_addr_by_index(lb.index)

    def on_enemy_change(self, lb):
        self.enemy.set_addr_by_index(lb.index)

    def pull_through(self, _):
        for person in self._global.persons:
            person.set_with('hp', 'hpmax')
        for chariot in self._global.chariots:
            chariot.health()

    def enemy_weak(self, _):
        """敌人一击死"""
        for enemy in self._global.enemys:
            enemy.hp = 1

    def load_chariot_fields(self, _):
        super().load_model_fields(self.models.Chariot)

    def dump_chariot_fields(self, _):
        super().dump_model_fields(self.models.Chariot)