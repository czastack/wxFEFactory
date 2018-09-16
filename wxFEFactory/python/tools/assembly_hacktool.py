from functools import partial
from lib.extypes import DataClass
from lib.hack import utils
from fefactory_api import ui
from .hacktool import BaseHackTool
from .assembly_code import AssemblyCodes


class AssemblyHacktool(BaseHackTool):
    """现在支持x86 jmp"""
    allocated_memory = None

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
            for item in functions:
                ui.ToggleButton(label=item.label, onchange=partial(
                    __class__.toggle_assembly_function, self.weak, item=item))

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

    def insure_memory(self):
        if self.allocated_memory is None:
            # 初始化代码区 PAGE_EXECUTE_READWRITE
            self.next_usable_memory = self.allocated_memory = self.handler.alloc_memory(2048, 0x40)
            self.registed_assembly = {}
            self.registed_variable = {}

    def register_assembly(self, item):
        """注册机器码修改
        :param item: AssemblyItem
        """
        if not self.handler.active:
            return

        original = item.original
        raplace = item.raplace
        assembly = item.assembly

        self.insure_memory()

        if item.key in self.registed_assembly:
            data = self.registed_assembly[item.key]
            addr = data['addr']
            original = data['original']
            memory = data['memory']
            data['active'] = True
        else:
            addr = self.find_address(original, item.find_start, item.find_end, item.find_range_from_base)
            if addr is -1:
                return
            memory = self.next_usable_memory
            if item.replace_len:
                original = original[:item.replace_len]
            data = self.registed_assembly[item.key] = {'addr': addr, 'original': original,
                'memory': memory, 'active': True}

        if item.is_inserted:
            original_len = len(original)
            available_len = original_len - len(raplace)  # 可用于跳转到插入的代码的jmp指令的长度
            # 使用参数(暂时支持4字节)
            if item.args:
                memory_conflict = memory == self.next_usable_memory
                if isinstance(assembly, AssemblyCodes):
                    for arg in item.args:
                        self.register_variable(arg)
                else:
                    if self.next_usable_memory > 0xFFFFFFFF:
                        raise ValueError('目前只支持32位参数地址')
                    assembly = assembly % tuple(self.register_variable(arg).to_bytes(4, 'little') for arg in item.args)
                if memory_conflict:
                    memory = data['memory'] = self.next_usable_memory

            # 动态生成机器码
            if isinstance(assembly, AssemblyCodes):
                assembly = assembly.generate(self, memory)

            if self.is32process:
                # E9 relative address
                # 计算jump地址, 5是jmp opcode的长度
                jmp_len = 5
                diff_new = utils.u32(memory - (addr + 5))
                diff_back = utils.u32(addr + original_len - (memory + len(assembly) + 5))
                raplace += raplace + b'\xE9' + diff_new.to_bytes(4, 'little')
                assembly = assembly + b'\xE9' + diff_back.to_bytes(4, 'little')
            else:
                if available_len >= 14:
                    jmp_len = 14
                    # FF25 00000000 absolute address
                    raplace += raplace + b'\xFF\x25\x00\x00\x00\x00' + memory.to_bytes(8, 'little')
                elif available_len >= 7 and self.next_usable_memory < 0xFFFFFFFF:
                    # ptr jmp
                    jmp_len = 7
                    memory_conflict = memory == self.next_usable_memory
                    temp = self.register_variable(item.key + '_jmp', 8)
                    if memory_conflict:
                        memory = data['memory'] = self.next_usable_memory
                        self.handler.write_ptr(temp, memory)
                    raplace += b'\xFF\x24\x25' + temp.to_bytes(4, 'little')

                assembly = assembly + b'\xFF\x25\x00\x00\x00\x00' + (addr + original_len).to_bytes(8, 'little')

            if available_len < jmp_len:
                raise ValueError("可用长度不足以插入jmp代码")

            # 填充的NOP
            raplace += b'\x90' * (available_len - jmp_len)

            if memory == self.next_usable_memory:
                self.next_usable_memory += utils.align4(len(assembly))

            self.handler.write(memory, assembly)

        self.handler.write(addr, raplace)

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

    def find_address(self, original, find_start, find_end, find_range_from_base=True):
        base_addr = self.handler.base_addr
        if find_start and find_range_from_base:
            find_start += base_addr
        if find_end and find_range_from_base:
            find_end += base_addr
        return self.handler.find_bytes(original, find_start, find_end)

    def register_variable(self, name, size=4):
        """注册变量"""
        self.insure_memory()
        if isinstance(name, tuple):
            name, size = name
        memory = self.registed_variable.get(name, None)
        if memory is None:
            memory = self.registed_variable[name] = self.next_usable_memory
            self.next_usable_memory += utils.align4(size)
        return memory

    def get_variable(self, name):
        if self.allocated_memory:
            return self.registed_variable.get(name, None)

    def get_variable_value(self, name, value):
        addr = self.get_variable(name)
        if addr:
            return self.handler.read32(addr)

    def set_variable_value(self, name, value):
        addr = self.get_variable(name)
        if addr:
            self.handler.write32(addr, value)


class AssemblyItems:
    def __init__(self, label, *children):
        self.label = label
        self.children = children


""" register_assembly 的参数类型
    :param original: 原始数据
    :param find_start: 原始数据查找起始
    :param find_end: 原始数据查找结束
    :param raplace: 原始数据替换为的内容
    :param assembly: 写到新内存的内容
    :param find_range_from_base: 是否将find_start和find_end加上模块起始地址
    :param is_inserted: 是否自动加入jmp代码
    :param replace_len: 只记录original前n个字节
"""
AssemblyItem = DataClass(
    'AssemblyItem',
    ('key', 'label', 'original', 'find_start', 'find_end', 'raplace', 'assembly',
        'find_range_from_base', 'is_inserted', 'replace_len', 'args'),
    defaults={
        'assembly': None,
        'find_range_from_base': True,
        'is_inserted': False,
        'replace_len': 0,
        'args': ()
    }
)


AssemblySwitch = DataClass('AssemblySwitch', ('key', 'label'))
