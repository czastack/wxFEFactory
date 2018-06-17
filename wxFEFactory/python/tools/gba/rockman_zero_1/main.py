from ..base import BaseGbaHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelFlagWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
from lib.hack.model import Model, Field, ByteField, WordField, ArrayField
from lib import utils
import fefactory_api
ui = fefactory_api.ui


class Global(Model):
    hp = ByteField(0x0202B62C)
    hpmax = ByteField(0x0202B723)
    limit_time = ByteField(0x02022CDC) # 限时关卡的时间
    lives = ByteField(0x0202A5D0)
    invincible = ByteField(0x0202B634)
    money = WordField(0x0202B79E)
    level = ByteField(0x0202B718)
    weapon_flag = ByteField(0x0202B728)
    element_flag = ByteField(0x0202B729)
    weapon_level = Field(0x0202B734)
    weapon_level_1 = ByteField(0x0202B734)
    weapon_level_2 = ByteField(0x0202B735)
    weapon_level_3 = ByteField(0x0202B736)
    weapon_level_4 = ByteField(0x0202B737)
    fairy_flag = ArrayField(0x0202B744, 5, Field(0))
    fairy_use_count = ArrayField(0x0202B758, 5, WordField(0))


LEVELS = ('F', 'E', 'D', 'C', 'B', 'A', 'S')
WEAPONS = ('光弹枪', '光束刀', '三尖矛', '护盾回旋镖')


class Tool(BaseGbaHack):

    def __init__(self):
        super().__init__()
        self._global = Global(0, self.handler)
    
    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("hp", "HP")
            ModelInput("hpmax", "最大HP")
            ModelInput("lives", "生命")
            ModelInput("limit_time", "限时关卡的时间")
            ModelInput("money", "水晶")
            ModelInput("weapon_level_1", "光弹枪等级")
            ModelInput("weapon_level_2", "光束刀等级")
            ModelInput("weapon_level_3", "三尖矛等级")
            ModelInput("weapon_level_4", "护盾回旋镖等级")
            ModelSelect("level", "等级", choices=LEVELS)
            ModelFlagWidget("weapon_flag", "武器", labels=WEAPONS)
            ModelCheckBox("invincible", "无敌", enableData=0xFF, disableData=0)

        with StaticGroup("功能"):
            with ui.GridLayout(cols=4, vgap=10, className="expand"):
                for name in ('max_weapon_level', 'all_weapon', 'all_element', 'all_fairy', 'fairy_use_count_infinite'):
                    func = getattr(self.weak, name)
                    ui.Button(func.__doc__, onclick=func)

    def get_hotkeys(self):
        this = self.weak
        return (
            ('pull_through', MOD_ALT, getVK('h'), this.pull_through),
            ('invincible', MOD_ALT, getVK('i'), this.invincible),
        )

    def pull_through(self, _):
        self._global.set_with('hp', 'hpmax')

    def invincible(self, _=None):
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