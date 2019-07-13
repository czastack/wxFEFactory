import json
import fefactory
import fefactory_api
import __main__
from lib import ui, utils, lazy
from lib.extypes import WeakBinder
from lib.win32.keys import WXK
from styles import btn_xs_style, styles, dialog_style
from ..utils import uint_hex


__ALL__ = (
    'Widget', 'TwoWayWidget', 'ModelWidget', 'OffsetsWidget', 'Group', 'DialogGroup', 'StaticGroup', 'GroupBox',
    'Groups', 'Input', 'ModelInput', 'ProxyInput', 'SimpleCheckBox', 'CheckBox', 'ModelCheckBox', 'Select',
    'ModelSelect', 'Choice', 'FlagWidget', 'ModelFlagWidget', 'TabList')


class Widget:
    GROUPS = []
    horizontal = True

    def __init__(self, name, label, addr=None, offsets=(), readonly=False):
        self.weak = WeakBinder(self)
        self.name = name
        self.label = name if label is None else label
        self.addr = addr
        self.offsets = offsets
        self.readonly = readonly

        parent = self.active_group()
        if parent:
            parent.append_child(self)
            if self.addr is None:
                self.addr = getattr(parent, 'addr', None)

            if parent.handler:
                self.handler = parent.handler

        self.oninit()

        if isinstance(parent, Group) and not parent.horizontal:
            self.horizontal = False
            with ui.Vertical(class_="expand"):
                self.render()
            del self.horizontal
        else:
            self.render()

    @classmethod
    def active_group(cls):
        return cls.GROUPS[-1] if len(cls.GROUPS) else None

    def oninit(self):
        """依赖parent的参数都初始化后，render之前执行一些操作"""
        pass

    def render(self):
        ui.Text(self.label, class_="input_label expand" if self.horizontal else "input_label_vertical")

    def render_btn(self):
        this = self.weak
        btn_read = ui.Button(label="r", style=btn_xs_style, onclick=lambda btn: this.read())
        btn_write = (ui.Button(label="w", style=btn_xs_style, onclick=lambda btn: this.write())
            if not self.readonly else None)
        return btn_read, btn_write

    def set_help(self, help):
        if self.view:
            self.view.SetToolTip(help)

    def onkey(self, v, event):
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if mod == 0:
            if code == WXK.R:
                self.read()
                return True
            elif code == WXK.W or code == 13:
                self.write()
                return True
            elif code == WXK('='):
                # 逻辑地址
                print(uint_hex(self.get_addr()))
                return True
        elif mod == WXK.MOD_SHIFT:
            if code == WXK._7:
                # 进程中的地址
                print(uint_hex(self.handler.address_map(self.get_addr())))
                return True
        event.Skip()

    def read(self):
        pass

    def write(self):
        pass

    def get_addr(self):
        return self.addr

    def __repr__(self):
        return '%s("%s", "%s")' % (self.__class__.__name__, self.name, self.label)


class TwoWayWidget(Widget):
    """双向控件"""
    def read(self):
        value = self.mem_value
        if value is not None:
            self.input_value = value

    def write(self):
        if self.readonly:
            return
        value = self.input_value
        if value is not None:
            self.mem_value = value


class ModelWidget:
    """模型绑定控件"""
    def __init__(self, name, label=None, instance=None, prop=None, **kwargs):
        """
        :param instance: Model实例，或者返回Model实例的函数，在Widget中用addr占位
        :param prop: Widget对应Field的属性名称，在Widget中用offsets占位
        """
        super().__init__(name, label, instance, prop or name, **kwargs)

    def oninit(self):
        if isinstance(self.addr, tuple):
            self.addr, self.instance_type = self.addr
        elif not callable(self.addr):
            self.instance_type = type(self.addr)
        else:
            self.instance_type = None

    def render(self):
        if self.label is self.name:
            # 从Field读取label
            field = self.field
            if field and field.label:
                self.label = field.label
        super().render()
        del self.instance_type

    @property
    def instance(self):
        """模型实例"""
        return self.addr() if callable(self.addr) else self.addr

    @property
    def field(self):
        # 尝试获取对应的模型字段
        field = None
        if self.instance_type:
            field = getattr(self.instance_type, self.offsets, None)
        else:
            instance = self.instance
            if instance and hasattr(instance, 'field'):
                field = instance.field(self.offsets)
        return field

    @property
    def mem_value(self):
        instance = self.instance
        if instance:
            return getattr(instance, self.offsets)

    @mem_value.setter
    def mem_value(self, value):
        instance = self.instance
        if instance:
            setattr(instance, self.offsets, value)

    @mem_value.deleter
    def mem_value(self):
        instance = self.instance
        if instance:
            delattr(instance, self.offsets)

    def get_addr(self):
        return self.instance & self.offsets


