from fefactory_api import ui
from lib.hack.form import Group, TwoWayWidget, ModelWidget
from commonstyle import dialog_style


class WeaponWidget(TwoWayWidget):
    def __init__(self, name, label, slot, slot_no_ammo, weapon_list, player, callback=None):
         self.slot = slot
         self.has_ammo = self.slot not in slot_no_ammo
         self.weapon_list = weapon_list
         self.player = player
         self.callback = callback
         super().__init__(name, label, None, None)

    def render(self):
        super().render()
        with ui.Horizontal(className="fill"):
            self.id_view = ui.Choice(className="fill", choices=(item[2] for item in self.weapon_list[self.slot]))
            if self.has_ammo:
                self.ammo_view = ui.SpinCtrl(className="fill", min=0, max=9999, initial=0)
            self.render_btn()

    @property
    def selected_item(self):
        return self.weapon_list[self.slot][self.id_view.index]

    @property
    def mem_value(self):
        player = self.player
        if callable(player):
            player = player()
        return player.weapons[self.slot]

    @mem_value.setter
    def mem_value(self, value):
        self.mem_value.set(value)
        if self.callback:
            self.callback(self)

    @property
    def input_value(self):
        id_ = self.selected_item[0]
        ammo = self.ammo_view.value if self.has_ammo else 0
        return (id_, ammo)

    @input_value.setter
    def input_value(self, value):
        weapon_id =  value.id
        i = 0
        for item in self.weapon_list[self.slot]:
            if item[0] == weapon_id:
                break
            i += 1
        else:
            return
        self.id_view.index = i
        if self.has_ammo:
            self.ammo_view.value = value.ammo


class ColorWidget(ModelWidget, TwoWayWidget):
    view_style = {'width': 50}
    color_item_style = {'width': 35, 'height': 35}

    def __init__(self, name, label, ins, prop, color_list):
        super().__init__(name, label, ins, prop)
        self.color_list = color_list

    def render(self):
        super().render()
        self.view = ui.Text("", style=self.view_style, className="label_left")
        self.view.background = 0xaabccc
        self.view.setOnDoubleClick(self.onDoubleClick)
        self.view.setOnClick(self.onClick)

    def onClick(self, _):
        self.read()

    def onDoubleClick(self, _):
        __class__.cur_view = self
        self.dialog.showModal()

    @property
    def dialog(self):
        cls = __class__
        dialog = getattr(cls, '_dialog', None)

        if not dialog:
            with ui.StdModalDialog("选择颜色", style=dialog_style) as dialog:
                with ui.GridLayout(cols=13, vgap=10, className="fill container"):
                    for color in self.color_list:
                        view = ui.Text("", style=cls.color_item_style)
                        view.background = color
                        view.setOnDoubleClick(cls.onSelectColor)
            cls._dialog = dialog

        return dialog

    @classmethod
    def onSelectColor(cls, item):
        cls.cur_view.view.background = item.background
        cls.cur_view.view.refresh()
        cls.cur_view.write()
        cls.cur_view = None
        cls._dialog.endModal()

    @property
    def input_value(self):
        return self.color_list.index(self.view.background)

    @input_value.setter
    def input_value(self, value):
        self.view.background = self.color_list[value]
        self.view.refresh()