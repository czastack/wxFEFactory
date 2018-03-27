from lib.hack.model import Model, Field, ByteField, ShortField


class ItemSlot(Model):
    SIZE = 0x2
    item = ByteField(0)
    count = ByteField(1)
    value = ShortField(0)


class BaseGlobal(Model):
    random = Field(0x03000000, size=8) # 乱数
    train_items_page = 1
    page_lenth = 10

    @property
    def train_items_offset(self):
        return (self.train_items_page - 1) * self.page_lenth