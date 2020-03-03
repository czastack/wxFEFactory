import types
from functools import partial
from typing import Union, List
from lib.extypes import new_dataclass, DataClass
from lib.hack import utils
from lib import ui
from .hacktool import BaseHackTool
from .assembly_code import AssemblyNode


class AssemblyHacktool(BaseHackTool):
    """现在支持x86 jmp"""
    allocated_memory = None
    allocation_size = 2048
    allocation_type = 0x00003000
    assembly_address_sources = None

    def __init__(self):
        super().__init__()
        self.variable_model = VariableModel(self.weak)
        self.is32process = False
        self.assembly_buttons = {}
        self.reset()

    def reset(self):
        """重置状态"""
        self.allocated_memory = None
        self.next_usable_memory = None
        self.registed_assembly = None
        self.registed_variable = None
        self.assembly_address_dict = None

    def onattach(self):
        super().onattach()
        self.reset()
        self.is32process = self.handler.is32process

        for key, button in self.assembly_buttons.items():
            if button.checked:
                self.toggle_assembly_button(key, True)

    def ondetach(self):
        super().ondetach()
        if self.allocated_memory is not None:
            self.handler.free_memory(self.allocated_memory)
            for _, value in self.registed_assembly.items():
                if value['active']:
                    self.unregister_assembly_item(value)
            self.reset()

    def render_assembly_buttons(self, functions, cols=4, vgap=10):
        with ui.GridLayout(cols=cols, vgap=vgap, class_="expand"):
            for item in functions:
                button = ui.ToggleButton(label=item.label,
                    onchange=partial(self.__class__.toggle_assembly_function, self.weak, item=item))
                if item.help:
                    button.SetToolTip(item.help)
                self.assembly_buttons[item.key] = button

    def toggle_assembly_function(self, btn, item):
        """切换单个汇编功能"""
        checked = btn.checked
        if isinstance(item, AssemblyItem):
            if checked:
                self.register_assembly(item)
            else:
                self.unregister_assembly(item.key)
        elif isinstance(item, AssemblyItems):
            for item in item.children:
                if checked:
                    self.register_assembly(item)
                else:
                    self.unregister_assembly(item.key)
        elif isinstance(item, AssemblySwitch):
            if checked and item.depends:
                for key in item.depends:
                    self.toggle_assembly_button(key, True)
            self.set_variable_value(item.key, int(checked))
        elif isinstance(item, SimpleButton):
            item.onclick(checked)

    def toggle_assembly_button(self, key, checked=None):
        self.assembly_buttons[key].toggle(checked, False)

    def insure_memory(self):
        """确保分配内存"""
        if not self.allocated_memory:
            # 初始化代码区 PAGE_EXECUTE_READWRITE
            if not self.handler.is32process:
                start = self.handler.base_addr - 0x10000000
                self.alloc_memory(start)
                if self.allocated_memory == 0:
                    self.alloc_memory(start - 0x10000000)
            if not self.allocated_memory:
                self.alloc_memory()
            if self.allocated_memory == 0:
                raise ValueError('分配内存失败')
            self.next_usable_memory = self.allocated_memory
            self.registed_assembly = {}
            self.registed_variable = {}

    def alloc_memory(self, start=0):
        """分配内存"""
        self.allocated_memory = self.handler.alloc_memory(
            self.allocation_size, start=start, allocation_type=self.allocation_type, protect=0x40)

    def register_assembly(self, item):
        """注册机器码修改
        :param item: AssemblyItem
        """
        if not self.handler.active:
            return

        self.insure_memory()

        if item.depends:
            for key in item.depends:
                self.toggle_assembly_button(key, True)

        if item.key in self.registed_assembly:
            data = self.registed_assembly[item.key]
            addr = data['addr']
            replace = data['replace']
            data['active'] = True
        else:
            original = item.original
            replace = item.replace
            assembly = item.assembly
            replace_len = item.replace_len
            replace_offset = item.replace_offset
            find_start = item.find_start
            find_end = item.find_end

            # 动态判断地址起始数据源
            if find_start is None:
                if not self.assembly_address_dict and self.assembly_address_sources:
                    for _, address_dict in self.assembly_address_sources.items():
                        temp = address_dict[item.key]
                        if isinstance(temp, (list, tuple)):
                            find_start, find_end = temp
                        else:
                            find_start = temp
                        if self.find_address(original, find_start, find_end, item.find_base, item.ordinal, item.fuzzy):
                            self.assembly_address_dict = address_dict
                            break
                if self.assembly_address_dict:
                    temp = self.assembly_address_dict[item.key]
                    if isinstance(temp, (list, tuple)):
                        find_start, find_end = temp
                    else:
                        find_start = temp
                else:
                    raise ValueError('no find_start')

            addr = self.find_address(original, find_start, find_end, item.find_base, item.ordinal, item.fuzzy)
            if addr == -1:
                print('找不到地址: ', item.key)
                return

            memory = self.next_usable_memory
            original_len = len(original)
            read_original = False  # 是否需要通过handler读取最新的original
            if replace_offset:
                if replace_len == 0:
                    if 0 < replace_offset < original_len:
                        replace_len = original_len - replace_offset
                    else:
                        raise ValueError('此情况下replace_offset依赖于replace_len参数')
                if replace_offset > 0 and replace_len <= original_len - replace_offset and not item.fuzzy:
                    original = original[replace_offset: replace_len + replace_offset]
                else:
                    read_original = True
                addr += replace_offset
                original_len = replace_len
            else:
                if replace_len:
                    original_len = replace_len
                if item.fuzzy:
                    read_original = True
                elif replace_len:
                    original = original[:original_len]

            if read_original:
                original = self.handler.read(addr, bytes, original_len)

            if item.inserted:
                available_len = original_len - len(replace)  # 可用于跳转到插入的代码的jmp指令的长度
                jump_back = addr + original_len  # 跳转回(下一个指令)的地址

                # 使用参数(暂时支持32位地址)
                if item.args:
                    memory_conflict = memory == self.next_usable_memory
                    if isinstance(assembly, AssemblyNode):
                        for arg in item.args:
                            self.register_variable(arg)
                    else:
                        if self.next_usable_memory > 0xFFFFFFFF:
                            raise ValueError('目前只支持32位参数地址')
                        assembly = assembly % tuple(self.register_variable(arg).addr.to_bytes(4, 'little')
                            for arg in item.args)
                    if memory_conflict:
                        memory = self.next_usable_memory

                # 动态生成机器码
                # 因为根据情况，addr可能会变
                def gen_assembly(assembly):
                    if isinstance(assembly, AssemblyNode):
                        return assembly.generate(self, types.SimpleNamespace(
                            item=item, original_addr=addr, original=original, addr=memory, jump_back=jump_back
                        ))
                    return assembly

                jmp_offset = memory - (addr + 5)
                if abs(jmp_offset) < 0x7FFFFFFF or self.is32process:
                    # E9 relative address
                    # 计算jump地址, 5是jmp opcode的长度
                    jmp_len = 5
                    assembly = gen_assembly(assembly)
                    diff_new = utils.u32(jmp_offset)
                    diff_back = utils.u32(jump_back - (memory + len(assembly) + 5))
                    replace += replace + b'\xE9' + diff_new.to_bytes(4, 'little')
                    assembly = assembly + b'\xE9' + diff_back.to_bytes(4, 'little')
                else:
                    if available_len >= 14:
                        jmp_len = 14
                        # FF25 00000000 absolute address
                        replace += replace + b'\xFF\x25\x00\x00\x00\x00' + memory.to_bytes(8, 'little')
                    elif available_len >= 7 and self.next_usable_memory < 0xFFFFFFFF:
                        # ptr jmp
                        jmp_len = 7
                        memory_conflict = memory == self.next_usable_memory
                        temp = self.register_variable(VariableType(item.key + '_jmp', size=8)).addr
                        if memory_conflict:
                            memory = self.next_usable_memory
                            self.handler.write_ptr(temp, memory)
                        replace += b'\xFF\x24\x25' + temp.to_bytes(4, 'little')
                    else:
                        raise ValueError('不支持当前情况jmp')

                    assembly = gen_assembly(assembly)
                    assembly = assembly + b'\xFF\x25\x00\x00\x00\x00' + jump_back.to_bytes(8, 'little')

                if available_len < jmp_len:
                    raise ValueError("可用长度不足以插入jmp代码")
                elif available_len != jmp_len:
                    # 填充的NOP
                    replace += b'\x90' * (available_len - jmp_len)

                if memory == self.next_usable_memory:
                    self.next_usable_memory += utils.align_4(len(assembly))
                self.handler.write(memory, assembly)
            else:
                # 仅替换
                if replace_len > len(replace):
                    replace += b'\x90' * (replace_len - len(replace))

            data = self.registed_assembly[item.key] = {'active': True, 'addr': addr, 'original': original,
                'replace': replace, 'memory': memory}

        self.handler.write(addr, replace)

    def unregister_assembly(self, key):
        """恢复机器码修改"""
        items = getattr(self, 'registed_assembly', None)
        if items:
            item = items.get(key, None)
            if item is not None:
                self.unregister_assembly_item(item)

    def unregister_assembly_item(self, item):
        self.handler.write(item['addr'], item['original'])
        item['active'] = False

    def find_address(self, original, find_start, find_end, find_base=True, ordinal=1, fuzzy=False):
        base_addr = find_base is True and self.handler.base_addr or callable(find_base) and find_base() or find_base
        if callable(find_start):
            find_start = find_start()
        if callable(find_end):
            find_end = find_end()
        elif isinstance(find_end, Delta):
            find_end = find_start + find_end
        if base_addr:
            find_start += base_addr
            find_end += base_addr
        return self.handler.find_bytes(original, find_start, find_end, ordinal, fuzzy)

    def register_variable(self, variable):
        """注册变量"""
        self.insure_memory()
        if isinstance(variable, str):
            variable = VariableType(variable)
        elif isinstance(variable, tuple):
            variable = VariableType(*variable)
        temp = self.registed_variable.get(variable.name, None)
        if temp is None:
            if variable.addr:
                variable = variable.clone()
            align = variable.align
            variable.addr = utils.align_size(self.next_usable_memory, align)
            self.registed_variable[variable.name] = variable
            self.next_usable_memory = variable.addr + utils.align_size(variable.size, align)
        else:
            variable = temp
        if variable.value != 0:
            self.handler.write(variable.addr, variable.value, variable.size)
        return variable

    def get_variable(self, name):
        """获取变量对象"""
        if self.allocated_memory:
            return self.registed_variable.get(name, None)

    def get_variable_value(self, name, default=None):
        """变量值读取"""
        variable = self.get_variable(name)
        if variable:
            return self.handler.read(variable.addr, variable.type, variable.size)
        return default

    def set_variable_value(self, name, value):
        """变量值写入"""
        variable = self.get_variable(name)
        if variable:
            self.handler.write(variable.addr, variable.type(value), variable.size)

    def variable_getter(self, name):
        weak = self.weak
        return lambda: weak.get_variable_value(name)

    def assambly_patcher(self, *args, **kwargs):
        """汇编码补丁"""
        return AssamblyPatcher(self.weak, *args, **kwargs)


