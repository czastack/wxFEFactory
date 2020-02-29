from tools.base.mono_models import MonoClass, MonoField, MonoStaticField, MonoArrayT, MonoProperty, MonoMethod


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
