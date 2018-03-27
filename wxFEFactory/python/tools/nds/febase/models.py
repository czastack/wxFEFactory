from lib.hack.model import Model, Field, ByteField, ShortField


class ItemSlot(Model):
    SIZE = 4
    item = ShortField(0)
    count = ByteField(2)
    status = ByteField(3) # 0x10=装备中
    value = Field(0)


class BaseGlobal(Model):
    train_items_page = 1
    page_lenth = 10

    @property
    def train_items_offset(self):
        return (self.train_items_page - 1) * self.page_lenth