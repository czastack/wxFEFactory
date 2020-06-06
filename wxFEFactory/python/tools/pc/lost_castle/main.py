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
            models.Hero,
            models.DDSystem,
            models.PhotonNetwork,
            models.PhotonPlayer,
        ))

        self.GameObject = models.GameObject(0, self)
        self.system = self.GameObject.Find(self.call_mono_string_new('system'))
        self.ddSystem = self.system.GetComponentByName(self.call_mono_string_new('DDSystem')).cast(models.DDSystem)
        self.PhotonNetwork = models.PhotonNetwork(0, self)

    def render_main(self):
        with Group(None, "全局"):
            self.render_global()

    def render_global(self):
        ModelInput('bag_money', instance=self)
        ModelInput('bag_soul', instance=self)

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

    def render_assembly_buttons_own(self):
        self.render_assembly_buttons((
            AssemblyItem(
                'item_keep', '物品使用不消失', '8B 45 D0 39 00 E8 24 00 00 00',
                None, Delta(0x200), 'C6 47 28 00',
                find_base=False, replace_offset=5, replace_len=5),
        ))
