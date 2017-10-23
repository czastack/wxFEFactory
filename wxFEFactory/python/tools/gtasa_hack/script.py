from lib.hack import model
from ..gta3_base.script import ArgType, BaseRunningScript
import struct


class ArgType(ArgType):
    # Types below are only available in GTA SA
    INTRODUCED_IN_GTASA = 7

    # Number arrays
    GLOBAL_NUMBER_ARRAY = INTRODUCED_IN_GTASA
    LOCAL_NUMBER_ARRAY = 8
    STATIC_SHORT_STRING = 9
    GLOBAL_SHORT_STRING_VARIABLE = 10
    LOCAL_SHORT_STRING_VARIABLE = 11
    GLOBAL_SHORT_STRING_ARRAY = 12
    LOCAL_SHORT_STRING_ARRAY = 13
    STATIC_PASCAL_STRING = 14
    STATIC_LONG_STRING = 15
    GLOBAL_LONG_STRING_VARIABLE = 16
    LOCAL_LONG_STRING_VARIABLE = 17
    GLOBAL_LONG_STRING_ARRAY = 18
    LOCAL_LONG_STRING_ARRAY = 19


class RunningScript(BaseRunningScript):
    """原生脚本调用环境"""
    SIZE = 0xE0

    condResult = model.Field(0xc5)
    MissionCleanUpFlag = model.Field(0xc6, size=1)
    notFlag = model.Field(0xd2, size=1)
    missionFlag = model.Field(0xdc, size=1)
    IsCustom = model.Field(0xdf, size=1)
    baseIP = model.Field(0x10)
    curIP = model.Field(0x14)
    m_aLVars = model.ArrayField(0x3c, 32, model.Field(0))

    def __init__(self, addr, mgr, script_space_base, process_addr, init_addr, buff_size=255):
        """
        :param init_addr: 初始化的原生函数地址
        :param process_addr: 执行一条脚本的原生函数地址
        """
        super().__init__(addr, mgr, script_space_base, process_addr, buff_size)
        self.init_addr = init_addr
        self.mgr.native_call_auto(self.init_addr, None, this=self.addr)

    def run(self, command_id, signature, *args):
        self.IsCustom = self.missionFlag = self.MissionCleanUpFlag = False
        self.notFlag = (command_id >> 15) & 1

        self.reset()
        # 写入command_id
        self.buff.append(command_id & 0xFF)
        self.buff.append((command_id >> 8) & 0xFF)
        # 写入参数
        self.push(signature, *args)
        self.push_end()
        self.handler.write(self.buff_addr, self.buff)
        self.baseIP = self.curIP = self.buff_addr

        self.mgr.native_call_auto(self.process_addr, None, this=self.addr)
        self.save_variables()
        return self.condResult != 0
