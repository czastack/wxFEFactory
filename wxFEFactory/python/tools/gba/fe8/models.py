from lib.hack.model import Model, Field, ByteField, ShortField, ArrayField, ModelField


class ItemSlot(Model):
    SIZE = 0x2
    item = ByteField(0)
    count = ByteField(1)


class Person(Model):
    SIZE = 0x48
    # start: 0x202be48
    prof = Field(4)
    level = ByteField(8)
    exp = ByteField(9)
    moved = ByteField(12)
    no = ByteField(13)
    posx = ByteField(16)
    posy = ByteField(17)
    hpmax = ByteField(18)
    hp = ByteField(19)
    power = ByteField(20)
    skill = ByteField(21)
    speed = ByteField(22)
    defensive = ByteField(23)
    magicdef = ByteField(24)
    lucky = ByteField(25)
    physical_add = ByteField(26)
    together = ByteField(27) # 同行人物序号
    move_add = ByteField(29)
    items = ArrayField(30, 5, ModelField(0, ItemSlot))
    proficiency = ArrayField(40, 8, ByteField(0)) # 武器熟练度(剑、枪、斧、弓、杖、理、光、暗) (E级:01 D级:1F C级:47 B级:79 A级:B5 S级:FB)
    status = ByteField(48) # 状态种类
    status_turn = ByteField(49) # 状态持续回合数
    support = ArrayField(50, 10, ByteField(0)) # 支援等级

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


class Global(Model):
    money = Field(0x0202BCF4)
    turns = ShortField(0x0202AA58)
    chapter = ByteField(0x0202BCFA)
    extra_flag = ShortField(0x02024F72)
    person_addr = Field(0x02003c08)
    curx = ShortField(0x0202bcc0)
    cury = ShortField(0x0202bcc2)
    persons = ArrayField(0x202be48, 0xff, ModelField(0, Person))