from lib.hack.models import Model, Field, FloatField, ToggleField, ArrayField, ModelField, ModelPtrField, PropertyField


class Item(Model):
    SIZE = 0x10
    item = Field(0, label='种类')
    count = Field(4, label='数量')


class Character(Model):
    """角色"""
    SIZE = 0xC8
    basedata = Field(0, label='序号')
    level = Field(4, label='等级')
    exp = Field(8, label='EXP')
    hp = Field(0x0C, label='HP')
    sp = Field(0x10, label='SP')
    prof = Field(0x28, label='职业')
    prof2 = Field(0x2C, label='第二职业')
    JP = Field(0x30, label='技能点数')
    extra_hp = Field(0x98, label='额外HP')
    extra_sp = Field(0x9C, label='额外SP')
    extra_un1 = Field(0xA0, label='额外??')
    extra_un2 = Field(0xA4, label='额外??')
    extra_phy_atk = Field(0xA8, label='额外的物理攻击')
    extra_phy_def = Field(0xAC, label='额外的物理防御')
    extra_attr_atk = Field(0xB0, label='额外的属性攻击')
    extra_attr_def = Field(0xB4, label='额外的属性防御')
    extra_hit = Field(0xB8, label='额外的命中')
    extra_speed = Field(0xBC, label='额外的行动速度')
    extra_critical = Field(0xC0, label='额外的暴击')
    extra_dodge = Field(0xC4, label='额外的回避')


class Main(Model):
    """基本数据"""
    money = Field((0x370, 0x158), label='金钱')
    chars = ArrayField((0x370, 0x1C8, 0), 5, ModelField(0, Character))
    items = ArrayField((0x3A8, 0), 255, ModelField(0, Item))
    items_count = Field(0x3B0, label="物品数量")
    no_encounter = ToggleField((0x78, 0x370, 0x2A8), enable=4292967266, disable=0, label="不随机遇敌")


class BattleCharacter(Model):
    """战斗中角色数据"""
    hp = Field(0x3E4, label='当前HP')
    sp = Field(0x3E8, label='当前SP')
    bp = Field(0x428, label='当前BP(可增幅点数)')


class BattleEnemy(BattleCharacter):
    """战斗中敌人数据"""
    shield = Field(0x42C, label='当前护盾')


class BattleEnemyHolder(Model):
    target = ModelField((0x160, 0x20, 0x3D8, 0xE0), BattleEnemy)


class Battle(Model):
    """战斗数据"""
    chars = ArrayField((0x150, 0x8), 5, ModelPtrField(0, BattleCharacter))
    enemys = ArrayField((0x4C0, 0x8), 5, ModelPtrField(0, BattleEnemyHolder))


class NoEncounter(Model):
    """不随机遇敌"""
    _value = Field((0x350, 0x0, 0x1A80, 0x1B8, 0x1BD8))
    value = ToggleField((0x350, 0x0, 0x1A80, 0x1B8, 0x1BD8), enable=1, disable=0)


class Base(Model):
    main = ModelPtrField(0x0289EA48, Main)
    battle = ModelPtrField(0x0289E9C8, Battle)
    encounter = Field((0x0289F060, 0x37C), label='遇敌步数')
    _no_encounter = ModelPtrField(0x029E7CE8, NoEncounter)

    @PropertyField(label="不随机遇敌")
    def no_encounter(self):
        return self._no_encounter.value

    @no_encounter.setter
    def no_encounter(self, value):
        self._no_encounter.value = value
        self.main.no_encounter = value


class BattleResult(Model):
    money = Field(0, label='金钱')
    exp = Field(4, label='经验')
    jp = Field(8, label='技能点数')
