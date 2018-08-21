from functools import partial
from lib.hack import utils
from fefactory_api import ui
from .hacktool import BaseHackTool


class AssemblyHacktool(BaseHackTool):
    allocated_memory = None

    """现在支持x86 jmp"""
    def ondetach(self):
        super().ondetach()
        memory = self.allocated_memory
        if memory is not None:
            self.handler.free_memory(memory)
            self.allocated_memory = None
            self.next_usable_memory = None
            for key, value in self.registed_assembly.items():
                if value['active']:
                    self.unregister_assembly_item(value)
            self.registed_assembly = None
            self.registed_variable = None

    def render_assembly_functions(self, functions, cols=4, vgap=10):
        with ui.GridLayout(cols=cols, vgap=vgap, className="expand"):
            for label, args in functions:
                ui.ToggleButton(label=label, onchange=partial(__class__.toggle_assembly_function, self.weak, args=args))

    def toggle_assembly_function(self, btn, args):
        if btn.checked:
            self.register_assembly(*args)
        else:
            self.unregister_assembly(args[0])

    def insure_memory(self):
        if self.allocated_memory is None:
            # 初始化代码区 PAGE_EXECUTE_READWRITE
            self.next_usable_memory = self.allocated_memory = self.handler.alloc_memory(2048, 0x40)
            self.registed_assembly = {}
            self.registed_variable = {}

    def register_assembly(self, key, original, find_start, find_end, raplace, assembly=None,
            find_range_from_base=True, is_inserted=False, only_replace_jump=False, args=()):
        """注册机器码修改
        :param original: 原始数据
        :param find_start: 原始数据查找起始
        :param find_end: 原始数据查找结束
        :param raplace: 原始数据替换为的内容
        :param assembly: 写到新内存的内容
        :param find_range_from_base: 是否将find_start和find_end加上模块起始地址
        :param is_inserted: 是否自动加入jmp代码
        :param only_replace_jump: 只替换original前5个字节为jmp的内容
        """
        if not self.handler.active:
            return

        if is_inserted and (len(original) - len(raplace)) < 5:
            print("需要可用间隔大于5")
            return

        self.insure_memory()

        if key in self.registed_assembly:
            data = self.registed_assembly[key]
            addr = data['addr']
            original = data['original']
            memory = data['memory']
        else:
            addr = self.find_address(original, find_start, find_end, find_range_from_base)
            if addr is -1:
                return
            memory = self.next_usable_memory
            if only_replace_jump:
                original = original[:len(raplace) + 5]
            self.registed_assembly[key] = {'addr': addr, 'original': original, 'memory': memory, 'active': True}

        if is_inserted:
            # 使用参数(暂时支持4字节)
            if args:
                memory_conflict = memory == self.next_usable_memory
                assembly = assembly % tuple(self.register_variable(arg).to_bytes(4, 'little') for arg in args)
                if memory_conflict:
                    self.registed_assembly[key]['memory'] = memory = self.next_usable_memory

            # 计算jump地址, 5是jmp opcode的长度
            diff_new = utils.u32(memory - (addr + 5))
            diff_back = utils.u32(addr + len(original) - (memory + len(assembly) + 5))
            # 填充的NOP
            replace_padding = b'\x90' * (len(original) - len(raplace) - 5)
            raplace = raplace + b'\xe9' + diff_new.to_bytes(4, 'little') + replace_padding
            assembly = assembly + b'\xe9' + diff_back.to_bytes(4, 'little')

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
        memory = self.registed_variable.get(name, None)
        if memory is None:
            memory = self.registed_variable[name] = self.next_usable_memory
            self.next_usable_memory += utils.align4(size)
        return memory

    def get_variable(self, name):
        if self.allocated_memory:
            return self.registed_variable.get(name, None)
