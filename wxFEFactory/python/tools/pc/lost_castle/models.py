from tools.base.mono_models import (
    MonoClass, MonoField, MonoStaticField, MonoProperty, MonoStaticField, MonoMethod, MonoArrayT
)


class List(MonoClass):
    """列表"""
    name = 'List`1'
    namespace = 'System.Collections.Generic'

    Count = MonoProperty(type=int)
    _items = MonoField(type=MonoArrayT(MonoClass))


class BagSystem(MonoClass):
    """背包系统"""
    namespace = 'Teran'

    m_money = MonoField(type=int, label="金钱")
    m_soul = MonoField(type=int, label="灵魂")

    UpdateMoney = MonoMethod()
    AddSoul = MonoMethod(param_count=1, signature='L')


class BagMgr(MonoClass):
    """背包管理器"""
    namespace = 'Teran'
    GetBagSystem = MonoMethod(param_count=1, signature='L', type=BagSystem)


class Entity(MonoClass):
    """实体"""
    namespace = 'Teran'

    NetId = MonoProperty(type=int)


class Hero(Entity):
    """英雄"""
    namespace = 'Teran'


class DDSystem(MonoClass):
    """管理类"""
    namespace = 'Teran'
    bagMgr = MonoField(type=BagMgr)
    heros = MonoField(type=List)

    @property
    def hero(self):
        return self.heros._items[0].cast(Hero)

    @property
    def bagSystem(self):
        return self.bagMgr.GetBagSystem(self.hero.NetId)


class PhotonPlayer(MonoClass):
    ID = MonoProperty(type=int)


class PhotonNetwork(MonoClass):
    player = MonoProperty(type=PhotonPlayer)


class GameObject(MonoClass):
    """游戏对象"""
    namespace = 'UnityEngine'

    Find = MonoMethod(param_count=1, signature='P', type='self')
    GetComponentByName = MonoMethod(param_count=1, signature='P', type=MonoClass)
