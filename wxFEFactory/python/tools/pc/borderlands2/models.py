from lib.hack.models import Model, Field, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField


class WeaponManager(Model):
    ammo = FloatField(0x6C, label='弹药')


class Manager(Model):
    weapon_mgrs = ArrayField((0x2C, 0x188), 7, ModelPtrField(0, WeaponManager), cachable=True)


class Global(Model):
    mgr = ModelPtrField(0x01EEE798, Manager)
