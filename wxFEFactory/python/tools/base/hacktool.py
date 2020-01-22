import abc
import traceback
import base64
import fefactory
import __main__
from .basetool import NestedTool
from lib.config import Config, ConfigGroup
from lib.hack.forms import Widget, BaseGroup
from lib.hack.handlers import ProxyHandler
from lib import ui


class BaseHackTool(NestedTool):
    handler_class = None

    @abc.abstractmethod
    def render_main(self):
        pass

    def __init__(self):
        super().__init__()
        self.config = Config("configs/%s.config.json" % self.module_name + '')
        if callable(self.handler_class):
            self.handler = self.handler_class()

    def attach(self, frame):
        super().attach(frame)
        return self.check_attach()

    def render(self):
        with self.render_win() as win:
            with ui.Vertical():
                with ui.Horizontal(class_="expand padding"):
                    ui.Button("检测", class_="vcenter", onclick=self.check_attach)
                    self.render_top_button()
                    self.attach_status_view = ui.Text("", class_="vcenter grow padding_left")
                    ui.CheckBox("保持最前", class_="vcenter", onchange=self.switch_keeptop)
                with ui.Notebook(class_="fill") as book:
                    book.set_on_page_changed(self.on_page_changed)
                    self.begin_group()
                    try:
                        self.render_main()
                        self.on_page_changed(book)
                    except Exception:
                        win.Close()
                        raise
                    self.end_group()

        return win

    def check_attach(self, _=None):
        """检查运行目标程序状态"""
        if self.handler.active:
            self.ondetach()

        succeed = self.handler.attach()
        if succeed or succeed is None and self.handler.attach_window(self.CLASS_NAME, self.WINDOW_NAME):
            self.attach_status_view.label = (self.WINDOW_NAME or self.CLASS_NAME) + ' 正在运行'

            if not self.win.hotkey_map:
                hotkeys = self.get_hotkeys()
                if hotkeys:
                    self.win.register_hotkeys(hotkeys)
            self.onattach()
            return True
        else:
            self.attach_status_view.label = '没有检测到 ' + (self.WINDOW_NAME or self.CLASS_NAME)
            return False

    def get_hotkeys(self):
        """重写这个函数，返回要注册的热键列表"""
        return ()

    @property
    def CLASS_NAME(self):
        return self.handler.CLASS_NAME

    @property
    def WINDOW_NAME(self):
        return getattr(self.handler, 'WINDOW_NAME', None) or self.CLASS_NAME

    def onclose(self, *args):
        if self.handler.active:
            self.ondetach()
        self.config.write()
        return super().onclose(*args)

    def lazy_group(self, group, fn, depend=None):
        """延迟加载的group"""
        groups = getattr(self, 'lazy_groups', None)
        if groups is None:
            self.lazy_groups = groups = {}

        item = groups[group.root] = group, fn, depend
        return item

    def handle_lazy_group(self, root):
        """处理延迟加载的group"""
        item = self.lazy_groups.get(root, None)
        if item:
            group, fn, depend = item
            if depend:
                self.handle_lazy_group(depend)
            with group:
                if fn() is False:
                    return
                # 释放tmp_style_list
                if group.view.keep_styles:
                    group.view.keep_styles = False
            group.after_lazy()
            del self.lazy_groups[root]

    def on_page_changed(self, book):
        groups = getattr(self, 'lazy_groups', None)
        if groups:
            root = book.get_page()
            if root:
                self.handle_lazy_group(root)

    def begin_group(self):
        Widget.GROUPS.append(self)
        ConfigGroup.GROUPS.append(self)
        self.groups = []

    def append_child(self, child):
        if isinstance(child, (BaseGroup, ConfigGroup)):
            self.groups.append(child)
        else:
            raise ValueError("子元素必须是lib.hack.forms.BaseGroup或lib.config.group.ConfigGroup的实例")

    def end_group(self):
        if Widget.GROUPS.pop() is not self:
            raise ValueError("Widget Group层级校验失败")
        if ConfigGroup.GROUPS.pop() is not self:
            raise ValueError("ConfigGroup Group层级校验失败")

    def discard_config(self, _=None):
        """放弃修改的配置"""
        self.config.cancel_change()

    def switch_keeptop(self, view):
        """切换置顶"""
        win = __main__.win if self.nested else self.win
        win.keeptop = view.checked

    def read_vector(self, addr):
        """ 在addr读三个float类型
        :return: (x, y, z)
        """
        r = self.handler.read_float
        return (r(addr), r(addr + 4), r(addr + 8))

    def onattach(self):
        if self.key_hook:
            self.win.setHook(self.handler.thread_id)

    def ondetach(self):
        pass

    def custom_hotkey(self, _=None):
        """用于自定义的临时热键功能"""
        fn = getattr(self, 'cfn', None)
        if fn:
            fn()

    def toggle_setting(self, name, default=False):
        """切换设置"""
        toggle = not getattr(self, name, default)
        setattr(self, name, toggle)
        return toggle

    def get_cache(self, name, key, fn):
        """ 获取缓存的内容
        :param fn: 缓存不存在时通过fn(key)获取
        """
        cache_name = '_cache_' + name
        cache = getattr(self, cache_name, None)
        if cache is None:
            cache = {}
            setattr(self, cache_name, cache)

        value = cache.get(key, None)
        if value is None:
            value = cache[key] = fn(key)
        return value

    def set_cfn(self, btn, menu=None):
        """绑定alt+c事件"""
        self.cfn = btn.click

    def render_top_button(self):
        """渲染额外顶部按钮"""
        pass

    def render_functions(self, names, cols=4):
        """渲染功能按钮"""
        with ui.GridLayout(cols=cols, vgap=10, class_="expand"):
            for name in names:
                func = getattr(self.weak, name)
                ui.Button(func.__doc__, onclick=func)

    def set_buttons_contextmenu(self):
        parent = ui.View.active_layout()
        with ui.ContextMenu() as contextmenu:
            ui.MenuItem("设为alt+c快捷键(&C)", onselect=self.set_cfn)
        for btn in parent.children:
            btn.set_context_menu(contextmenu)

    def load_model_fields(self, instance):
        """导入模型字段数据"""
        data = fefactory.json_load_file(self)
        if not data:
            return

        model = type(instance)
        if data['model'] != model.__name__:
            print('Model不匹配，需要的Model为%s，读取到的为%s' % (data['model'], model.__name__))
            return

        names = tuple(data['data'].keys())
        exportable_fields = [model.field(name) for name in names]
        choices = [field.label or names[i] for i, field in enumerate(exportable_fields)]
        dialog = ui.dialog.ListDialog("选择导出的字段", listbox={'choices': choices})
        if dialog.ShowModal():
            for i in dialog.listbox.GetCheckedItems():
                field = exportable_fields[i]
                value = data['data'][names[i]]
                if isinstance(value, str):
                    value = base64.b64decode(value.encode())
                field.__set__(instance, value)
            print('导入成功')

    def dump_model_fields(self, instance, names=None):
        """导出模型字段数据"""
        model = type(instance)
        if names is None:
            names = model.exportable_fields
        exportable_fields = [model.field(name) for name in names]
        choices = [field.label or names[i] for i, field in enumerate(exportable_fields)]
        dialog = ui.dialog.ListDialog("选择导出的字段", listbox={'choices': choices})
        if dialog.ShowModal():
            data = {'model': model.__name__, 'data': {}}
            for i in dialog.listbox.GetCheckedItems():
                field = exportable_fields[i]
                value = field.__get__(instance)
                if not isinstance(value, (int, float)):
                    # 尝试按bytes处理
                    if not hasattr(value, 'to_bytes'):
                        raise ValueError('%s不支持序列化(to_bytes)' % choices[i])
                    value = base64.b64encode(value.to_bytes()).decode()
                data['data'][names[i]] = value
            fefactory.json_dump_file(self, data)


class ProxyHackTool(BaseHackTool):
    """ 使用代理Handler
    abs field: handler_class: iterable
    """
    def __init__(self):
        super().__init__()
        self.handler = ProxyHandler()

    def check_attach(self, _=None):
        if self.handler.active:
            self.ondetach()

        for Handler in self.handler_class:
            handler = Handler()
            if handler.attach():
                self.handler.set(handler)
                self.attach_status_view.label = (getattr(handler, 'WINDOW_NAME', None) or handler.CLASS_NAME) + ' 正在运行'
                if not self.win.hotkey_map:
                    hotkeys = self.get_hotkeys()
                    if hotkeys:
                        self.win.register_hotkeys(hotkeys)
                self.onattach()
                return True
        else:
            self.attach_status_view.label = '绑定失败, 未找到支持的进程'
            return False
