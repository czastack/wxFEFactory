from fefactory_api import ui
from lib.hack.form import ModelWidget, TwoWayWidget
from lib.utils import rgb2bgr
from styles import btn_sm_style


class WeaponWidget(TwoWayWidget):
    def __init__(self, ped, name, label, weapon, has_ammo=True, callback=None):
         self._ped = ped
         self.weapon = weapon
         self.has_ammo = has_ammo
         self.callback = callback
         super().__init__(name, label, None, None)

    def render(self):
        super().render()
        with ui.Horizontal(className="fill"):
            if self.has_ammo:
                self.ammo_view = ui.SpinCtrl(className="fill", min=0, max=9999, initial=0)
                ui.Button("最大", style=btn_sm_style, onclick=self.max_ammo)
            ui.Button("移除", style=btn_sm_style, onclick=self.remove_weapon)
            self.render_btn()

    @property
    def ped(self):
        ped = self._ped
        if callable(ped):
            ped = ped()
        return ped

    @property
    def mem_value(self):
        ped = self.ped
        return ped.get_ammo(self.weapon)

    @mem_value.setter
    def mem_value(self, value):
        """ value: 弹药数 """
        ped = self.ped
        if ped.has_weapon(self.weapon):
            ped.set_ammo(self.weapon, value)
            # 切换到当前武器
            ped.weapon = self.weapon
        else:
            ped.give_weapon(self.weapon, value)
            if self.callback:
                self.callback(self)

    @property
    def input_value(self):
        return self.ammo_view.value if self.has_ammo else 0

    @input_value.setter
    def input_value(self, value):
        ped = self.ped
        if self.has_ammo:
            if ped.has_weapon(self.weapon):
                self.ammo_view.value = value
            else:
                self.ammo_view.value = 0

    def max_ammo(self, _=None):
        ammo = self.ped.get_max_ammo(self.weapon)
        self.mem_value = ammo
        self.input_value = ammo

    def remove_weapon(self, _=None):
        self.ped.remove_weapon(self.weapon)


class CustomColorWidget(ModelWidget, TwoWayWidget):
    def render(self):
        super().render()
        with ui.Horizontal(className="fill"):
            self.view = ui.ColorPicker(className="vcenter", onchange=lambda v: self.write())
            self.render_btn()
            ui.Button("清除", onclick=self.clear_color)

    def clear_color(self, _=None):
        del self.mem_value

    @property
    def input_value(self):
        return rgb2bgr(self.view.color)

    @input_value.setter
    def input_value(self, value):
        self.view.color = rgb2bgr(value)