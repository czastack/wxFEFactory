from abc import ABC, abstractmethod
from lib import extypes, wxconst, utils
from styles import btn_xs_style
from lib import exui
from lib.extypes import WeakBinder
from lib.win32.keys import WXK
from .group import ConfigGroup
from fefactory_api import ui


__all__ = ('BoolConfig', 'InputConfig', 'IntConfig', 'FloatConfig')


class ConfigCtrl(ABC):
    def __init__(self, name, label, default):
        parent = ConfigGroup.active_group()

        if not parent:
            raise TypeError('Config Widget must be within ConfigGroup')

        self.weak = WeakBinder(self)
        self.name = name
        self.label = label
        self.default = default
        parent.append_child(self)
        self.owner = parent.owner
        self.owner.setdefault(name, default)
        self.owner.register_observer(name, self.weak._onConfigChange)

    def _onConfigChange(self, config, name, value):
        self.read()

    def __get__(self, obj, type=None):
        return self.get_config_value()

    def __set__(self, obj, value):
        self.set_config_value(value)

    def get_config_value(self):
        return self.owner.getconfig(self.name, self.default)

    def set_config_value(self, value, notity=True):
        return self.owner.setconfig(self.name, value, notity)

    @abstractmethod
    def get_input_value(self):
        pass

    @abstractmethod
    def set_input_value(self, value):
        pass

    def render_lable(self):
        return exui.Label(self.label)

    def read(self, _=None):
        self.set_input_value(self.get_config_value())

    def write(self, _=None):
        self.set_config_value(self.get_input_value(), False)

    def render_btn(self):
        this = self.weak
        ui.Button(label="r", style=btn_xs_style, onclick=this.read)
        ui.Button(label="w", style=btn_xs_style, onclick=this.write)

    def set_help(self, text=None):
        if text is None:
            text = self.help
        try:
            self.view.setToolTip(text)
        except Exception:
            self.help = text
        return self


class BoolConfig(ConfigCtrl):
    def __init__(self, name, label, default=False):
        super().__init__(name, label, default)

    def render(self):
        ui.Hr()
        self.view = ui.CheckBox(self.label, onchange=self.weak.write)

    def get_input_value(self):
        return self.view.checked

    def set_input_value(self, value):
        self.view.checked = value


class InputConfig(ConfigCtrl):
    def __init__(self, name, label, default, type):
        super().__init__(name, label, default)
        self.type = type

    def render(self):
        self.render_lable()
        with ui.Horizontal(className="fill"):
            self.view = ui.TextInput(className="fill", wxstyle=wxconst.TE_PROCESS_ENTER)
            self.render_btn()
        self.view.setOnKeyDown(self.weak.onKey)

    def get_input_value(self):
        return self.type(self.view.value)

    def set_input_value(self, value):
        self.view.value = extypes.astr(value)

    def onKey(self, v, event):
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if mod == 0:
            if code == WXK.R:
                self.read()
                return True
            elif code == WXK.W:
                self.write()
                return True
        event.Skip()


class IntConfig(InputConfig):
    def __init__(self, name, label, default=0):
        return super().__init__(name, label, default, int)


class FloatConfig(InputConfig):
    def __init__(self, name, label, default=0.0):
        return super().__init__(name, label, default, float)


class SelectConfig(ConfigCtrl):
    def __init__(self, name, label, choices, values=None, default=None):
        self.choices, self.values = utils.prepare_option(choices, values)
        if default is None:
            default = self.values[1] if self.values else 0
        super().__init__(name, label, default)

    def render(self):
        self.render_lable()
        self.view = ui.Choice(self.choices, className="fill", onselect=self.weak.write)
        self.view.setSelection(0, True)

    def get_input_value(self):
        index = self.view.index
        if index is -1:
            return None
        return self.values[index] if self.values else index

    def set_input_value(self, value):
        try:
            self.view.index = self.values.index(value) if self.values else value if value < len(self.choices) else -1
        except ValueError:
            self.view.index = -1