class VariableModel:
    """主要用于ModelWidget绑定变量"""
    def __init__(self, owner):
        object.__setattr__(self, 'owner', owner)

    def __getattr__(self, name):
        return self.owner.get_variable_value(name)

    def __setattr__(self, name, value):
        return self.owner.set_variable_value(name, value)

    def __and__(self, field):
        variable = self.owner.get_variable(field)
        return variable and variable.addr or 0


class AssamblyPatcher:
    """汇编码补丁"""
    def __init__(self, owner, name, offset, size=4, type=int, is_memory=False):
        self.owner = owner
        self.name = name
        self.offset = offset
        self.size = size
        self.type = type
        self.is_memory = is_memory

    def get_addr(self):
        items = getattr(self.owner, 'registed_assembly', None)
        if items:
            item = items.get(self.name, None)
            if item is not None:
                return item['memory' if self.is_memory else 'addr'] + self.offset

    def read(self):
        addr = self.get_addr()
        if addr:
            return self.owner.handler.read(addr, self.type, self.size)

    def write(self, value):
        addr = self.get_addr()
        if addr:
            self.owner.handler.write(addr, self.type(value), self.size)

    def __iter__(self):
        yield self.read
        yield self.write


class AssemblyItems:
    def __init__(self, label, *children, help=None):
        self.label = label
        self.children = children
        self.help = help

    @property
    def key(self):
        return self.children[0].key