class OffsetsWidget:
    """多级偏移控件"""
    def get_addr(self):
        return self.addr() if callable(self.addr) else self.addr

    @property
    def mem_value(self):
        ret = self.handler.ptrs_read(self.get_addr(), self.offsets, self.type, self.size)
        if self.type is float:
            ret = utils.float32(ret)
        return ret

    @mem_value.setter
    def mem_value(self, value):
        self.handler.ptrs_write(self.get_addr(), self.offsets, self.type(value), self.size)


class BaseGroup(Widget):
    """基本控件容器"""
    cachable = True

    def __init__(self, name, label, addr=None, handler=None, cachable=True):
        """
        :param addr: 子元素使用ModelWidget时，addr可以是Model实例或者getter或者(instance_getter, instance_type)
            instance_type 方便子元素取label
        :param cachable: 子元素是ModelWidget时有用
        """
        self.children = []
        self.view = None
        origin_addr = addr
        if isinstance(origin_addr, tuple):
            # (instance_getter, instance_type)
            addr = origin_addr[0]
        cachable = cachable and callable(addr)
        if not cachable:
            self.cachable = False
            if handler is None:
                handler = getattr(addr, 'handler', None)
        else:
            self._ins_getter = addr
            self._ins_cached = False
            self._ins = None

        self.handler = handler

        super().__init__(name, label, origin_addr)

        # 处理缓存
        if cachable:
            self.addr = self.weak.cached_ins_getter
            if isinstance(origin_addr, tuple):
                self.addr = (self.addr, origin_addr[1])

    def append_child(self, child):
        self.children.append(child)

    def __enter__(self):
        self.view and self.view.__enter__()
        self.GROUPS.append(self)
        return self

    def __exit__(self, *args):
        self.view and self.view.__exit__(*args)
        if self.GROUPS.pop() is not self:
            raise ValueError('GROUPS层次校验失败')

    def cached_ins_getter(self):
        if self._ins_cached:
            if self._ins is None:
                # 获取Model实例并缓存
                self._ins = self._ins_getter()
            return self._ins

        return self._ins_getter()

    def start_ins_cache(self):
        if self.cachable:
            self._ins_cached = True

    def end_ins_cache(self):
        if self.cachable:
            self._ins_cached = False
            self._ins = None

    def read(self):
        self.start_ins_cache()
        for field in self.children:
            field.read()
        self.end_ins_cache()

    def write(self):
        self.start_ins_cache()
        for field in self.children:
            field.write()
        self.end_ins_cache()

    def load(self):
        """从文件中加载数据"""
        data = fefactory.json_load_file(self)
        if data:
            for field in self.children:
                try:
                    value = data.get(field.name, None)
                    if value is not None:
                        field.input_value = value
                except Exception as e:
                    print("加载字段%s出错" % field.name, e.args)

    def export(self):
        """导出数据到文件"""
        data = {field.name: field.input_value for field in self.children if field.input_value is not None}
        fefactory.json_dump_file(self, data)

    def after_lazy(self):
        """lazy_group渲染后调用"""
        pass


class Group(BaseGroup):
    """通用控件容器，会生成NoteBook的一个tab"""
    cols = 2
    horizontal = True

    def __init__(self, *args, flexgrid=True, hasheader=False, hasfooter=True,
            horizontal=True, serializable=True, cols=None, **kwargs):
        self.flexgrid = flexgrid
        self.hasheader = hasheader
        self.hasfooter = hasfooter
        self.serializable = serializable
        if cols:
            self.cols = cols
        if not horizontal:
            self.horizontal = horizontal
        super().__init__(*args, **kwargs)

    def render(self):
        self.root = self.render_root()

    def render_root(self):
        """渲染外层框架"""
        this = self.weak
        with ui.Vertical(class_="fill", extra={'caption': self.label} if self.label else None) as root:
            if self.hasheader:
                self.header = ui.Horizontal(class_="expand padding")

            self.render_main()

            if self.hasfooter:
                with ui.Horizontal(class_="expand padding") as footer:
                    ui.Button(label="读取", class_="btn_sm", onclick=lambda btn: this.read())
                    ui.Button(label="写入", class_="btn_sm", onclick=lambda btn: this.write())
                    if self.serializable:
                        ui.Button(label="导入", class_="btn_sm", onclick=lambda btn: this.load())
                        ui.Button(label="导出", class_="btn_sm", onclick=lambda btn: this.export())
                self.footer = footer
        del self.flexgrid, self.hasheader, self.hasfooter, self.serializable
        return root

    def render_main(self):
        """渲染主要内容"""
        with ui.ScrollView(class_="fill padding") as content:
            if self.flexgrid:
                self.view = ui.FlexGridLayout(cols=self.cols, vgap=10, hgap=10, class_="fill")
                if self.horizontal:
                    for i in range(self.cols >> 1):
                        self.view.sizer.AddGrowableCol((i << 1) + 1)
                else:
                    for i in range(self.cols):
                        self.view.sizer.AddGrowableCol(i)
            else:
                self.view = content

    def after_lazy(self):
        """延迟加载后的操作"""
        if isinstance(self.view, ui.FlexGridLayout):
            self.view.parent.relayout()


