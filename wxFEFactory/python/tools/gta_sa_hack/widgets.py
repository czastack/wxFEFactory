from fefactory_api import ui
from lib.hack.form import Group, TwoWayWidget, ModelWidget
from commonstyle import dialog_style
from . import models, address
from .data import color_list, SLOT_NO_AMMO, WEAPON_LIST


class WeaponWidget(TwoWayWidget):
    def __init__(self, name, label, slot):
         self.slot = slot
         self.has_ammo = self.slot not in SLOT_NO_AMMO
         super().__init__(name, label, None, None)

    def render(self):
        super().render()
        with ui.Horizontal(className="fill"):
            self.id_view = ui.Choice(className="fill", choices=(item[2] for item in WEAPON_LIST[self.slot]))
            if self.has_ammo:
                self.ammo_view = ui.SpinCtrl(className="fill", min=0, max=9999, initial=0)
            self.render_btn()

    @property
    def mem_value(self):
        handler = self._handler
        return models.Player(handler.read32(address.PLAYER_BASE), handler).weapons[self.slot]

    @mem_value.setter
    def mem_value(self, value):
        self.mem_value.set(value)

    @property
    def input_value(self):
        id_ = WEAPON_LIST[self.slot][self.id_view.index][0]
        ammo = self.ammo_view.value if self.has_ammo else 0
        return (id_, ammo)

    @input_value.setter
    def input_value(self, value):
        weapon_id =  value.id
        i = 0
        for item in WEAPON_LIST[self.slot]:
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

    def __init__(self, name, label, ins, prop):
        super().__init__(name, label, ins, prop)

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
                    for color in color_list:
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
        return color_list.index(self.view.background)

    @input_value.setter
    def input_value(self, value):
        self.view.background = color_list[value]
        self.view.refresh()