from lib.hack import model
from ..gta3_base.script import ArgType, RunningScript
import struct


class RunningScript(RunningScript):
    """原生脚本调用环境"""
    SIZE = 0x88

    m_nCondResult = model.Field(0x78, size=1)
    m_bIsMission = model.Field(0x79, size=1)

    def push_common_arg(self, arg_type, fmt, arg):
        """ 压入通用参数
        :return: bytes object
        """
        if arg_type is ArgType.FLOAT:
            fmt = 'h'
            arg = int(arg * 16)

        self.buff.extend(struct.pack(fmt, arg))