class DialogGroup(Group):
    def __init__(self, *args, closable=True, button=True, **kwargs):
        self.button = button
        self.closable = closable
        self.dialog_style = kwargs.pop('dialog_style', None)
        super().__init__(*args, **kwargs)

    def render(self):
        if self.button:
            ui.Button(label=self.label, onclick=self.weak.show)

        style = dict(dialog_style, **self.dialog_style) if self.dialog_style else dialog_style
        with __main__.win:
            with ui.dialog.StdDialog(self.label, style=style, styles=styles, cancel=False, closable=self.closable) as root:
                self.render_root()

        self.root = root
        del self.button, self.closable

    def show(self, _=None):
        self.root.show()

    def ShowModal(self, _=None):
        self.root.ShowModal()


class StaticGroup(Group):
    """静态容器，不绑定目标"""
    def __init__(self, caption):
        return Group.__init__(self, None, caption, 0, flexgrid=False, hasfooter=False)


class GroupBox(BaseGroup):
    """StaticBox外观的容器"""
    def render(self):
        with ui.StaticBox(self.label, class_="fill") as root:
            self.view = ui.ScrollView(class_="fill padding")

        self.root = root


class VirtualGroup(BaseGroup):
    """虚拟分组"""
    def __init__(self, addr=None, handler=None, cachable=True):
        super().__init__(None, None, addr, handler, cachable)

    def render(self):
        pass


class Groups(BaseGroup):
    """可容纳子Group"""
    def __init__(self, caption, on_page_changed=None, **kwargs):
        self.on_page_changed = on_page_changed
        return super().__init__(None, caption, **kwargs)

    def render(self):
        with ui.Vertical(class_="fill") as root:
            self.view = ui.Notebook(class_="fill")
        if self.label:
            root.extra = dict(caption=self.label)
        self.root = root
        if self.on_page_changed:
            self.view.set_on_page_changed(self.on_page_changed)

    def __enter__(self):
        super().__enter__()
        self.root.freeze()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.root.thaw()
        if self.on_page_changed:
            self.on_page_changed(self.view)


class BaseInput(TwoWayWidget):
    """基类输入框"""
    def __init__(self, *args, hex=False, spin=False, size=4, min=0, max=None, **kwargs):
        """size: hex为True时有用"""
        self.hex = hex and not spin
        self.size = size
        self.spin = spin
        self.min = min
        self.max = max
        super().__init__(*args, **kwargs)

    def render(self):
        super().render()
        with ui.Horizontal(class_="fill") as container:
            if self.spin:
                self.view = ui.SpinCtrl(class_="fill", wxstyle=ui.wx.TE_PROCESS_ENTER | ui.wx.SP_ARROW_KEYS,
                    min=self.min, max=self.max or (1 << (self.size << 3) - 1) - 1)
            else:
                self.view = ui.TextInput(class_="fill", wxstyle=ui.wx.TE_PROCESS_ENTER, readonly=self.readonly)
            self.render_btn()
            self.view.set_on_keydown(self.weak.onkey)
        self.container = container
        del self.min, self.max

    @property
    def input_value(self):
        value = self.view.value
        if not self.spin:
            if value == '':
                return None
            if self.hex or value.startswith('0x'):
                value = int(value, 16)
        return value

    @input_value.setter
    def input_value(self, value):
        if not self.spin:
            value = ("0x%0*X" % (self.size << 1, value)) if self.hex else str(value)
        self.view.value = value


