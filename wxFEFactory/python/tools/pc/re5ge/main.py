from functools import partial
from lib.hack.forms import (
    Group, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.hacktool import BaseHackTool
from fefactory_api import ui
from . import models


# item +15 slot_index size=0x30

class Main(BaseHackTool):
    CLASS_NAME = 'MTFramework'
    WINDOW_NAME = 'RESIDENT EVIL 5'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)
        self.character_struct = models.CharacterStruct(0, self.handler)
        self.person = models.Player(0, self.handler)

    def render_main(self):
        with Group("player", "角色", self.person):
            # ModelCheckBox("x_invincible", "X无敌", enableData=0xFF, disableData=0)
            Choice("角色", tuple("play%d" % i for i in range(1, 5)), self.on_person_change)
            ModelInput("hp")
            ModelInput("hpmax")
            ModelCoordWidget("moving_coord", savable=True)
            ModelCoordWidget("melee_coord", savable=True)
            ModelInput("target")
            ModelCheckBox("invincible")

        with Group("player", "全局", self._global):
            ModelInput("money", "金钱")

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    def onattach(self):
        proc_base = self.handler.proc_base
        # self.health_check = self.handler.find_bytes(b'\x66\x83\xB9\x64\x13\x00\x00\x00\x0F\x9E\xC0\xC3',
        #     proc_base + 0x00700000, proc_base + 0x00800000)
        # print(hex(self.health_check))
        self.character_struct.addr = self.handler.read_ptr(proc_base + 0x00DA2A5C)
        self.person.addr = self.character_struct.players[0].addr

    def on_person_change(self, lb):
        self.person.addr = self.character_struct.players[lb.index].addr

    def pull_through(self, _=None):
        for i in range(self.character_struct.players_count):
            self.character_struct.players[i].set_with('hp', 'hpmax')
