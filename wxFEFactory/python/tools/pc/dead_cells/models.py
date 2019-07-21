from lib.hack.models import (
    Model, Field, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class Global(Model):
    hp = Field(0xDB, label='HP')
    hpmax = Field(0xEC, label='HP上限')
    red_tier = ByteField(0x114, label='暴虐')
    purple_tier = ByteField(0x110, label='战术')
    green_tier = ByteField(0x118, label='生存')
