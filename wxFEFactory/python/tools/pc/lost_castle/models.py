from tools.base.mono_models import (
    MonoClass, MonoField, MonoStaticField, MonoProperty, MonoStaticField, MonoMethod, MonoArrayT
)


class List(MonoClass):
    """列表"""
    name = 'List`1'
    namespace = 'System.Collections.Generic'

    _type = None
    Count = MonoProperty(type=int)
    _items = MonoField(type=MonoArrayT(MonoClass))

    def __iter__(self):
        _items = self._items
        for i in range(0, self.Count):
            item = _items[i]
            # TODO cast
            if self._type:
                item = item.cast(self._type)
            yield item

    def __getitem__(self, i):
        item = self._items[i]
        if self._type:
            item = item.cast(self._type)
        return item


class ListT(type):
    """主要用于field的type参数，表示这是一个数组"""
    def __new__(cls, _type=MonoClass):
        return type('ListNew', (List,), {'_type': _type})


class BagSystem(MonoClass):
    """背包系统"""
    namespace = 'Teran'

    m_money = MonoField(type=int, label="金钱")
    m_soul = MonoField(type=int, label="灵魂")

    UpdateMoney = MonoMethod()
    AddSoul = MonoMethod(param_count=1, signature='L')
    # void pickupItem(Item item, bool isSetToCur = true)
    pickupItem = MonoMethod(param_count=2, signature='PB')


class Item(MonoClass):
    namespace = 'Teran'
    GetItemName = MonoMethod(type=str, size=64)
    GetIntro = MonoMethod(type=str, size=256)
    itemName = MonoField(type=str, size=64)


class Entity(MonoClass):
    """实体"""
    namespace = 'Teran'
    NetId = MonoProperty(type=int)
    IsOwner = MonoProperty(type=bool)


class HeroBase(Entity):
    Update = MonoMethod(compile=True)
    RpcHadUseSkill = MonoMethod(compile=True)
    # 切换武器 ChangeWeapon(Equipment newWeapon)
    ChangeWeapon = MonoMethod(param_count=1, signature='P')


class Hero(HeroBase):
    """英雄"""
    namespace = 'Teran'
    propertiesInspector = MonoField(type='PropertiesInspector')
    basicAttribute = MonoField(type='BasicAttribute')
    CDTimeFactor = MonoField(type=float, label="CD时间倍率(最大3)")


class PropertiesInspector(MonoClass):
    """角色属性"""
    name = 'Creature/PropertiesInspector'
    namespace = 'Teran'
    CurrentHp = MonoProperty(type=int, label="当前HP")
    maxHp = MonoField(type=int, label="最大HP")
    currentHp = MonoField(type=int, label="当前HP")
    attack = MonoField(type=int, label="攻击")
    defence = MonoField(type=int, label="防御")
    critical = MonoField(type=int, label="暴击")
    whiteHp = MonoField(type=int, label="护盾")


class BasicAttribute(MonoClass):
    """基本属性"""
    name = 'Creature/BasicAttribute'
    namespace = 'Teran'
    hp = MonoField(type=int, label="HP")
    attack = MonoField(type=int, label="攻击")
    defence = MonoField(type=int, label="防御")
    critical = MonoField(type=int, label="暴击")


class BagMgr(MonoClass):
    """背包管理器"""
    namespace = 'Teran'
    GetBagSystem = MonoMethod(param_count=1, signature='L', type=BagSystem)


class ItemDropSys(MonoClass):
    """背包管理器"""
    namespace = 'Teran'
    equip_dropSys = MonoField(type='EquipmentDropSys')


class EquipmentDropSys(MonoClass):
    namespace = 'Teran'
    GetEquip = MonoMethod(param_count=1, signature='P', type='MonoClass')


class EquipmentMgr(MonoClass):
    namespace = 'Teran'
    weapons = MonoField(type=ListT(Item))
    armors = MonoField(type=ListT(Item))


class DDSystem(MonoClass):
    """管理类"""
    namespace = 'Teran'
    bagMgr = MonoField(type=BagMgr)
    itemDropSys = MonoField(type=ItemDropSys)
    equipMgr = MonoField(type=EquipmentMgr)
    heros = MonoField(type=List)

    @property
    def hero(self):
        hero = self.heros._items[0].cast(Hero)
        if not hero.mono_object:
            raise ValueError('获取英雄失败')
        return hero

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
