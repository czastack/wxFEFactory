from lib.hack.model import Model, Field, ByteField, ShortField


class ItemSlot(Model):
    SIZE = 0x2
    item = ByteField(0)
    count = ByteField(1)
    value = ShortField(0)


class BasePerson(Model):
    def __getattr__(self, name):
        if name.startswith('proficiency.'):
            index = int(name[12:])
            return self.proficiency[index]
        elif name.startswith('items.'):
            index = int(name[6:])
            return self.items[index].item
        elif name.startswith('items_count.'):
            index = int(name[12:])
            return self.items[index].count

    def __setattr__(self, name, value):
        if name.startswith('proficiency.'):
            index = int(name[12:])
            self.proficiency[index] = value
        elif name.startswith('items.'):
            index = int(name[6:])
            self.items[index].item = value
        elif name.startswith('items_count.'):
            index = int(name[12:])
            self.items[index].count = value
        else:
            super().__setattr__(name, value)


class BaseGlobal(Model):
    random = Field(0x03000000, size=8) # 乱数

    def __getattr__(self, name):
        if name.startswith('train_items.'):
            index = int(name[12:])
            return self.train_items[index].item
        elif name.startswith('train_items_count.'):
            index = int(name[18:])
            return self.train_items[index].count

    def __setattr__(self, name, value):
        if name.startswith('train_items.'):
            index = int(name[12:])
            self.train_items[index].item = value
        elif name.startswith('train_items_count.'):
            index = int(name[18:])
            self.train_items[index].count = value
        else:
            super().__setattr__(name, value)