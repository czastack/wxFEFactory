from lib.hack.models import (
    Model, Field, Fields, ByteField, WordField, QWordField, FloatField, ArrayField, ModelField, ModelPtrField,
    CoordField, BytesField, ToggleField, UnicodeField, PropertyField
)


class Character(Model):
    """角色"""
    health_max = FloatField(0x20, label="最大HP")
    health = FloatField(0x24, label="HP")



class PositionStruct(Model):
    """位置数据"""
    coord = CoordField((0x18, 0x30), label="坐标")


class Coord(Model):
    coord = CoordField(0, label="角色坐标")


class BagItem(Model):
    """背包物品"""
    quantity = Field((0x28, 0x88), label="数量")

    class ItemData(Model):
        name = UnicodeField(0x24, size=64)
        ptr1 = QWordField(0)
        ptr2 = QWordField(0x18)

    data = ModelPtrField((0x28, 0x80), ItemData)

    @PropertyField(label='物品名称')
    def name(self):
        return self.data.name

    @name.setter
    def name(self, name):
        data = self.data
        # 直接替换物品指针
        find_data = b''.join([
            data.ptr1.to_bytes(8, 'little'), b'*' * 8, b'\x00' * 8, data.ptr2.to_bytes(8, 'little'),
            len(name).to_bytes(4, 'little'), name.encode('utf-16-le')
        ])
        addr = self.handler.find_bytes(find_data, data.addr - 0x2000000, data.addr + 0x2000000, fuzzy=True)
        if addr != -1:
            self.data = addr
        else:
            print('无法替换class ptr')


class BoxItem(Model):
    """物品箱物品"""
    name = UnicodeField((0x20, 0x24), size=64, label="物品名称")
    quantity = Field(0x28, label="数量")

    class ItemData(Model):
        name = UnicodeField(0x24, size=64)
        class_ptr1 = QWordField(0)
        class_ptr2 = QWordField(0x18)

    data = ModelPtrField(0x20, ItemData)

    data = BagItem.data


class Manager(Model):
    character = ModelPtrField((0x58, 0x28, 0x28, 0x70), Character)
    bag_count = Field((0x60, 0x28), label="背包物品数量")
    bag_items = ArrayField((0x60, 0x20, 0x30), 20, ModelPtrField(0, BagItem))
    box_items = ArrayField((0x58, 0x68, 0x60, 0x30), 20, ModelPtrField(0, BoxItem))


class Statistics(Model):
    """统计"""
    herb_count = Field(0x180, label="治疗物品使用数量")
    open_box_count = Field(0x1F0, label="已打开物品箱数量")


class Global(Model):
    manager = ModelPtrField(0x081E4148, Manager)
    statistics = ModelPtrField((0x081EA178, 0x88), Statistics)


class CodexGlobal(Model):
    manager = ModelPtrField(0, Manager)


SPECIFIC_GLOBALS = {
    'steam': Global,
    'codex': CodexGlobal,
}
