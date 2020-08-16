from lib.hack.models import Model, Field, ByteField
from ..models import Character


class Global(Model):
    partner_count = Field(0x02018AB5)  # 我方人数
    enemy_count = Field(0x02018AB6)  # 敌方人数
