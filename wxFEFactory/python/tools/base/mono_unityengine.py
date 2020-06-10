from tools.base.mono_models import (
    MonoClass, MonoField, MonoStaticField, MonoProperty, MonoStaticField, MonoMethod, MonoArrayT
)


class GameObject(MonoClass):
    """游戏对象"""
    namespace = 'UnityEngine'
    Find = MonoMethod(param_count=1, signature='P', type='self')
    GetComponentByName = MonoMethod(param_count=1, signature='P', type=MonoClass)


class Resources(MonoClass):
    """资源"""
    namespace = 'UnityEngine'
    Load = MonoMethod(param_count=1, signature='P', type='MonoClass')


class TextAsset(MonoClass):
    """文本资源"""
    namespace = 'UnityEngine'
    ToString = MonoMethod(type=MonoClass)