class Input(OffsetsWidget, BaseInput):
    def __init__(self, *args, type=int, **kwargs):
        self.type = type
        super().__init__(*args, **kwargs)


class ModelInput(ModelWidget, BaseInput):
    pass


class ProxyInput(BaseInput):
    """代理输入框"""
    def __init__(self, name, label, getter, setter):
        super().__init__(name, label, None, None)
        self.getter = getter
        self.setter = setter

    @property
    def mem_value(self):
        return self.getter()

    @mem_value.setter
    def mem_value(self, value):
        self.setter(value)


class SimpleCheckBox(Widget):
    """采用切换事件的立即模式"""
    def __init__(self, name, label, addr=None, offsets=(), enable=None, disable=None, size=None):
        """
        :param enable: 激活时写入的数据
        :param disable: 关闭时写入的数据
        """
        super().__init__(name, label, addr, offsets)
        self.enable = enable
        self.disable = disable
        if size is None:
            if isinstance(enable, bytes):
                size = len(enable)
            else:
                size = 4
        self.size = size

    def render(self):
        self.view = ui.CheckBox(self.label, onchange=self.weak.onchange)

    def onchange(self, checkbox):
        data = self.enable if checkbox.checked else self.disable
        self.handler.ptrs_write(self.addr, self.offsets, data, self.size)


class BaseCheckBox(TwoWayWidget):
    def __init__(self, name, label, addr=None, offsets=(), enable=None, disable=None, alone=False):
        """
        :param enable: 激活时写入的数据
        :param disable: 关闭时写入的数据
        """
        self.alone = alone
        self.enable = enable
        self.disable = disable
        self.type = type(enable)
        super().__init__(name, label, addr, offsets)

    def render(self):
        label = self.label
        if self.alone:
            self.label = ''
        super().render()
        if self.alone:
            self.label = label
        with ui.Horizontal(class_="fill") as container:
            self.view = ui.CheckBox("" if not self.alone else label, class_="fill")
            self.render_btn()
        self.container = container

    def toggle(self):
        self.view.toggle()

    @property
    def input_value(self):
        return self.enable if self.view.checked else self.disable

    @input_value.setter
    def input_value(self, value):
        if value == self.enable:
            self.view.checked = True
        elif self.disable is None or value == self.disable:
            self.view.checked = False


class CheckBox(OffsetsWidget, BaseCheckBox):
    pass


class ModelCheckBox(ModelWidget, BaseCheckBox):
    @property
    def input_value(self):
        if self.enable is None:
            return self.view.checked
        return super().input_value

    @input_value.setter
    def input_value(self, value):
        if self.enable is None:
            self.view.checked = value
        else:
            BaseCheckBox.input_value.__set__(self, value)


