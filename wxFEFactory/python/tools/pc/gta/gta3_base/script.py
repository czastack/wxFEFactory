from lib.hack import models, utils
from ..gta_base.models import ManagedModel
import struct


class ArgType:
    END = 0
    INT32 = 1
    GLOBAL_I = 2
    LOCAL_I = 3
    INT8 = 4
    INT16 = 5
    FLOAT = 6
    STRING = 10  # 自己定义的

    ARG_TYPE = {
        0x63: INT8,      # c
        0x62: INT8,      # b
        0x68: INT16,     # h
        0x48: INT16,     # H
        0x69: INT32,     # i
        0x49: INT32,     # I
        0x6c: INT32,     # l
        0x4c: INT32,     # L
        0x66: FLOAT,     # f
        0x64: FLOAT,     # d
        0x50: LOCAL_I,   # P
        # 0x50: GLOBAL_I,  # P

        0x70: STRING,  # p
        0x73: STRING,  # s
    }

    get = ARG_TYPE.get


class BaseRunningScript(ManagedModel):
    m_szName = models.StringField(0x08, 8)

    def __init__(self, addr, context, script_space_base, init_addr, process_addr, buff_size=255):
        """
        :param process_addr: 执行一条脚本的原生函数地址
        """
        super().__init__(addr, context)
        self.script_space_base = script_space_base
        self.process_addr = process_addr
        self.buff_size = buff_size
        self.buff = bytearray()
        self.variables = []

        self.m_szName = 'an-scr'
        self.buff_addr = self.handler.alloc_memory(buff_size)
        self.init_addr = init_addr
        self.context.native_call_auto(self.init_addr, None, this=self.addr)

    def __del__(self):
        self.handler.free_memory(self.buff_addr)

    def push(self, signature, *args):
        """压入参数"""
        arg_it = iter(args)

        for fmt in utils.iter_signature(signature):
            try:
                arg_type = self.get_arg_type(ch)
            except IndexError:
                raise ValueError('unsupported format: ' + fmt)
            arg = next(arg_it)
            self.buff.append(arg_type)

            if arg_type is ArgType.LOCAL_I:
                # 指针参数
                var_index = len(self.variables)
                self.buff.append(var_index & 0xFF)
                self.buff.append((var_index >> 8) & 0xFF)
                self.variables.append(arg)
            elif arg_type is ArgType.GLOBAL_I:
                # 指针参数
                var_offset = len(self.variables) << 2
                self.buff.append(var_offset & 0xFF)
                self.buff.append((var_offset >> 8) & 0xFF)
                # 把script_space_base对应位置内存设为当前指针中的值
                # self.handler.write32(self.script_space_base + var_offset, self.handler.read32(arg))
                self.variables.append(arg)
            elif arg_type is ArgType.STRING:
                # 字符串参数
                self.push_string(arg)
            else:
                # 普通参数
                self.push_common_arg(arg_type, fmt, arg)

    def push_end(self):
        """写入结束符"""
        self.buff.append(ArgType.END)

    def push_common_arg(self, arg_type, fmt, arg):
        """ 压入通用参数
        :return: bytes object
        """
        self.buff.extend(struct.pack(fmt, arg))

    def push_string(self, arg):
        self.buff.pop()
        if isinstance(arg, str):
            arg = bytes(arg, 'gbk')
        self.buff.extend(arg[:7] + b'\x00')

    def get_arg_type(self, fmt_code):
        return ArgType.get(fmt_code)

    def save_variables(self):
        var_type = ArgType.get(0x50)
        if var_type is ArgType.LOCAL_I:
            for ptr, value in zip(self.variables, self.m_aLVars):
                self.handler.write32(ptr, value)
        elif var_type is ArgType.GLOBAL_I:
            var_addr = self.script_space_base
            for i in range(len(self.variables)):
                self.handler.write32(self.variables[i], self.handler.read32(var_addr))
                var_addr += 4

    def reset(self):
        self.buff.clear()
        self.variables.clear()

    def __enter__(self):
        self.reset()
        return self

    def __exit__(self, *args):
        pass


class RunningScript(BaseRunningScript):
    """原生脚本调用环境"""
    SIZE = 0x88

    m_nIp = models.Field(0x10)
    scriptType = models.Field(0x2e)
    m_aLVars = models.ArrayField(0x30, 16, models.Field(0))
    m_nCondResult = models.ByteField(0x79)
    m_bIsMission = models.ByteField(0x7a)
    m_bNotFlag = models.ByteField(0x82)
    m_bDeathArrestCheckEnabled = models.ByteField(0x83)
    m_bMissionCleanup = models.ByteField(0x85)

    def run(self, command_id, signature, *args):
        self.m_bDeathArrestCheckEnabled = True
        self.m_bIsMission = self.m_bMissionCleanup = False
        self.scriptType = self.m_bMissionCleanup = False
        self.m_bNotFlag = (command_id >> 15) & 1
        # self.m_nCondResult = 0

        self.reset()
        # 写入command_id
        self.buff.append(command_id & 0xFF)
        self.buff.append((command_id >> 8) & 0xFF)
        # 写入参数
        if signature:
            self.push(signature, *args)
        self.push_end()
        self.handler.write(self.buff_addr, self.buff)

        ip = self.buff_addr - self.script_space_base
        if ip < 0:
            raise ValueError('申请的内存不太对，重新按下检测按钮吧')

        self.m_nIp = self.buff_addr - self.script_space_base

        self.context.native_call_auto(self.process_addr, None, this=self.addr)
        self.save_variables()
        return self.m_nCondResult
