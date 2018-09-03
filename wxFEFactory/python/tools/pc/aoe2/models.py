from lib.hack.models import (
    Model, Field, FloatField, ByteField, WordField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class ResourceManager(Model):
    SIZE = 12
    food = FloatField(0, label='食物')
    wood = FloatField(4, label='木材')
    rock = FloatField(8, label='石材')
    gold = FloatField(12, label='黄金')


class PopulationManager(Model):
    SIZE = 0
    current = FloatField(0x2C, label='当前')
    total = FloatField(0x10, label='剩余')


class Global(Model):
    resources = ModelPtrField((0x00295794, 0xFC, 0xA8), ResourceManager)
    population_mgr = ModelPtrField((0x003912A0, 0x424, 0x4C, 0x4, 0xA8), PopulationManager)
