from tools.base.mono_models import MonoClass, MonoField, MonoStaticField, MonoProperty, MonoStaticField, MonoMethod


class PlayerAttribute(MonoClass):
    set_currentEnergy = MonoMethod(param_count=1, compile=True)
    set_currentHP = MonoMethod(param_count=1, compile=True)


class UIDataBind(MonoClass):
    UpdateCharInfo = MonoMethod(compile=True)
