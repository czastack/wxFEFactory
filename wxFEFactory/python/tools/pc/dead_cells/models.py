from lib.hack.models import (
    Model, Field, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class Global(Model):
    hpmax = Field(0xEC, label='HP上限')
    attr_red = ByteField(0x114, label='暴虐')
    attr_blue = ByteField(0x110, label='战术')
    attr_green = ByteField(0x118, label='生存')
