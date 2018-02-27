from functools import partial
from ..base import BaseDolphinHack
from . import models, datasets
from lib.hack.form import Group, StaticGroup, InputWidget, CheckBoxWidget, ModelInputWidget
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseDolphinHack):

    def __init__(self):
        super().__init__()
        self._ram = models.Ram(0, self.handler)
        self.count_data = {}

    def check_attach(self, _=None):
        if super().check_attach():
            self._ram.addr = self.ramaddr
            return True
        return False
    
    def render_main(self):
        with Group("player", "角色", self._ram, handler=self.handler):
            ModelInputWidget("level", "等级(1+)")
            ModelInputWidget("hp", "生命")
            ModelInputWidget("max_hp", "最大生命")
            ModelInputWidget("money", "金钱")
            ModelInputWidget("power", "力")
            ModelInputWidget("stamina", "体力")
            ModelInputWidget("energy", "气力")
            ModelInputWidget("soul", "魂")
            ModelInputWidget("exp", "经验")

        for group in datasets.LISTS:
            if group['hascount']:
                self.count_data[group['name']] = [0] * len(group['items'])

            with StaticGroup(group['caption']):
                li = ui.ListView(className="fill")
                li.enableCheckboxes()
                li.appendColumns(*group['head'])
                if group['hascount']:
                    li.appendColumn('数量')
                li.insertItems(group['items'])

                with ui.Horizontal(className="expand"):
                    uncheck_action = ui.CheckBox(label="不选中表示移除该物品", className="vcenter")
                    if group['hascount']:
                        ui.Text("数量 ", className="vcenter")
                        input_num = ui.SpinCtrl(className="vcenter")
                        ui.Text("  ")
                        ui.Button(label="修改数量", className="button", 
                            onclick=partial(self.set_count, view=li, group=group, input_num=input_num)).setToolTip('勾选高亮选中的项的数量')
                    ui.Button(label="勾选选中", className="button", onclick=partial(self.list_view_check_select, view=li)).setToolTip('勾选高亮选中的项')
                    ui.Button(label="全选", className="button", onclick=partial(self.list_view_checkall, view=li))
                    ui.Button(label="全不选", className="button", onclick=partial(self.list_view_uncheckall, view=li))
                    ui.Button(label="读取", className="button", onclick=partial(self.list_view_read, view=li, group=group))
                    ui.Button(label="写入", className="button", onclick=partial(self.list_view_write, view=li, group=group, uncheck_action=uncheck_action))

    # def onListSelect(self, view, event):
    #     index = event.index
    #     view.checkItem(index, not view.isItemChecked(index))

    def list_view_check_select(self, _, view):
        for i in view.getSelectedList():
            view.checkItem(i, not view.isItemChecked(i))

    def list_view_checkall(self, _, view):
        view.checkAll()

    def list_view_uncheckall(self, _, view):
        view.checkAll(False)

    def list_view_read(self, _, view, group):
        field = getattr(self._ram, group['name'])
        data = self.handler.read(field.addr, bytes, field.size)
        hascount = group['hascount']

        if hascount:
            numcol = view.getColumnCount() - 1
            count_data = self.count_data[group['name']]
        
        for i in range(len(group['items'])):
            if hascount:
                view.setItem(i, numcol, str(data[i]))
                count_data[i] = data[i]
        
            if data[i]:
                view.checkItem(i)


    def list_view_write(self, _, view, group, uncheck_action):
        field = getattr(self._ram, group['name'])
        data = bytearray(self.handler.read(field.addr, bytes, field.size))
        hascount = group['hascount']
        # 不选中表示移除该物品
        uncheck_as_no = uncheck_action.checked
        checked = view.getCheckedList()
        if hascount:
            count_data = self.count_data[group['name']]
        for i in range(len(group['items'])):
            if i in checked:
                data[i] = count_data[i] if hascount else 1

            elif uncheck_as_no:
                data[i] = 0

        self.handler.write(field.addr, data, field.size)

    def set_count(self, _, view, group, input_num):
        numcol = view.getColumnCount() - 1
        for i in view.getSelectedList():
            value = input_num.value
            view.setItem(i, numcol, str(value))
            self.count_data[group['name']][i] = value