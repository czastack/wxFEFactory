import abc
from lib import extypes, utils
from styles import btn_xs_style
from lib import ui
from lib.extypes import WeakBinder
from lib.win32.keys import WXK
from .group import ConfigGroup


__all__ = ('BoolConfig', 'InputConfig', 'IntConfig', 'FloatConfig')


class ConfigCtrl(abc.ABC):
    """配置项控件"""

    def __init__(self, name, label, default, help=None):
        parent = ConfigGroup.active_group()

        if not parent:
            raise TypeError('Config Widget must be within ConfigGroup')

        parent.append_child(self)
        self.weak = WeakBinder(self)
        self.name = name
        self.label = label
        self.default = default
        self.help = help
        self.owner = parent.owner
        self.owner.setdefault(name, default)
        self.owner.register_observer(name, self.weak._on_config_change)
        self.view = None

    def _on_config_change(self, config, name, value):
        self.read()

    def __get__(self, obj, type=None):
        return self.get_config_value()

    def __set__(self, obj, value):
        self.set_config_value(value)

    def get_config_value(self):
        return self.owner.getconfig(self.name, self.default)

    def set_config_value(self, value, notity=True):
        return self.owner.setconfig(self.name, value, notity)

    @abc.abstractmethod
    def get_input_value(self):
        """获取控件的输入值"""
        pass

    @abc.abstractmethod
    def set_input_value(self, value):
        """设置控件的输入值"""
        pass

    def render_lable(self):
        """渲染标签文本"""
        return ui.Label(self.label)

    def read(self, _=None):
        self.set_input_value(self.get_config_value())

    def write(self, _=None):
        self.set_config_value(self.get_input_value(), False)

    def render_btn(self):
        """渲染按钮"""
        this = self.weak
        ui.Button(label="r", style=btn_xs_style, onclick=this.read)
        ui.Button(label="w", style=btn_xs_style, onclick=this.write)

    def set_help(self, text=None):
        """设置帮助内容"""
        if text is None:
            text = self.help
        try:
            self.view.SetToolTip(text)
        except Exception:
            self.help = text
        return self


class BoolConfig(ConfigCtrl):
    """布尔值控件"""
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
    """输入控件"""
    def __init__(self, name, label, default, type):
        super().__init__(name, label, default)
        self.type = type

    def render(self):
        self.render_lable()
        with ui.Horizontal(class_="fill"):
            self.view = ui.TextInput(class_="fill", wxstyle=ui.wx.TE_PROCESS_ENTER)
            self.render_btn()
        self.view.set_on_keydown(self.weak.onkey)

    def get_input_value(self):
        return self.type(self.view.value)

    def set_input_value(self, value):
        self.view.value = extypes.astr(value)

    def onkey(self, v, event):
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if mod == 0:
            if code == WXK.R or code == WXK.SPACE:
                self.read()
                return True
            elif code == WXK.W or WXK.ENTER:
                self.write()
                return True
        event.Skip()


class IntConfig(InputConfig):
    """整型输入控件"""
    def __init__(self, name, label, default=0):
        super().__init__(name, label, default, int)


class FloatConfig(InputConfig):
    """浮点型输入控件"""
    def __init__(self, name, label, default=0.0):
        super().__init__(name, label, default, float)


class SelectConfig(ConfigCtrl):
    """下拉框控件"""
    def __init__(self, name, label, choices, values=None, default=None):
        self.choices, self.values = utils.prepare_option(choices, values)
        if default is None:
            default = self.values[1] if self.values else 0
        super().__init__(name, label, default)

    def render(self):
        self.render_lable()
        self.view = ui.Choice(self.choices, class_="fill", onselect=self.weak.write)
        self.view.set_selection(0, True)

    def get_input_value(self):
        index = self.view.index
        if index == -1:
            return None
        return self.values[index] if self.values else index

    def set_input_value(self, value):
        try:
            self.view.index = self.values.index(value) if self.values else value if value < len(self.choices) else -1
        except ValueError:
            self.view.index = -1
