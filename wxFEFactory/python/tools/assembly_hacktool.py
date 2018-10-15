from functools import partial
from lib.extypes import DataClass
from lib.hack import utils
from fefactory_api import ui
from .hacktool import BaseHackTool
from .assembly_code import AssemblyGroup


class AssemblyHacktool(BaseHackTool):
    """现在支持x86 jmp"""
    allocated_memory = None

    def __init__(self):
        super().__init__()
        self.variable_model = VariableModel(self.weak)

    def reset(self):
        self.allocated_memory = None
        self.next_usable_memory = None
        self.registed_assembly = None
        self.registed_variable = None

    def onattach(self):
        super().onattach()
        self.reset()
        self.is32process = self.handler.is32process

    def ondetach(self):
        super().ondetach()
        if self.allocated_memory is not None:
            self.handler.free_memory(self.allocated_memory)
            for key, value in self.registed_assembly.items():
                if value['active']:
                    self.unregister_assembly_item(value)
            self.reset()

    def render_assembly_functions(self, functions, cols=4, vgap=10):
        with ui.GridLayout(cols=cols, vgap=vgap, className="expand"):
            self.assembly_buttons = {
                item.key: ui.ToggleButton(label=item.label,
                    onchange=partial(__class__.toggle_assembly_function, self.weak, item=item)) for item in functions
            }

    def toggle_assembly_function(self, btn, item):
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
            self.set_variable_value(item.key, int(checked))

    def toggle_assembly_button(self, key):
        self.assembly_buttons[key].toggle()

    def insure_memory(self):
        if self.allocated_memory is None:
            # 初始化代码区 PAGE_EXECUTE_READWRITE
            self.next_usable_memory = self.allocated_memory = self.handler.alloc_memory(2048, protect=0x40)
            self.registed_assembly = {}
            self.registed_variable = {}

    def register_assembly(self, item):
        """注册机器码修改
        :param item: AssemblyItem
        """
        if not self.handler.active:
            return

        self.insure_memory()

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

            addr = self.find_address(original, item.find_start, item.find_end, item.find_range_from_base, item.fuzzy)
            if addr is -1:
                return

            memory = self.next_usable_memory
            original_len = len(original)
            read_original = False  # 是否需要通过handler读取最新的original
            if replace_offset:
                if replace_len is 0:
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
                # 使用参数(暂时支持4字节)
                if item.args:
                    memory_conflict = memory == self.next_usable_memory
                    if isinstance(assembly, AssemblyGroup):
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
                if isinstance(assembly, AssemblyGroup):
                    assembly = assembly.generate(self, memory)

                jmp_offset = memory - (addr + 5)
                if abs(jmp_offset) < 0x7FFFFFFF or self.is32process:
                    # E9 relative address
                    # 计算jump地址, 5是jmp opcode的长度
                    jmp_len = 5
                    diff_new = utils.u32(jmp_offset)
                    diff_back = utils.u32(addr + original_len - (memory + len(assembly) + 5))
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

                    assembly = assembly + b'\xFF\x25\x00\x00\x00\x00' + (addr + original_len).to_bytes(8, 'little')

                if available_len < jmp_len:
                    raise ValueError("可用长度不足以插入jmp代码")
                elif available_len != jmp_len:
                    # 填充的NOP
                    replace += b'\x90' * (available_len - jmp_len)

                if memory == self.next_usable_memory:
                    self.next_usable_memory += utils.align4(len(assembly))
                self.handler.write(memory, assembly)

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

    def find_address(self, original, find_start, find_end, find_range_from_base=True, fuzzy=False):
        base_addr = self.handler.base_addr
        if find_start and find_range_from_base:
            find_start += base_addr
        if find_end and find_range_from_base:
            find_end += base_addr
        return self.handler.find_bytes(original, find_start, find_end, fuzzy=fuzzy)

    def register_variable(self, variable, value=0):
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
            align = variable.align or variable.size
            variable.addr = utils.align_size(self.next_usable_memory, align)
            self.registed_variable[variable.name] = variable
            self.next_usable_memory += utils.align_size(variable.size, align)
        else:
            variable = temp
        if value is not 0:
            self.handler.write(variable.addr, value, size)
        return variable

    def get_variable(self, name):
        """获取变量地址"""
        if self.allocated_memory:
            return self.registed_variable.get(name, None)

    def get_variable_value(self, name):
        """变量值读取"""
        variable = self.get_variable(name)
        if variable:
            return self.handler.read(variable.addr, variable.type, variable.size)

    def set_variable_value(self, name, value):
        """变量值写入"""
        variable = self.get_variable(name)
        if variable:
            self.handler.write(variable.addr, variable.type(value), variable.size)


class VariableModel:
    """主要用于ModelWidget绑定变量"""
    def __init__(self, owner):
        object.__setattr__(self, 'owner', owner)

    def __getattr__(self, name):
        return self.owner.get_variable_value(name)

    def __setattr__(self, name, value):
        return self.owner.set_variable_value(name, value)


class AssemblyItems:
    def __init__(self, label, *children):
        self.label = label
        self.children = children

    @property
    def key(self):
        return self.children[0].key


""" register_assembly 的参数类型
    :param original: 原始数据
    :param find_start: 原始数据查找起始
    :param find_end: 原始数据查找结束
    :param replace: 原始数据替换为的内容
    :param assembly: 写到新内存的内容
    :param find_range_from_base: 是否将find_start和find_end加上模块起始地址
    :param inserted: 是否自动加入jmp代码
    :param replace_len: 只记录original前n个字节
"""
AssemblyItem = DataClass(
    'AssemblyItem',
    ('key', 'label', 'original', 'find_start', 'find_end', 'replace', 'assembly',
        'find_range_from_base', 'inserted', 'fuzzy', 'replace_len', 'replace_offset', 'args'),
    defaults={
        'assembly': None,
        'find_range_from_base': True,
        'inserted': False,
        'fuzzy': False,
        'replace_len': 0,
        'replace_offset': 0,
        'args': ()
    }
)


AssemblySwitch = DataClass('AssemblySwitch', ('key', 'label'))

VariableType = DataClass('VariableType', ('name', 'size', 'type', 'value', 'align', 'addr'),
    defaults={'size': 4, 'type': int, 'value': 0})
