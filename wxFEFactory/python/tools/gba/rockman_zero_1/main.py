from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelFlagWidget
from lib.win32.keys import VK
from lib.hack.models import Model, Field, ByteField, WordField, ArrayField
from fefactory_api import ui
from ..base import BaseGbaHack


class Global(Model):
    hp = ByteField(0x0202B62C, label="HP")
    hpmax = ByteField(0x0202B723, label="最大HP")
    limit_time = ByteField(0x02022CDC, label="生命")  # 限时关卡的时间
    lives = ByteField(0x0202A5D0, label="限时关卡的时间")
    invincible = ByteField(0x0202B634, label="无敌")
    money = WordField(0x0202B79E, label="水晶")
    level = ByteField(0x0202B718, label="等级")
    weapon_flag = ByteField(0x0202B728, label="武器")
    element_flag = ByteField(0x0202B729)
    weapon_level = Field(0x0202B734)
    weapon_level_1 = ByteField(0x0202B734, label="光弹枪等级")
    weapon_level_2 = ByteField(0x0202B735, label="光束刀等级")
    weapon_level_3 = ByteField(0x0202B736, label="三尖矛等级")
    weapon_level_4 = ByteField(0x0202B737, label="护盾回旋镖等级")
    fairy_flag = ArrayField(0x0202B744, 5, Field(0))
    fairy_use_count = ArrayField(0x0202B758, 5, WordField(0))


LEVELS = ('F', 'E', 'D', 'C', 'B', 'A', 'S')
WEAPONS = ('光弹枪', '光束刀', '三尖矛', '护盾回旋镖')


class Main(BaseGbaHack):

    def __init__(self):
        super().__init__()
        self._global = Global(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("hp")
            ModelInput("hpmax")
            ModelInput("lives")
            ModelInput("limit_time")
            ModelInput("money")
            ModelInput("weapon_level_1")
            ModelInput("weapon_level_2")
            ModelInput("weapon_level_3")
            ModelInput("weapon_level_4")
            ModelSelect("level", choices=LEVELS)
            ModelFlagWidget("weapon_flag", labels=WEAPONS)
            ModelCheckBox("invincible", enable=0xFF, disable=0)

        with StaticGroup("功能"):
            self.render_functions(('max_weapon_level', 'all_weapon', 'all_element', 'all_fairy',
                'fairy_use_count_infinite'))

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT, VK.I, this.invincible),
        )

    def pull_through(self):
        self._global.set_with('hp', 'hpmax')

    def invincible(self):
        self._global.invincible = 0xFF

    def max_weapon_level(self, _):
        """武器等级最高"""
        self._global.weapon_level = 0x02040603

    def all_weapon(self, _):
        """全武器"""
        self._global.weapon_flag = 0x0F

    def all_element(self, _):
        """全元素"""
        self._global.element_flag = 0x0F

    def all_fairy(self, _):
        """全精灵"""
        self._global.fairy_flag.fill(0xFFFF)

    def fairy_use_count_infinite(self, _):
        """妖精次数无限"""
        self._global.fairy_use_count.fill(0)
