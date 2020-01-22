import struct
from lib.hack import models
from ..gta3_base.script import ArgType as BaseArgType, BaseRunningScript


class ArgType(BaseArgType):
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

    condResult = models.Field(0xc5)
    MissionCleanUpFlag = models.ByteField(0xc6)
    notFlag = models.ByteField(0xd2)
    missionFlag = models.ByteField(0xdc)
    IsCustom = models.ByteField(0xdf)
    baseIP = models.Field(0x10)
    curIP = models.Field(0x14)
    m_aLVars = models.ArrayField(0x3c, 32, models.Field(0))

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

        self.context.native_call_auto(self.process_addr, None, this=self.addr)
        self.save_variables()
        return self.condResult