class BaseSelect(TwoWayWidget):
    """基类下拉框"""
    search_map = {}

    def __init__(self, *args, choices=None, values=None, onselect=None, dragable=False, **kwargs):
        # 预处理choices, values
        self.choices, self.values = utils.prepare_option(choices, values)
        self.onselect = onselect
        self.dragable = dragable
        if dragable:
            parent = self.active_group()
            self.parent = parent.weak
        super().__init__(*args, **kwargs)

    def render(self):
        super().render()
        with ui.Horizontal(class_="fill") as container:
            self.view = ui.Choice(class_="fill", choices=self.choices, onselect=self.onselect)
            self.view.set_context_menu(self.contextmenu)
            self.view.set_on_destroy(self.weak.on_destroy)
            self.render_btn()
        self.container = container
        self.view.set_on_keydown(self.weak.onkey)
        if self.dragable:
            self.view.set_on_left_down(self.weak.on_left_down)
            self.view.set_on_text_drop(self.weak.on_text_drop)
        self.search_map[id(self.view)] = self

    def Set(self, choices, values=0):
        self.choices = choices
        self.view.Set(choices)
        if values is not 0:
            self.values = values

    def read(self):
        self.input_value = self.mem_value

    @property
    def input_value(self):
        index = self.view.index
        if index is -1:
            return None
        return self.values[index] if self.values else index

    @input_value.setter
    def input_value(self, value):
        try:
            self.view.index = self.values.index(value) if self.values else (
                value if value is not None and value < len(self.choices) else -1)
        except ValueError:
            self.view.index = -1
            # print(hex(value), "不在%s的可选值中" % self.label)
        if self.onselect:
            self.onselect(self.view)

    @lazy.classlazy
    def contextmenu(cls):
        """右键菜单"""
        with ui.ContextMenu() as contextmenu:
            ui.MenuItem("搜索(&S)", onselect=cls.menu_search)
            ui.MenuItem("拖拽帮助", onselect=cls.move_about)
        return contextmenu

    @lazy.classlazy
    def search_dialog(cls):
        return ui.dialog.SearchDialog("搜索", onselect=cls.onsearch_select, onsearch=cls.onsearch)

    @classmethod
    def menu_search(cls, view, menu):
        cls.active_ins = cls.search_map[id(view)]
        if getattr(cls, 'search_last_choices', None) is not cls.active_ins.choices:
            cls.search_dialog.listbox.clear()
        else:
            cls.search_dialog.listbox.index = -1
        cls.search_dialog.ShowModal()
        del cls.active_ins

    @classmethod
    def move_about(cls, view, menu):
        fefactory_api.alert("按住shift，在下拉框上按下鼠标左键，拖拽到同源下拉框上释放，能交换两者的选值；\n"
            "若释放时按着ctrl，则为复制值；若按着alt，则是把值移到目标处，原有区域下移或上移")

    @classmethod
    def onsearch(cls, dialog, value):
        choices = []
        values = []
        i = 0
        for item in cls.active_ins.choices:
            if value in item:
                choices.append(item)
                values.append(i)
            i += 1
        cls.search_dialog.listbox.Set(choices)
        cls.search_last_choices = cls.active_ins.choices  # 上次搜索的内容集
        cls.search_values = values

    @classmethod
    def onsearch_select(cls, view):
        # 搜索结果选择后切换到对应的序号
        cls.active_ins.view.set_selection(cls.search_values[view.index], True)
        cls.search_dialog.EndModal()

    def on_destroy(self, view):
        self.search_map.pop(id(view), None)

    def on_left_down(self, view, event):
        if fefactory_api.GetKeyState(WXK.SHIFT):
            view.start_text_drag(str(id(self.view)))
            return False

    def on_text_drop(self, i):
        """拖动事件"""
        if i.isdigit():
            instance = self.search_map.get(int(i), None)
            if instance and self != instance:
                if instance.choices == self.choices:
                    ctrl = fefactory_api.GetKeyState(WXK.CONTROL)
                    value = instance.view.index
                    if not ctrl:
                        alt = fefactory_api.GetKeyState(WXK.ALT)
                        if not alt:
                            # 交换
                            instance.view.index = self.view.index
                        else:
                            # 区域变化
                            try:
                                sibling = self.parent.children
                                a = sibling.index(instance)
                                b = sibling.index(self)
                                if a < b:
                                    # 往下拖动
                                    for i in range(a, b):
                                        sibling[i].view.index = sibling[i + 1].view.index
                                else:
                                    # 往上拖动
                                    for i in range(a, b, -1):
                                        sibling[i].view.index = sibling[i - 1].view.index
                            except Exception:
                                pass
                    self.view.index = value
                else:
                    print("数据源不一致")

    class CacheContex:
        """选项数组缓存，避免重复C++类型转换"""
        def __enter__(self):
            ui.wx.start_cache()
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            ui.wx.Choice.end_cache()

    choices_cache = CacheContex()


class Select(OffsetsWidget, BaseSelect):
    def __init__(self, *args, type=int, size=4, **kwargs):
        self.type = type
        self.size = size
        super().__init__(*args, **kwargs)


class ModelSelect(ModelWidget, BaseSelect):
    pass


class BaseChoiceDisplay(Widget):
    """静态选项(只显示)"""
    def __init__(self, *args, choices=None, values=None, **kwargs):
        # 预处理choices, values
        self.choices, self.values = utils.prepare_option(choices, values)
        kwargs['readonly'] = True
        super().__init__(*args, **kwargs)

    def render(self):
        super().render()
        with ui.Horizontal(class_="fill") as container:
            self.view = ui.TextInput(class_="fill", wxstyle=ui.wx.TE_PROCESS_ENTER, readonly=True)
            self.render_btn()
        self.view.set_on_keydown(self.weak.onkey)
        self.container = container

    def Set(self, choices, values=0):
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
        self.view.value = self.choices[index] if index is not -1 else ''


class ChoiceDisplay(OffsetsWidget, BaseChoiceDisplay):
    def __init__(self, *args, type=int, size=4, **kwargs):
        self.type = type
        self.size = size
        super().__init__(*args, **kwargs)


