from lib import utils
from fefactory_api import ui
from .widgets import BaseGroup, Group, TwoWayWidget, ModelWidget, OffsetsWidget


class PgGroup(Group):
    def render_main(self):
        self.pg = ui.PropertyGrid(class_="fill")


class PgCategory(BaseGroup):
    def __init__(self, label, addr=None, handler=None, cachable=True):
        return super().__init__(None, label, addr, handler, cachable)

    def render(self):
        PgWidget.render(self)
        self.pg.addCategory(self.label)


class PgWidget(TwoWayWidget):
    def render(self):
        group = Group.active_group()
        if not isinstance(group, (PgGroup, PgCategory)):
            raise TypeError('PgWidget父元素必须是PgGroup或PgCategory子类')
        self.pg = group.pg

    def set_help(self):
        self.pg.setHelp(self.name, help)

    @property
    def input_value(self):
        return self.pg.getValue(self.name)

    @input_value.setter
    def input_value(self, value):
        self.pg.setValue(self.name, value)


class PgBaseInput(PgWidget):
    def __init__(self, *args, type=int, hex=False, **kwargs):
        self.type = type
        self.hex = hex
        super().__init__(*args, **kwargs)

    def render(self):
        PgWidget.render(self)
        if self.type is int:
            if self.hex:
                self.pg.addHexProperty(self.label, self.name)
            else:
                self.pg.addIntProperty(self.label, self.name)
        elif self.type is float:
            self.pg.addFloatProperty(self.label, self.name)
        else:
            self.pg.addStringProperty(self.label, self.name)


class PgInput(PgBaseInput, OffsetsWidget):
    pass


class PgModelInput(ModelWidget, PgBaseInput):
    pass


class PgBaseCheckBox(PgWidget):
    def __init__(self, name, label, addr, offsets=(), enable=None, disable=None):
        """
        :param enable: 激活时写入的数据
        :param disable: 关闭时写入的数据
        """
        super().__init__(name, label, addr, offsets)
        self.enable = enable
        self.disable = disable
        self.type = type(enable)

    def render(self):
        PgWidget.render(self)
        self.pg.addBoolProperty(self.label, self.name)

    def toggle(self):
        PgWidget.input_value.__set__(self, not PgWidget.input_value.__get__(self))

    @property
    def input_value(self):
        return self.enable if super().input_value else self.disable

    @input_value.setter
    def input_value(self, value):
        if value == self.enable:
            PgWidget.input_value.__set__(self, True)
        elif self.disable is None or value == self.disable:
            PgWidget.input_value.__set__(self, False)


class PgCheckBox(PgBaseCheckBox, OffsetsWidget):
    pass


class PgModelCheckBox(ModelWidget, PgBaseCheckBox):
    @property
    def input_value(self):
        if self.enable is None:
            return self.pg.getValue(self.name)
        return super().input_value

    @input_value.setter
    def input_value(self, value):
        if self.enable is None:
            self.pg.setValue(self.name, value)
        else:
            PgBaseCheckBox.input_value.__set__(self, value)


class PgBaseSelect(PgWidget):
    def __init__(self, *args, choices=None, values=None, onselect=None, **kwargs):
        # 预处理choices, values
        self.choices, self.values = utils.prepare_option(choices, values)
        self.onselect = onselect
        # self.dragable = dragable
        # if dragable:
        #     parent = self.active_group()
        #     self.parent = parent.weak
        super().__init__(*args, **kwargs)

    def render(self):
        PgWidget.render(self)
        self.pg.addEnumProperty(self.label, self.name, None, self.choices, self.values)

    def setItems(self, choices, values=None):
        self.choices, self.values = utils.prepare_option(choices, values)
        self.pg.setEnumChoices(self.name, self.choices, self.values)


class PgSelect(PgBaseSelect, OffsetsWidget):
    def __init__(self, *args, type=int, size=4, **kwargs):
        self.type = type
        self.size = size
        super().__init__(*args, **kwargs)


class PgModelSelect(ModelWidget, PgBaseSelect):
    pass


class PgBaseChoiceDisplay(PgWidget):
    def __init__(self, *args, choices=None, values=None, **kwargs):
        # 预处理choices, values
        self.choices, self.values = utils.prepare_option(choices, values)
        super().__init__(*args, **kwargs)

    def render(self):
        PgWidget.render(self)
        self.pg.addStringProperty(self.label, self.name)
        self.pg.setReadonly(self.name)

    def setItems(self, choices, values=0):
        self.choices = choices
        if values is not 0:
            self.values = values

    def read(self):
        self.input_value = self.mem_value

    @property
    def input_value(self):
        return None

    @input_value.setter
    def input_value(self, value):
        try:
            index = self.values.index(value) if self.values else value if value < len(self.choices) else -1
        except ValueError:
            index = -1
        PgWidget.input_value.__set__(self, self.choices[index] if index is not -1 else '')


class PgChoiceDisplay(PgBaseChoiceDisplay, OffsetsWidget):
    def __init__(self, *args, size=4, **kwargs):
        self.size = size
        super().__init__(*args, **kwargs)


class PgModelChoiceDisplay(ModelWidget, PgBaseChoiceDisplay):
    pass


class PgBaseFlagWidget(PgWidget):
    def __init__(self, *args, labels=None, values=None, **kwargs):
        """size: hex为True时有用"""
        self.labels = labels
        self.values = values
        super().__init__(*args, **kwargs)

    def render(self):
        PgWidget.render(self)
        self.pg.addFlagsProperty(self.label, self.name, None, self.labels, self.values)


class PgFlagWidget(PgBaseFlagWidget, OffsetsWidget):
    def __init__(self, *args, type=int, size=4, **kwargs):
        self.type = type
        self.size = size
        super().__init__(*args, **kwargs)


class PgModelFlagWidget(ModelWidget, PgBaseFlagWidget):
    pass
