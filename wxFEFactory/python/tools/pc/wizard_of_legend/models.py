from tools.base.mono_models import MonoClass, MonoField, MonoStaticField, MonoArrayT, MonoProperty, MonoMethod


class NumVarStat(MonoClass):
    """数值"""
    CurrentValue = MonoProperty(type=float)  # 当前值
    ModifiedValue = MonoProperty(type=float)  # 最大值


class Health(MonoClass):
    # 生命值相关
    CurrentHealthValue = MonoProperty()  # 生命
    CurrentShieldValue = MonoProperty()  # 护盾
    CurrentGuardCountValue = MonoProperty()  # 防御次数

    healthStat = MonoField(type=NumVarStat)
    shieldStat = MonoField(type=NumVarStat)
    guardCountStat = MonoField(type=NumVarStat)


class Wallet(MonoClass):
    """钱包"""
    balance = MonoField(label="余额")
    maxBalance = MonoField(label="最大值")
    # 存入
    Deposit = MonoMethod(param_count=1, compile=True)


class Player(MonoClass):
    # 玩家
    need_vtable = True
    OverdriveProgress = MonoProperty(type=float)
    health = MonoField(type=Health)
    goldWallet = MonoStaticField(type=Wallet)
    platWallet = MonoStaticField(type=Wallet)

    # void AssignSkillSlot(int skillSlotNum, string skillID, bool setSignature = false, bool signatureStatus = false)
    # AssignSkillSlot = MonoMethod(param_count=4, signature='iP2B')
    # Player.SkillState GetSkill(string ID)
    GetSkill = MonoMethod(param_count=1, signature='P', type=MonoClass)
    # void HandleSkillUnlock(string givenID, bool isSignature)
    HandleSkillUnlock = MonoMethod(param_count=2, signature='PB')
    # void PickUpSkill(string givenID, bool isSignature = false, bool isEmpowered = false)
    PickUpSkill = MonoMethod(param_count=3, signature='P2B')
    # void GiveDesignatedItem(string givenID = "")
    GiveDesignatedItem = MonoMethod(param_count=1, signature='P')

    # # void RequestTeleportMoveToLocation(Vector2 givenLocation, bool useCheck = false)
    # RequestTeleportMoveToLocation = MonoMethod(param_count=2, signature='PB')
    # # Vector2 GetInputVector(bool faceInputVector = true, bool useAimVector = true, bool ignoreZero = true)
    # GetInputVector = MonoMethod(param_count=3, signature='3B')


class GameController(MonoClass):
    # 获取玩家实例
    need_vtable = True
    activePlayers = MonoStaticField(type=MonoArrayT(Player))


class Cooldown(MonoClass):
    # 技能冷却相关
    get_ChargesMissing = MonoMethod(compile=True)
    get_IsCharging = MonoMethod(compile=True)


class CooldownEntry(MonoClass):
    EntryUpdate = MonoMethod(compile=True)
