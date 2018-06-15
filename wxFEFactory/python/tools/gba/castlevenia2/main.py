from ..base import BaseGbaHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelFlagWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
from lib.hack.model import Model, Field, ByteField, WordField, ArrayField, Fields, ToggleField
from lib import utils
import fefactory_api
ui = fefactory_api.ui


class Global(Model):
    hp = WordField(0x0201326E)
    hpmax = WordField(0x02013272)
    mp = WordField(0x02013270)
    mpmax = WordField(0x02013274)
    str = WordField(0x02013276)
    con = WordField(0x02013278)
    int = WordField(0x0201327A)
    lck = WordField(0x0201327C)
    level = ByteField(0x201326D)
    invincible1 = ToggleField(0x08020910, enableData=0, disableData=0x04008008)
    enemy_static = ToggleField(0x020004BE, size=2, enableData=0xFFFF, disableData=0)
    invincible2 = ToggleField(0x02000502, size=1, enableData=0xFF, disableData=0)
    monster_flag = ArrayField(0x02013394, 7, Field(0))
    skill_flag = ArrayField(0x02013386, 3, WordField(0))
    soul_flag = ArrayField(0x02013310, 31, Field(0))
    equip_counts = ArrayField(0x020132A8, 104, ByteField(0))
    tool_counts = ArrayField(0x02013288, 32, ByteField(0))
    enemy_flag = ArrayField(0x02013394, 12, Field(0))
    map_flag = ArrayField(0x020000AC, 0x145, WordField(0))
    extra_flag = Fields(ByteField(0x02000060), ByteField(0x02000F4D))
    boss_rush_flag = ByteField(0x020000A1)


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
            ModelInput("mp", "MP")
            ModelInput("mpmax", "最大MP")
            ModelInput("str", "STR")
            ModelInput("con", "CON")
            ModelInput("int", "INT")
            ModelInput("lck", "LCK")
            ModelInput("level", "等级")
            ModelCheckBox("invincible1", "不会扣血")
            ModelCheckBox("enemy_static", "敌人静止")
            ModelCheckBox("invincible2", "暂时无敌")

        with StaticGroup("功能"):
            with ui.GridLayout(cols=4, vgap=10, className="expand"):
                for name in ('set_monster_flag', 'set_skill_flag', 'set_soul_flag', 'set_equip_counts',
                        'set_tool_counts', 'set_enemy_flag', 'set_map_flag', 'set_extra_flag', 'set_boss_rush_flag'):
                    func = getattr(self.weak, name)
                    ui.Button(func.__doc__, onclick=func)

    def get_hotkeys(self):
        this = self.weak
        return (
            ('pull_through', MOD_ALT, getVK('h'), this.pull_through),
        )

    def pull_through(self, _):
        self._global.set_with('hp', 'hpmax')
        self._global.set_with('mp', 'mpmax')
        
    def set_monster_flag(self, _):
        """全怪物数据"""
        self._global.monster_flag.fill(0xFFFFFFFF)

    def set_skill_flag(self, _):
        """全技能"""
        self._global.skill_flag.fill(0xFFFF)

    def set_soul_flag(self, _):
        """全魂"""
        self._global.soul_flag.fill(0xFFFFFFFF)

    def set_equip_counts(self, _):
        """全装备"""
        self._global.equip_counts.fill(1)

    def set_tool_counts(self, _):
        """全道具"""
        self._global.tool_counts.fill(99)

    def set_enemy_flag(self, _):
        """全敌人图鉴"""
        self._global.enemy_flag.fill(0xFFFFFFFF)

    def set_map_flag(self, _):
        """地图全开"""
        self._global.map_flag.fill(0xFFFF)

    def set_extra_flag(self, _):
        """附加项开启"""
        self._global.extra_flag = 3

    def set_boss_rush_flag(self, _):
        """存档后可进入BOSS RUSH"""
        self._global.boss_rush_flag = 0xFF