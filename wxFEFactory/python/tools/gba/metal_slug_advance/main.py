from ..base import BaseGbaHack
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.win32.keys import VK
from lib.exui.components import Pagination
from lib.hack.models import Model, Field, ByteField, WordField
from lib import utils
import fefactory_api
ui = fefactory_api.ui


class Global(Model):
    hp = ByteField(0x02004948, label="生命(50)")
    tankhp = ByteField(0x02005618, label="载具生命(50)")
    invincible = ByteField(0x02000028, label="无敌")
    ammo = WordField(0x02000072, label="子弹")
    bomb = ByteField(0x0200006F, label="手榴")
    shell = ByteField(0x03004756, label="机器炮弹")
    shoot_limit = ByteField(0x0200006C)
    weapon = ByteField(0x0200006D, label="武器种类")
    bombtype = ByteField(0x0200006E, label="炸弹种类")
    level_flag = ByteField(0x0200CD69)
    cards_flag = ByteField(0x0200CD70) # ~0x0200CD88
    prisoner_flag = ByteField(0x0200CD90) # ~0x0200CD9C


WEAPONS, WEAPON_VALUES = utils.split_value_label((
    (0x00, "普通"),
    (0x02, "S枪"),
    (0x03, "R枪"),
    (0x05, "H枪"),
    (0x06, "L枪"),
    (0x0A, "双弹"),
    (0x0C, "C枪"),
    (0x0D, "I枪"),
    (0x0E, "D枪"),
    (0x0F, "炮弹"),
))


BOMB_TYPES = ("手榴", "火瓶")
BOMB_VALUES = (1, 2)


class Main(BaseGbaHack):

    def __init__(self):
        super().__init__()
        self._global = Global(0, self.handler)
    
    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("hp")
            # ModelInput("tankhp")
            ModelCheckBox("invincible", enableData=0x20, disableData=0)
            ModelInput("ammo")
            ModelInput("bomb")
            ModelInput("shell")
            ModelSelect("weapon", choices=WEAPONS, values=WEAPON_VALUES)
            ModelSelect("bombtype", choices=BOMB_TYPES, values=BOMB_VALUES)

        with StaticGroup("功能"):
            self.render_functions(('max_ammo', 'fast_shoot'))

        with StaticGroup("快捷键"):
            with ui.ScrollView(className="fill"):
                ui.Text("恢复HP: alt+h")

    def get_hotkeys(self):
        this = self.weak
        return (
            ('pull_through',VK.MOD_ALT, VK.H, this.pull_through),
        )

    def pull_through(self, _=None):
        self._global.hp = 0x32
        if self._global.tankhp:
            self._global.tankhp = 0x32

    def max_ammo(self, _=None):
        """无限弹药"""
        self._global.ammo = 0xFFFF
        self._global.bomb = 0x63
        self._global.shell = 0x63

    def fast_shoot(self, _=None):
        """快速射击"""
        self._global.shoot_limit = 0xFF
