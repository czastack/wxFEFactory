from lib.hack.models import Model, Field, ArrayField, ModelPtrField, CoordField, CoordData
from ..gta_base.native import NativeContext


class _Vector3(Model):
    value = CoordField(0)


class NativeContext(NativeContext):
    """GTAIV原生函数调用的环境"""
    SIZE = 160

    m_nDataCount = Field(0x0C)                                          # unsigned int m_nDataCount;     // 0C-10
    m_pOriginalData = ArrayField(0x10, 4, ModelPtrField(0, _Vector3))  # CVector3 * m_pOriginalData[4]; // 10-20
    m_TemporaryData = ArrayField(0x20, 4, CoordField(0, length=4))      # Vector4 m_TemporaryData[4];    // 20-60
    m_TempStack = ArrayField(0x60, 16, Field(0))                        # int m_TempStack[16];           // 60-A0

    def get_result(self, type, size=0):
        """获取调用结果"""
        if self.m_nDataCount:
            """推测是把local Vector变量写回传进的Vector指针参数"""
            for i in range(self.m_nDataCount):
                self.m_pOriginalData[i].value.set(self.m_TemporaryData[i])

            self.m_nDataCount = 0

        return self.handler.read(self.m_TempStack.addr, type, size)

    def reset(self):
        self.m_nArgCount = 0
        self.m_nDataCount = 0
