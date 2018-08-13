from functools import partial
from lib.hack.utils import align4
from lib.utils import u32
from fefactory_api import ui
from .hacktool import BaseHackTool


class AssemblyHacktool(BaseHackTool):
    """现在支持x86 jmp"""
    def ondetach(self):
        super().ondetach()
        memory = getattr(self, 'allocated_memory', None)
        if memory is not None:
            self.handler.free_memory(memory)
            self.allocated_memory = None
            self.next_usable_memory = None
            for key, value in self.registed_assembly.items():
                if value['active']:
                    self.unregister_assembly_item(value)
            self.registed_assembly = None

    def render_assembly_functions(self, functions, cols=4, vgap=10):
        with ui.GridLayout(cols=cols, vgap=vgap, className="expand"):
            for label, args in functions:
                ui.ToggleButton(label=label, onchange=partial(__class__.toggle_assembly_function, self.weak, args=args))

    def toggle_assembly_function(self, btn, args):
        if btn.checked:
            self.register_assembly(*args)
        else:
            self.unregister_assembly(args[0])

    def register_assembly(self, key, original, find_start, find_end, raplace, assembly=None,
            find_range_from_base=True, is_inserted=False, only_replace_jump=False):
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

        if getattr(self, 'allocated_memory', None) is None:
            # 初始化
            self.next_usable_memory = self.allocated_memory = self.handler.alloc_memory(2048)
            self.registed_assembly = {}
            self.registed_assembly_memory = {}

        if key in self.registed_assembly:
            data = self.registed_assembly[key]
            addr = data['addr']
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
            # 计算jump地址, 5是jmp opcode的长度
            diff_new = u32(memory - (addr + 5))
            diff_back = u32(addr + len(original) - (memory + len(assembly) + 5))
            # 填充的NOP
            replace_padding = b'\x90' * (len(original) - len(raplace) - 5)
            raplace = raplace + b'\xe9' + diff_new.to_bytes(4, 'little') + replace_padding
            assembly = assembly + b'\xe9' + diff_back.to_bytes(4, 'little')

            if memory == self.next_usable_memory:
                self.next_usable_memory += align4(len(assembly))

            self.handler.write(memory, assembly)

        # from lib.gba.utils import bytes_beautify
        # print(bytes_beautify(assembly))
        # print(bytes_beautify(raplace))
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
