from functools import partial
from lib.hack.forms import Group, StaticGroup, Input, CheckBox, ModelInput, ListFooterButtons
from lib import ui
from ..base import BaseDolphinHack
from . import models, datasets


class Main(BaseDolphinHack):

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self.count_data = {}

    def render_main(self):
        with Group("player", "角色", self._global):
            ModelInput("level", "等级(1+)")
            ModelInput("hp", "生命")
            ModelInput("max_hp", "最大生命")
            ModelInput("money", "金钱")
            ModelInput("power", "力")
            ModelInput("stamina", "体力")
            ModelInput("energy", "气力")
            ModelInput("soul", "魂")
            ModelInput("exp", "经验")

        for group in datasets.LISTS:
            if group['hascount']:
                self.count_data[group['name']] = [0] * len(group['items'])

            self.lazy_group(StaticGroup(group['caption']), partial(self.render_one_list, group))

    def render_one_list(self, group):
        """渲染其中一个列表"""
        li = ui.ListView(class_="fill")
        li.EnableCheckBoxes()
        li.append_columns(*group['head'])
        if group['hascount']:
            li.AppendColumn('数量')
        li.insert_items(group['items'])

        with ui.Horizontal(class_="expand padding_top"):
            uncheck_action = ui.CheckBox(label="不选中表示移除该物品", class_="vcenter")
            if group['hascount']:
                ui.Text("数量 ", class_="vcenter")
                input_num = ui.SpinCtrl(class_="vcenter")
                ui.Text("  ")
                ui.Button(label="修改数量", class_="button", onclick=partial(self.set_count, view=li,
                    group=group, input_num=input_num))
            ListFooterButtons(li)
            ui.Button(label="读取", class_="button",
                onclick=partial(self.list_view_read, view=li, group=group))
            ui.Button(label="写入", class_="button", onclick=partial(self.list_view_write, view=li,
                group=group, uncheck_action=uncheck_action))

    def list_view_read(self, _, view, group):
        field = getattr(self._global, group['name'])
        data = self.handler.read(field.addr, bytes, field.size)
        hascount = group['hascount']

        if hascount:
            numcol = view.GetColumnCount() - 1
            count_data = self.count_data[group['name']]

        for i in range(len(group['items'])):
            if hascount:
                view.SetItem(i, numcol, str(data[i]))
                count_data[i] = data[i]

            if data[i]:
                view.CheckItem(i)

    def list_view_write(self, _, view, group, uncheck_action):
        field = getattr(self._global, group['name'])
        data = bytearray(self.handler.read(field.addr, bytes, field.size))
        hascount = group['hascount']
        # 不选中表示移除该物品
        uncheck_as_no = uncheck_action.checked
        checked = view.get_checked_list()
        if hascount:
            count_data = self.count_data[group['name']]
        for i in range(len(group['items'])):
            if i in checked:
                data[i] = count_data[i] if hascount else 1

            elif uncheck_as_no:
                data[i] = 0

        self.handler.write(field.addr, data, field.size)

    def set_count(self, _, view, group, input_num):
        numcol = view.SetColumnCount() - 1
        for i in view.get_selected_list():
            value = input_num.value
            view.SetItem(i, numcol, str(value))
            self.count_data[group['name']][i] = value
