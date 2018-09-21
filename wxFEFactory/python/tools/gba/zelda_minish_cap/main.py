from ..base import BaseGbaHack
from lib.hack.forms import Group, StaticGroup, ModelInput, ModelSelect, ModelCheckBox, ModelFlagWidget, Choice
from lib.hack.models import Model, Field, ByteField, WordField, ToggleField, ArrayField
from lib.win32.keys import VK
from fefactory_api import ui


class Global(Model):
    hp = ByteField(0x02002AEA, label="生命")  # A0
    hpmax = ByteField(0x02002AEB, label="生命上限")  # A0
    rupees = WordField(0x02002B00, label="宝石")  # 03E7
    rupeesmax = ByteField(0x02002AE8, label="宝石上限")  # 03
    scrolls_flag = WordField(0x02002B44, label="卷轴")  # FFFF
    skills_flag = WordField(0x0300402C, label="剑技")  # FFFF
    bomb = ByteField(0x02002AEC, label="炸弹数")  # 63
    array = ByteField(0x02002AED, label="弓箭数")  # 63
    conch = WordField(0x02002B02, label="海螺数")  # 03E7
    keys = ArrayField(0x02002E9D, 16, ByteField(0))  # 钥匙数
    help_tool = ArrayField(0x02002EAD, 16, ByteField(0))  # 迷宫辅助道具
    weapon_a = ByteField(0x02002AF4, label="A键武器")
    weapon_b = ByteField(0x02002AF5, label="B键武器")
    items_flag = Field(0x02002B32, size=8, label="物品")
    bodysize = ByteField(0x03003FB0, label="身体大小")

    all_scrolls = ToggleField(scrolls_flag.offset, enableData=0xFFFF, label="全卷轴")
    all_skills = ToggleField(skills_flag.offset, enableData=0xFFFF, label="全剑技")
    all_map = ToggleField(0x02002A80, enableData=0x1FFFF, label="地图全开")
    guide_falg = Field(0x02002B0E, bytes, 20, label="全图鉴")


def gen_flags(items, unit=1):
    return gen_flags_by_indexs(range(len(items)), unit)


def gen_flags_by_indexs(indexs, unit=1):
    return tuple((unit << (i << 1)) for i in indexs)


WEAPONS = (
    "无",
    "史密斯之剑",
    "银白之剑",
    "银白之剑(二分身)",
    "银白之剑(三分身)",
    "...(灯)",
    "四之剑",
    "炸弹",
    "遥控炸弹",
    "弓",
    "光之弓",
    "回旋镖",
    "魔法回旋镖",
    "小盾",
    "镜盾",
    "油灯(熄灭)",
    "油灯",
    "魔法壶",
    "魔杖",
    "鼹鼠手套",
    "羽毛斗篷",
    "天马之靴",
    "魔杖",
    "风之笛",
    "书(无效)",
    "蘑菇(无效)",
    "蹼(无效)",
    "油灯(拾取)",
    "空瓶1",
    "空瓶2",
    "空瓶3",
    "空瓶4",
)

ITEMS_FLAG = gen_flags(WEAPONS)

SCROLLS = ("回旋斩", "剑气斩", "冲刺斩", "剑气突", "破岩斩", "回转突", "下段突", "大回旋斩")
SCROLLS_FLAG = gen_flags_by_indexs((0, 4, 2, 7, 3, 1, 6, 5))

SKILLS = SCROLLS + ("大回旋斩时间延长", "大回旋斩次数增加", "蓄力时间缩短")
SKILLS_FLAG = (0x01, 0x10, 0x04, 0x80, 0x08, 0x02, 0x40, 0x20, 0x0000, 0x0800, 0x0200)


class Main(BaseGbaHack):
    def __init__(self):
        super().__init__()
        self._global = Global(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global, cols=4):
            ModelInput("hp")
            ModelInput("hpmax")
            ModelInput("rupees")
            ModelInput("rupeesmax")
            ModelInput("bomb")
            ModelInput("array")
            ModelInput("conch")
            ModelSelect("weapon_a", choices=WEAPONS)
            ModelSelect("weapon_b", choices=WEAPONS)
            ModelSelect("bodysize", choices=("大", "小"), values=(0, 0x80))
            ModelCheckBox("all_scrolls")
            ModelCheckBox("all_skills")
            ModelCheckBox("all_map")

        self.lazy_group(Group("items", "物品", self._global), self.render_items)

    def render_items(self):
        ModelFlagWidget("items_flag", labels=WEAPONS, values=ITEMS_FLAG, cols=4)
        ModelFlagWidget("scrolls_flag", labels=SCROLLS, values=SCROLLS_FLAG, cols=4, checkbtn=True)
        ModelFlagWidget("skills_flag", labels=SKILLS, values=SKILLS_FLAG, cols=4, checkbtn=True)

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    def pull_through(self):
        self._global.set_with('hp', 'hpmax')
