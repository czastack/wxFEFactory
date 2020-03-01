from tools.base.mono_models import MonoClass, MonoField, MonoStaticField, MonoProperty, MonoStaticField


class GirlData(MonoClass):
    """角色数据"""
    Money = MonoField(type=int, label="金钱")
    Hp = MonoField(type=int, label="生命")
    PhysicAtk = MonoField(type=float, label="物理攻击")
    MagicAtk = MonoField(type=float, label="魔法攻击")
    CureAtk = MonoField(type=float, label="治疗效果")
    RageAtk = MonoField(type=float, label="怒气效果")

    curAbyssLevel = MonoField()
    curAbyssIndex = MonoField()
    abyssScore = MonoField()
    totalAbyssGold = MonoField()
    playerAbyssScore = MonoField()
    saveRage = MonoField()


class GameTool(MonoClass):
    """游戏工具"""
    need_vtable = True
    roleData = MonoStaticField(type=GirlData)


class Role(MonoClass):
    """角色"""
    CurHP = MonoProperty(label="生命")
    MaxHP = MonoProperty(label="生命上限")
    OrgPhysicAtk = MonoProperty(type=float, label="原始物理攻击")
    OrgMagicAtk = MonoProperty(type=float, label="原始魔法攻击")
    OrgPhysicDef = MonoProperty(type=float, label="原始物理防御")
    OrgMagicDef = MonoProperty(type=float, label="原始魔法攻击")
    PhysicAtk = MonoProperty(type=float, label="物理攻击")
    MagicAtk = MonoProperty(type=float, label="魔法攻击")
    PhysicDef = MonoProperty(type=float, label="物理防御")
    MagicDef = MonoProperty(type=float, label="魔法攻击")
    CureRate = MonoProperty(type=float, label="治疗率")
    VampireRate = MonoProperty(type=float, label="吸血率")


class Enemy(Role):
    """对战时敌人"""
    BrokeClothLevel = MonoProperty(label="爆衣等级")


class Player(Role):
    """对战时玩家"""
    CurRage = MonoProperty(type=float, label="当前怒气")
    MaxRage = MonoProperty(type=float, label="最大怒气")
    CureAtk = MonoProperty(type=float, label="治疗效果")
    RageAtk = MonoProperty(type=float, label="怒气效果")
    RageRate = MonoProperty(type=float, label="怒气率")
    RageLocked = MonoProperty(type=bool, label="怒气锁定")


class StarBox(MonoClass):
    """消消乐盒子"""
    need_vtable = True
    Instance = MonoProperty(type='self')
    Enemy = MonoProperty(type=Enemy)
    Player = MonoProperty(type=Player)