class ModelChoiceDisplay(ModelWidget, BaseChoiceDisplay):
    pass


def Choice(laebl, choices, onselect):
    """选项框"""
    ui.Label(laebl)
    return ui.Choice(class_="fill", choices=choices, onselect=onselect).set_selection(0)


def Title(label):
    """标题"""
    ui.Hr()
    return ui.Text(label)


class BaseFlagWidget(TwoWayWidget):
    """参数组合"""
    def __init__(self, *args, labels=None, helps=None, values=None, checkbtn=False, cols=None, **kwargs):
        """size: hex为True时有用"""
        self.labels = labels
        self.helps = helps
        self.values = values or tuple(1 << i for i in range(len(labels)))
        self.checkbtn = checkbtn
        self.cols = cols
        super().__init__(*args, **kwargs)

    def render(self):
        ui.Text(self.label, class_="form_label expand")
        with ui.Horizontal(class_="fill") as container:
            if self.cols is not None:
                view = ui.GridLayout(cols=self.cols, vgap=10, class_="fill")
            else:
                view = ui.Horizontal(class_="fill")
            with view:
                self.views = tuple(
                    ui.CheckBox(label) for label in self.labels
                )
                if self.helps:
                    for view, help in zip(self.views, self.helps):
                        view.SetToolTip(help)
            if self.checkbtn:
                ui.Button(label="全选", style=btn_xs_style, onclick=self.weak.check_all)
                ui.Button(label="不选", style=btn_xs_style, onclick=self.weak.uncheck_all)
            self.render_btn()
        self.view = view
        self.container = container
        self.helps, self.cols

    @property
    def input_value(self):
        value = 0
        for i in range(len(self.labels)):
            if self.views[i].checked:
                value |= self.values[i]

        return value

    @input_value.setter
    def input_value(self, value):
        for i in range(len(self.labels)):
            self.views[i].checked = value & self.values[i]

    def check_all(self, _=None):
        for view in self.views:
            view.checked = True

    def uncheck_all(self, _=None):
        for view in self.views:
            view.checked = False


class FlagWidget(OffsetsWidget, BaseFlagWidget):
    def __init__(self, *args, type=int, size=4, **kwargs):
        self.type = type
        self.size = size
        super().__init__(*args, **kwargs)


class ModelFlagWidget(ModelWidget, BaseFlagWidget):
    pass


class ModelArrayWidget(ModelWidget, Widget):
    def get_labels(self):
        field = self.field

        if self.label is self.name:
            if field and field.label:
                self.label = field.label

        if isinstance(self.label, str):
            labels = ["%s%d" % (self.label, i + 1) for i in range(field.length)]
        else:
            labels = self.label
        return field, labels


class ModelArrayInput(ModelArrayWidget):
    """输入框数组"""
    def render(self):
        field, labels = self.get_labels()
        self.children = [ModelInput('%s.%d' % (self.name, i), label=labels[i])
            for i in range(field.length)]


class ModelArraySelect(ModelArrayWidget):
    """下拉框数组"""
    def __init__(self, *args, choices=None, **kwargs):
        self.choices = choices
        super().__init__(*args, **kwargs)

    def render(self):
        field, labels = self.get_labels()
        with ModelSelect.choices_cache:
            self.children = [ModelSelect('%s.%d' % (self.name, i), label=labels[i], choices=self.choices)
                for i in range(field.length)]


def TabList(data):
    """多个tab的列表框"""
    book = ui.Notebook(class_="fill", wxstyle=0x0200)
    with book:
        for category in data:
            ui.ListBox(class_="expand", choices=(item[0] for item in category[1]), extra=dict(caption=category[0]))
    return book


class ListFooterButtons:
    """渲染带复选框列表的底部按钮"""
    def __init__(self, li):
        self.li = li
        ui.Button(label="全选", class_="button", onclick=lambda btn: li.checkall())
        ui.Button(label="全不选", class_="button", onclick=lambda btn: li.checkall(False))
        ui.Button(label="勾选高亮", class_="button", onclick=lambda btn: li.check_selection())
        ui.Button(label="导出勾选", class_="button", onclick=self.dump_checked)
        ui.Button(label="导入勾选", class_="button", onclick=self.load_checked)

    def dump_checked(self, _):
        """导出勾选"""
        fefactory.json_dump_file(self, self.li.get_checked_list())

    def load_checked(self, _):
        """导入勾选"""
        self.li.set_checked_list(fefactory.json_load_file(self))
