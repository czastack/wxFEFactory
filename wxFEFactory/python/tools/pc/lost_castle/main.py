from lib import ui
from lib.hack.forms import (
    Group, StaticGroup, ModelInput, ModelAddrInput, ProxyInput, Title
)
from lib.hack.utils import Descriptor
from lib.hack.models import PropertyField
from lib.win32.keys import VK
from tools.base.assembly_code import AssemblyGroup, MemRead, ORIGIN
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems, Delta
from tools.base.mono_hacktool import MonoHacktool
from . import models, datasets


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'Lost Castle'

    def __init__(self):
        super().__init__()
        self.UnityEngine = None
        self.GameObject = None
        self.system = None
        self.ddSystem = None
        self.PhotonNetwork = None

    def onattach(self):
        super().onattach()

        mscorlib = self.native_call_1(self.mono_api.mono_image_loaded("mscorlib"))
        UnityEngine = self.native_call_1(self.mono_api.mono_image_loaded("UnityEngine"))
        self.register_classes((
            models.List,
        ), mscorlib)
        self.register_classes((
            models.GameObject,
        ), UnityEngine)

        self.register_classes((
            models.BagSystem,
            models.BagMgr,
            models.Entity,
            models.HeroBase,
            models.Hero,
            models.DDSystem,
            # models.PhotonNetwork,
            # models.PhotonPlayer,
            models.BasicAttribute,
            models.PropertiesInspector,
        ))

        self.GameObject = models.GameObject(0, self)
        self.system = self.GameObject.Find(self.call_mono_string_new('system'))
        self.ddSystem = self.system.GetComponentByName(self.call_mono_string_new('DDSystem')).cast(models.DDSystem)
        self.PhotonNetwork = models.PhotonNetwork(0, self)

        self.assembly_address_dict = {
            'no_cd': models.HeroBase.Update.mono_compile,
            'no_cd2': models.HeroBase.RpcHadUseSkill.mono_compile,
        }

    def render_main(self):
        with Group(None, "全局"):
            self.render_global()
        self.lazy_group(Group(None, "初始属性", (self.get_hero_init, models.BasicAttribute)), self.render_hero_init)
        self.lazy_group(Group(None, "属性", (self.get_hero_prop, models.PropertiesInspector)), self.render_hero_prop)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_global(self):
        ModelInput('bag_money', instance=self)
        ModelInput('bag_soul', instance=self)

    def render_hero_init(self):
        ModelInput('hp')
        ModelInput('attack')
        ModelInput('defence')
        ModelInput('critical')

    def render_hero_prop(self):
        ModelInput('currentHp')
        ModelInput('maxHp')
        ModelInput('attack')
        ModelInput('defence')
        ModelInput('critical')
        ModelInput('whiteHp')

    def get_hero_init(self):
        return self.ddSystem.hero.basicAttribute

    def get_hero_prop(self):
        return self.ddSystem.hero.propertiesInspector

    @PropertyField(label="金钱")
    def bag_money(self):
        return self.ddSystem.bagSystem.m_money

    @bag_money.setter
    def bag_money(self, value):
        bag = self.ddSystem.bagSystem
        bag.m_money = int(value)
        bag.UpdateMoney()

    @PropertyField(label="灵魂")
    def bag_soul(self):
        return self.ddSystem.bagSystem.m_soul

    @bag_soul.setter
    def bag_soul(self, value):
        bag = self.ddSystem.bagSystem
        bag.AddSoul(int(value) - bag.m_soul)

    def recover_hp(self):
        """回复HP"""
        self.ddSystem.hero.RpcRecoverHp(1000)

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.recover_hp),
        )

    def render_assembly_buttons_own(self):
        self.render_assembly_buttons((
            AssemblyItem(
                'no_cd', '技能无CD', '7A 17 77 15 F3 0F 10 05 * * * * F3 0F 5A C0 F2 0F 5A E8 F3 0F 11 6D E4',
                None, Delta(0x2000), 'C7 45 E4 00 00 C8 42', replace_len=25, find_base=False, fuzzy=True),
            # push rbp -> ret
            AssemblyItem(
                'no_cd2', '技能无CD2', '55', None, Delta(0x2000), 'C3', find_base=False),
        ))