class Delta(int):
    """差值"""


class AssemblyButton(DataClass):
    """汇编功能按钮"""
    fields = ('key', 'label')


class AssemblyItem(AssemblyButton):
    """ register_assembly 的参数类型
        :param original: 原始数据
        :param find_start: 原始数据查找起始
        :param find_end: 原始数据查找结束
        :param replace: 原始数据替换为的内容
        :param assembly: 写到新内存的内容
        :param find_base: 是否将find_start和find_end加上模块起始地址
        :param inserted: 是否自动加入jmp代码
        :param replace_len: 只记录original前n个字节
        :param replace_offset: 替换其实位置偏移(可以为负数)
        :param ordinal: 出现的序号(相同原始数据查出的第n个)
        :param fuzzy: 模糊查找，?表示任意字节
        :param args: 变量列表
        :param help: 帮助文本，显示在按钮hover时
        :param depends: 依赖
        :param ext: 其他数据
    """
    fields = ('original', 'find_start', 'find_end', 'replace', 'assembly', 'find_base',
        'ordinal', 'fuzzy', 'inserted', 'replace_len', 'replace_offset', 'args', 'help', 'depends', 'ext')
    defaults = {
        'assembly': None,
        'find_base': True,
        'ordinal': 1,
        'fuzzy': False,
        'inserted': False,
        'hidden': False,
        'replace_len': 0,
        'replace_offset': 0,
        'args': ()
    }

    original: Union[str, bytes]
    depends: Union[str, List[str]]

    def oninit(self):
        # 字符串转bytes
        if isinstance(self.original, str):
            if '*' in self.original:
                self.original = self.original.replace('*', '2A')
                self.fuzzy = True
        for name in ('original', 'replace', 'assembly'):
            value = self[name]
            if isinstance(value, str):
                self[name] = bytes.fromhex(value)
        if isinstance(self.depends, str):
            self.depends = self.depends.split()


class AssemblySwitch(AssemblyButton):
    """变量开关"""
    fields = ('help', 'depends')

    depends: Union[str, List[str]]

    def oninit(self):
        if isinstance(self.depends, str):
            self.depends = self.depends.split()


class SimpleButton(AssemblyButton):
    """简易按钮"""
    fields = ('help', 'onclick')


class VariableType(DataClass):
    """变量类型"""
    fields = ('name', 'size', 'type', 'value', 'align', 'addr')
    defaults = {'size': 4, 'type': int, 'value': 0, 'align': 4}
