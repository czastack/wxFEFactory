from fefactory_api import ui
from lib.hack.form import Group, TwoWayWidget, ModelWidget
from commonstyle import dialog_style
from . import models, address
from .data import SLOT_NO_AMMO, WEAPON_LIST


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