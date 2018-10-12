from lib.hack.models import Model, Field, ByteField, WordField, ArrayField, ModelField


class ItemSlot(Model):
    SIZE = 0x28
    item = Field(0)
    count = ByteField(4)


class SkillSlot(Model):
    SIZE = 8
    skill = Field(0)
    spec = WordField(4)  # 01 01 消耗潜力值习得状态, 0102 不消耗潜力值习得状态, 0103 锁定技能消耗潜力值习得状态, 0002 先天技能，不上锁，不占技能槽


class Person(Model):
    SIZE = 0x3F0
    prof = Field(0x00)  # 职业指针 step=11C
    camp = Field(0x04)  # 阵营？0x8064CDFC = 晓之团
    no = ByteField(0x0C)  # 角色编号
    belong = ByteField(0x0D)  # 所属
    level = ByteField(0x0E)
    exp = ByteField(0x0F)
    posx = ByteField(0x12)  # 横坐标(左上角开始)
    posy = ByteField(0x13)  # 纵坐标
    moved = ByteField(0x1F)  # 1表示已经移动，0表示可以行动
    hp = ByteField(0x24)  # 当前hp
    physical_add = ByteField(0x25)
    move_add = ByteField(0x26)
    hp_add = ByteField(0x29)  # hp增加值(最大hp=hp初始值+hp增加值)
    power_add = ByteField(0x2A)
    magic_add = ByteField(0x2B)
    skill_add = ByteField(0x2C)
    speed_add = ByteField(0x2D)
    lucky_add = ByteField(0x2E)
    defense_add = ByteField(0x2F)
    magicdef_add = ByteField(0x30)
    skills = ArrayField(0x3C, 12, ModelField(0, SkillSlot))
    items = ArrayField(0xCC, 7, ModelField(0, ItemSlot))
    # 24个字节 武器熟练度(剑、枪、斧、弓、短剑、打、炎、雷、风、光、暗、杖) A级[00B5] S级[00FB] SS级[014B]
    proficiency = ArrayField(0x01E4, 18, WordField(0))
    support = ArrayField(0x210, 72, ByteField(0))  # 支援等级 72个字节 C级=32, B级=64, A级=96
    biorhythm = WordField(0x288)  # 生理节律，01是当前状态大好，08是曲线类型

    def __setattr__(self, name, value):
        data = self.test_comlex_attr(name)
        if data:
            if data.attrs[0] == 'skills':
                skill = self.skills[data.attrs[1]]
                skill.skill = value
                skill.spec = 0x0002
                return
        super().__setattr__(name, value)


class Global(Model):
    # 角色指针起始
    # 4.0.2: 9: 0x00914EC0-0x3F0*9
    # 5.x 9: 0x00930C80-0x3F0*9
    persons = ArrayField(0x0092E910, 0xff, ModelField(0, Person))
    turn = WordField(0x003AE34A)  # 回合数
    money1 = Field(0x003AE350)
    money2 = Field(0x003AE354)
    money3 = Field(0x003AE358)
    exp1 = Field(0x003AE35C, type=float)
    exp2 = Field(0x003AE360, type=float)
    exp3 = Field(0x003AE364, type=float)
    pedid = ByteField(0x003AC8FC)  # 当前人物编号
    curx = ByteField(0x003C88B1)  # 当前光标x坐标
    cury = ByteField(0x003C88B3)  # 当前光标y坐标
