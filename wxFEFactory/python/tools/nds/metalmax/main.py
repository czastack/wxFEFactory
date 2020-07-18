import abc
from lib import ui
from lib.hack.forms import (
    Group, Groups, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelChoiceDisplay, DialogGroup, Choice
)
from lib.ui.components import Pagination
from lib.win32.keys import VK
from functools import partial
from ..base import BaseNdsHack


class MetalMaxHack(BaseNdsHack):
    IREM_PAGE_LENGTH = 9

    @abc.abstractproperty
    def models(self):
        pass

    @abc.abstractproperty
    def datasets(self):
        pass

    @abc.abstractproperty
    def chariot_equips(self):
        pass

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self._global.train_items_offset = 0
        self.person = self.models.Person(0, self.handler)
        self.chariot = self.models.Chariot(0, self.handler)
        self.chariot_item_info = self.models.ChariotItemInfo(0, self.handler)
        self.enemy = self.models.Enemy(0, self.handler)
        self.has_holes = self.chariot.field('hole_type') is not None

    def render_main(self):
        with Group("global", "全局", self._global, cols=4):
            ModelInput("money")
            ModelInput("stamp")
            self.render_global_ext()

        self.lazy_group(Group("person", "角色", self.person, cols=4), self.render_person)
        self.lazy_group(Group("person_ext", "角色额外", self.person, cols=4), self.render_person_ext)
        self.lazy_group(Group("chariot", "战车", self.chariot, cols=4), self.render_chariot)
        self.lazy_group(Group("chariot_items", "战车物品/装备", self.chariot, cols=2 if self.has_holes else 4),
            self.render_chariot_items)
        self.lazy_group(Group("chariot_special_bullets", "特殊炮弹", self.chariot), self.render_chariot_special_bullets)
        self.lazy_group(Group("battle_status", "战斗状态", self._global, cols=4), self.render_battle_status)
        self.lazy_group(Group("enemy", "敌人", self.enemy, cols=4), self.render_enemy)
        self.lazy_group(Groups("包裹", self.weak.on_page_changed), self.render_package_group)
        self.render_ext()

        with StaticGroup("功能"):
            self.render_buttons(('enemy_weak',))

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    def render_global_ext(self):
        pass

    def render_person(self):
        datasets = self.datasets
        Choice("角色", datasets.PERSONS, self.on_person_change)
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
        with ModelSelect.choices_cache:
            ModelSelect("weapon_1", choices=datasets.EQUIP_WEAPON.choices, values=datasets.EQUIP_WEAPON.values)
            ModelSelect("weapon_2", choices=datasets.EQUIP_WEAPON.choices, values=datasets.EQUIP_WEAPON.values)
            ModelSelect("weapon_3", choices=datasets.EQUIP_WEAPON.choices, values=datasets.EQUIP_WEAPON.values)
        ModelSelect("equip_head", choices=datasets.EQUIP_HEAD.choices, values=datasets.EQUIP_HEAD.values)
        ModelSelect("equip_body", choices=datasets.EQUIP_BODY.choices, values=datasets.EQUIP_BODY.values)
        ModelSelect("equip_hand", choices=datasets.EQUIP_HAND.choices, values=datasets.EQUIP_HAND.values)
        ModelSelect("equip_foot", choices=datasets.EQUIP_FOOT.choices, values=datasets.EQUIP_FOOT.values)
        ModelSelect("equip_orn", choices=datasets.EQUIP_ORN.choices, values=datasets.EQUIP_ORN.values)
        ModelInput("atk1")
        ModelInput("atk2")
        ModelInput("atk3")
        ModelInput("defense")

        for i, label in enumerate("火光电声气冰"):
            ModelInput("resistance.%d" % i, "%s抗性" % label, spin=True, max=100)

        ModelSelect("prof", choices=datasets.PROFS)
        if self.person.field("subprof"):
            ModelSelect("subprof", choices=datasets.SUBPROFS)

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

        Choice("战车", datasets.CHARIOTS, self.on_chariot_change)
        ModelInput("sp")
        ModelSelect("chassis.equip", "底盘", choices=datasets.CHARIOT_CHASSIS.choices,
            values=datasets.CHARIOT_CHASSIS.values)
        ModelInput("chassis.defense", "底盘防御")
        ModelInput("chassis.attr1", "荷台").set_help('道具容量，最大18个')
        ModelInput("chassis.attr2", "弹舱")
        ModelSelect("chassis.change", "双持类型", choices=datasets.DOUBLE_TYPE)
        ModelInput("chassis.weight", "底盘重量")

    def render_chariot_items(self):
        datasets = self.datasets

        show_chariot_item_info = self.__class__.show_chariot_item_info
        show_chariot_item_preset = self.__class__.show_chariot_item_preset

        def detail_keep_click(key):
            return partial(show_chariot_item_info, self.weak, key=key, read=False)

        def detail_click(key):
            return partial(show_chariot_item_info, self.weak, key=key)

        def preset_click(key):
            return partial(show_chariot_item_preset, self.weak, dialog_name='chariot_weapon_dialog', key=key)

        def preset_ci_click(key):
            return partial(show_chariot_item_preset, self.weak, dialog_name='chariot_ci_dialog', key=key)

        item_choices = self.datasets.CHARIOT_ALL_ITEM.choices
        item_values = self.datasets.CHARIOT_ALL_ITEM.values

        with ModelChoiceDisplay("equips.0.equip", "C装置", choices=item_choices, values=item_values).container:
            ui.Button("上次", class_="btn_sm", onclick=detail_keep_click("equips.0"))
            ui.Button("详情", class_="btn_sm", onclick=detail_click("equips.0"))
            ui.Button("预设", class_="btn_sm", onclick=preset_ci_click("equips.0"))
        with ModelChoiceDisplay("equips.1.equip", "引擎", choices=item_choices, values=item_values).container:
            ui.Button("上次", class_="btn_sm", onclick=detail_keep_click("equips.1"))
            ui.Button("详情", class_="btn_sm", onclick=detail_click("equips.1"))
            ui.Button("预设", class_="btn_sm", onclick=preset_ci_click("equips.1"))
        with ModelChoiceDisplay("equips.2.equip", "C装置2/引擎2", choices=item_choices, values=item_values).container:
            ui.Button("上次", class_="btn_sm", onclick=detail_keep_click("equips.2"))
            ui.Button("详情", class_="btn_sm", onclick=detail_click("equips.2"))
            ui.Button("预设", class_="btn_sm", onclick=preset_ci_click("equips.2"))
        for i in range(5):
            key = "equips.%d" % (i + 3)
            ui.Label("炮穴%d" % (i + 1))
            with ui.Horizontal(class_="fill"):
                if self.has_holes:
                    ModelSelect("hole_type.%d" % i, "类型", choices=datasets.HOLE_TYPES)
                ModelChoiceDisplay(key + '.equip', "", choices=item_choices, values=item_values)
                ui.Button("上次", class_="btn_sm", onclick=detail_keep_click(key))
                ui.Button("详情", class_="btn_sm", onclick=detail_click(key))
                ui.Button("预设", class_="btn_sm", onclick=preset_click(key))
        for i in range(self.chariot.items.length):
            key = "items.%d" % i
            with ModelChoiceDisplay(
                    key + '.item', "物品%d" % (i + 1),
                    choices=item_choices, values=item_values).container:
                ui.Button("上次", class_="btn_sm", onclick=detail_keep_click(key))
                ui.Button("详情", class_="btn_sm", onclick=detail_click(key))
                ui.Button("C装置/引擎", onclick=preset_ci_click(key))
                ui.Button("武器", class_="btn_sm", onclick=preset_click(key))
        with Group.active_group().footer:
            ui.Button("导入字段", onclick=self.weak.load_chariot_fields)
            ui.Button("导出字段", onclick=self.weak.dump_chariot_fields)

    def render_chariot_special_bullets(self):
        datasets = self.datasets
        with ModelSelect.choices_cache:
            for i in range(self.chariot.special_bullets.length):
                ui.Label("特殊炮弹%d" % (i + 1))
                with ui.Horizontal(class_="fill"):
                    ModelSelect("special_bullets.%d.item" % i, "", choices=datasets.SPECIAL_BULLETS.choices,
                        values=datasets.SPECIAL_BULLETS.values)
                    ModelInput("special_bullets.%d.count" % i, "数量")

    def render_package_group(self):
        datasets = self.datasets

        def on_page_change(self, page, item=None):
            setattr(self._global, "{}_offset".format(item['key']), (page - 1) * self.IREM_PAGE_LENGTH)
            item['group'].read()

        def render_items(self, item=None):
            with ModelSelect.choices_cache:
                for i in range(self.IREM_PAGE_LENGTH):
                    ModelSelect("{0}.{1}+{0}_offset.item".format(item['key'], i), "",
                        choices=item['source'].choices, values=item['source'].values)
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

    def render_battle_status(self):
        for i in range(self._global.chariot_battle_status.length):
            ModelInput("chariot_battle_status.%d.sp" % i, "战车%d装甲" % (i + 1))
            ModelInput("chariot_battle_status.%d.spmax" % i, "最大装甲")

    def render_enemy(self):
        datasets = self.datasets
        Choice("敌人", tuple("敌人%d" % i for i in range(1, 11)), self.on_enemy_change)
        ModelSelect("race", choices=datasets.MONSTERS)
        ModelInput("level")
        ModelInput("hp")
        ModelInput("atk")
        ModelInput("defense")
        ModelInput("hit")
        ModelInput("avoid")
        ModelInput("speed")
        for i, label in enumerate("物火光电音气冷"):
            ModelInput("resistance.%d" % i, "%s抗性" % label, spin=True, min=-100, max=100).set_help(
                "○<=-50, -50<●<=-20, 20<空<30, 30<=△<80, 80<=×")

        with ModelSelect.choices_cache:
            for i in range(4):
                ModelSelect("enemy_case.%d.race" % i, "种类%d" % (i + 1),
                    instance=self._global, choices=datasets.MONSTERS)
                ModelInput("enemy_case.%d.count" % i, "数量", instance=self._global)

    def render_ext(self):
        pass

    def get_chariot_item_info_dialog(self):
        datasets = self.datasets
        name = 'chariot_item_info_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(None, "战车物品详情", self.chariot_item_info, cols=1,
                    dialog_style={'width': 600, 'height': 1200},
                    closable=False, horizontal=False, button=False) as dialog:
                ModelSelect("equip", choices=datasets.CHARIOT_ALL_ITEM.choices, values=datasets.CHARIOT_ALL_ITEM.values)
                ModelInput("change")
                ModelInput("ammo")
                ModelInput("star")
                ModelInput("defense")
                ModelInput("attr1")
                ModelInput("attr2")
                ModelInput("weight")
                ModelInput("status")

            setattr(self, name, dialog)
        return dialog

    def get_chariot_item_dialog(self, name, label, head, items):
        """战车物品预设对话框"""
        dialog = getattr(self, name, None)
        if dialog is None:
            datasets = self.datasets
            with ui.dialog.StdDialog(label, parent=self.win, style={'width': 1400, 'height': 900},
                                     cancel=False, closable=False) as dialog:
                with ui.Horizontal(class_="expand"):
                    dialog.search = ui.ComboBox(wxstyle=ui.wx.CB_DROPDOWN, class_="fill",
                        onselect=partial(self.__class__.on_chariot_item_preset_search_select, self.weak, dialog=dialog))
                    ui.Button("搜索", onclick=partial(self.__class__.on_chariot_item_preset_search,
                              self.weak, dialog=dialog))
                dialog.listview = listview = ui.ListView(class_="fill")
                with ui.Horizontal(class_="expand"):
                    dialog.use_max = ui.CheckBox(label="最大", class_="vcenter", checked=True)
                    dialog.use_weight = ui.CheckBox(label="重量", class_="vcenter", checked=True)
                    dialog.use_attr2 = ui.CheckBox(label="武器弹舱/C装置回避", class_="vcenter", checked=True)
                dialog.listview.append_columns(*head)

                dialog.data_list = []  # 读取预设数据时的列表
                dialog.name_list = []  # 搜索时用的名称列表
                for item in items:
                    item_name = datasets.ITEMS[item[0]]
                    part_name = (item_name,)  # 名称元祖
                    if isinstance(item[1], tuple):
                        # 多个星级
                        part_id = item[:1]
                        for sub in item[1]:
                            listview.insert_items([part_name + sub + item[2:]])
                            dialog.data_list.append(part_id + sub)
                            dialog.name_list.append(item_name)
                    else:
                        listview.insert_items([part_name + item[1:]])
                        dialog.data_list.append(item)
                        dialog.name_list.append(item_name)
                listview.set_on_item_activated(partial(self.__class__.on_chariot_item_preset_selected,
                    self.weak, dialog=dialog))
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
        data = dialog.data_list[event.GetSelection()]
        ins = self.chariot_item_info
        use_max = dialog.use_max.checked
        item_type = self.models.Chariot.item_type(data[0])
        ins.equip = data[0]
        ins.star = data[1]
        ins.attr1 = data[3] if use_max and item_type != 'engine' else data[2]
        ins.defense = data[5] if use_max else data[4]
        if dialog.use_weight.checked:
            ins.weight = data[6]
        if dialog.use_attr2.checked:
            if item_type != 'engine':
                attr2 = ins.attr2 = data[8] if use_max else data[7]
                if item_type == 'weapon':
                    # 武器弹舱
                    ins.ammo = attr2

        dialog.EndModal()

    def on_chariot_item_preset_search(self, _, dialog):
        """预设搜索"""
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
        dialog.search.Set(choices)
        dialog.search.Popup()

    def on_chariot_item_preset_search_select(self, view, dialog):
        """点击搜索项定位"""
        list_index = dialog.search_values[view.index]
        dialog.listview.clear_selected()
        dialog.listview.Select(list_index)
        dialog.listview.Focus(list_index)

    def show_chariot_item_info(self, view, key=None, read=True):
        """显示详情对话框"""
        item = getattr(self.chariot, key)
        self.chariot_item_info.addr = item.addr
        dialog = self.get_chariot_item_info_dialog()
        if read and self.handler.active:
            dialog.read()
        dialog.show()

    def show_chariot_item_preset(self, view, dialog_name=None, key=None):
        """显示预设对话框"""
        item = getattr(self.chariot, key)
        self.chariot_item_info.addr = item.addr
        dialog = getattr(self, dialog_name)
        equip = self.handler.active and self.chariot_item_info.equip
        if equip:
            i = 0
            for item in dialog.data_list:
                if item[0] == equip:
                    # 尝试匹配星级
                    star = self.chariot_item_info.star
                    for j in range(min(4, len(dialog.data_list) - i)):
                        item = dialog.data_list[i + j]
                        if item[0] == equip and item[1] == star:
                            i = i + j
                            break
                    dialog.listview.clear_selected()
                    dialog.listview.Select(i)
                    dialog.listview.Focus(i)
                    break
                i += 1
        dialog.ShowModal()

    def on_person_change(self, lb):
        self.person.set_addr_by_index(lb.index)

    def on_chariot_change(self, lb):
        self.chariot.set_addr_by_index(lb.index)

    def on_enemy_change(self, lb):
        self.enemy.set_addr_by_index(lb.index)

    def pull_through(self):
        for person in self._global.persons:
            person.set_with('hp', 'hpmax')
        for item in self._global.chariot_battle_status:
            item.set_with('sp', 'spmax')

    def enemy_weak(self, _):
        """敌人一击死"""
        for enemy in self._global.enemys:
            enemy.hp = 1

    def load_chariot_fields(self, _):
        super().load_model_fields(self.chariot)

    def dump_chariot_fields(self, _):
        super().dump_model_fields(self.chariot)
