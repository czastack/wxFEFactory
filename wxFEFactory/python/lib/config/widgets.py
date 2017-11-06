from abc import ABC, abstractmethod
from lib import extypes
from . import Configurable
import fefactory_api
ui = fefactory_api.ui


__all__ = ('BoolConfig', 'InputConfig', 'IntConfig', 'FloatConfig')


class BaseConfig(ABC):
    def __init__(self, owner, name, label, default):
        if not isinstance(owner, Configurable):
            raise ValueError('owner must be Configurable object')
        setattr(owner, name, self)
        self.owner = owner
        self.name = name
        self.label = label
        self.default = default
        owner.registerObserver(name, self._onConfigChange)
        self.read()

    def _onConfigChange(self, config, key, value):
        self.onConfigChange(value)

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
        ui.Button(label="r", style=btn_style, onclick=self.read)
        ui.Button(label="w", style=btn_style, onclick=self.write)


class BoolConfig(BaseConfig):
    def __init__(self, owner, name, label, default=False):
        self.view = ui.CheckBox(label, onchange=self.write)
        super().__init__(owner, name, label, default)

    def get_input_value(self):
        return self.view.checked

    def set_input_value(self, value):
        self.view.checked = value


class InputConfig(BaseConfig):
    def __init__(self, owner, name, label, default, type):
        super().__init__(owner, name, label, default)
        self.type = type
        self.render_lable()
        self.view = ui.TextInput(className="fill", wxstyle=0x0400)
        self.render_btn()
        self.view.setOnKeyDown(self.onKey)

    def get_input_value(self):
        return self.type(self.view.value)

    def set_input_value(self, value):
        self.value = extypes.astr(value)

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
    def __init__(self, *args, **kwargs):
        kwargs['type'] = int
        kwargs.setdefault('default', 0)
        return super().__init__(*args, **kwargs)


class FloatConfig(InputConfig):
    def __init__(self, *args, **kwargs):
        kwargs['type'] = float
        kwargs.setdefault('default', 0.0)
        return super().__init__(*args, **kwargs)


btn_style = {
    'width': 36,
}