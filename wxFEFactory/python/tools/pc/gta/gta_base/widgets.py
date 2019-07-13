from lib import ui
from lib.hack.forms import Group, TwoWayWidget, ModelWidget
from styles import dialog_style


class WeaponWidget(TwoWayWidget):
    def __init__(self, ped, name, label, slot, slot_no_ammo, weapon_list, callback=None):
        self.slot = slot
        self.has_ammo = self.slot not in slot_no_ammo
        self.weapon_list = weapon_list
        self.ped = ped
        self.callback = callback
        super().__init__(name, label, None, None)

    def render(self):
        super().render()
        with ui.Horizontal(class_="fill"):
            self.id_view = ui.Choice(class_="fill", choices=(item[2] for item in self.weapon_list[self.slot]))
            if self.has_ammo:
                self.ammo_view = ui.SpinCtrl(class_="fill", min=0, max=9999, initial=0)
            self.render_btn()

    @property
    def selected_item(self):
        return self.weapon_list[self.slot][self.id_view.index]

    @property
    def mem_value(self):
        ped = self.ped
        if callable(ped):
            ped = ped()
        return ped.weapons[self.slot]

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
        weapon_id = value.id
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
        self.view = ui.Text("", style=self.view_style, class_="input_label")
        self.view.background = 0xaabccc
        self.view.set_on_double_click(self.on_double_click)
        self.view.set_on_left_down(self.onclick)

    def onclick(self, v, e):
        self.read()

    def on_double_click(self, _):
        __class__.cur_view = self
        self.dialog.ShowModal()

    @property
    def dialog(self):
        cls = __class__
        dialog = getattr(cls, '_dialog', None)

        if not dialog:
            with ui.dialog.StdDialog("选择颜色", style=dialog_style) as dialog:
                with ui.GridLayout(cols=13, vgap=10, class_="expand"):
                    for color in self.color_list:
                        view = ui.Text("", style=cls.color_item_style)
                        view.background = color
                        view.set_on_double_click(cls.on_select_color)
            cls._dialog = dialog

        return dialog

    @classmethod
    def on_select_color(cls, item):
        cls.cur_view.view.background = item.background
        cls.cur_view.view.refresh()
        cls.cur_view.write()
        cls.cur_view = None
        cls._dialog.EndModal()

    @property
    def input_value(self):
        return self.color_list.index(self.view.background)

    @input_value.setter
    def input_value(self, value):
        self.view.background = self.color_list[value]
        self.view.refresh()
