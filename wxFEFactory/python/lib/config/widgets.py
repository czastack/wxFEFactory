from abc import ABC, abstractmethod
from lib import extypes
from styles import btn_xsm_style
from . import Configurable
import fefactory_api
ui = fefactory_api.ui


__all__ = ('BoolConfig', 'InputConfig', 'IntConfig', 'FloatConfig')



class ConfigGroup:
    GROUPS = []

    def __init__(self, owner):
        if not isinstance(owner, Configurable):
            raise TypeError('owner must be Configurable object')
        self.owner = owner
        self.children = []

    def __del__(self):
        self.children.clear()

    def appendChild(self, child):
        self.children.append(child)

    def __enter__(self):
        self.GROUPS.append(self)
        return self

    def __exit__(self, *args):
        if self.GROUPS.pop() is not self:
            raise ValueError('GROUPS层次校验失败')
        for field in self.children:
            field.render()
            field.read()
            help_text = getattr(field, 'help', None)
            if help_text is not None:
                field.set_help()

    def read(self, _=None):
        for field in self.children:
            field.read()

    def write(self, _=None):
        for field in self.children:
            field.write()


class ConfigCtrl(ABC):
    def __init__(self, name, label, default):
        parent = ConfigGroup.GROUPS[-1] if len(ConfigGroup.GROUPS) else None

        if not parent:
            raise TypeError('Config Widget must put within ConfigGroup')
        
        self.name = name
        self.label = label
        self.default = default
        parent.appendChild(self)
        self.owner = parent.owner
        self.owner.setDefault(name, default)
        self.owner.registerObserver(name, self._onConfigChange)

    def _onConfigChange(self, config, name, value):
        self.read()

    def __get__(self, obj, type=None):
        return self.get_config_value()

    def __set__(self, obj, value):
        self.set_config_value(value)

    def get_config_value(self):
        return self.owner.getConfig(self.name, self.default)

    def set_config_value(self, value, notity=True):
        return self.owner.setConfig(self.name, value, notity)

    @abstractmethod
    def get_input_value(self):
        pass

    @abstractmethod
    def set_input_value(self, value):
        pass

    def render_lable(self):
        return ui.Text(self.label, className="label_left expand")

    def read(self, _=None):
        self.set_input_value(self.get_config_value())

    def write(self, _=None):
        self.set_config_value(self.get_input_value(), False)

    def render_btn(self):
        ui.Button(label="r", style=btn_xsm_style, onclick=self.read)
        ui.Button(label="w", style=btn_xsm_style, onclick=self.write)

    def set_help(self, text=None):
        if text is None:
            text = self.help
        try:
            self.view.setToolTip(text)
        except Exception:
            self.help = text
        return self

    def onDestroy(self, view):
        """如果self.view有引用本类的函数，必须注册destroy事件以免循环引用"""
        del self.view


class BoolConfig(ConfigCtrl):
    def __init__(self, name, label, default=False):
        super().__init__(name, label, default)

    def render(self):
        ui.Hr()
        self.view = ui.CheckBox(self.label, onchange=self.write)

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
            self.view = ui.TextInput(className="fill", wxstyle=0x0400)
            self.render_btn()
        self.view.setOnKeyDown(self.onKey)
        self.view.setOnDestroy(self.onDestroy)

    def get_input_value(self):
        return self.type(self.view.value)

    def set_input_value(self, value):
        self.view.value = extypes.astr(value)

    def onKey(self, v, event):
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if mod == 0:
            if code == event.getWXK('r'):
                self.read()
                return True
            elif code == event.getWXK('w'):
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
    def __init__(self, name, label, choices, default=None):
        super().__init__(name, label, default)
        if default is None:
            default = choices[0][1]
        self.choices = choices

    def render(self):
        self.render_lable()
        self.view = ui.Choice((item[0] for item in self.choices), className="fill", onselect=self.write)
        self.view.setOnDestroy(self.onDestroy)
        self.view.setSelection(0, True)

    def get_input_value(self):
        return self.choices[self.view.index][1]

    def set_input_value(self, value):
        for i, item in enumerate(self.choices):
            if value == item[1]:
                break
        else:
            return
        self.view.index = i
