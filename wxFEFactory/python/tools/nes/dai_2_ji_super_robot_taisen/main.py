from lib.hack.forms import Group, DialogGroup, StaticGroup, ModelInput, ModelSelect, ModelFlagWidget, Input, Choice
from lib.win32.keys import VK
from lib import ui, utils
from ..base import BaseNesHack
from . import models, datasets


class Main(BaseNesHack):

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self.person = models.Person(0, self.handler)
        # self.weapon = models.Weapon(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("money", "金钱")
            ModelInput("exp", "驾驶员经验")

        with Group("player", "我方角色", self.person, cols=4):
            Choice("角色", datasets.PARTNERS, self.on_person_change)
            ModelInput("ability", "机体类型(海陆空)及变身能力")
            ModelInput("spiritual_type", "精神类型")
            ModelSelect("robot", "机体图", choices=datasets.ROBOTS)
            ModelInput("map_y", "地图X坐标")
            ModelInput("map_x", "地图Y坐标")
            ModelInput("map_avatar", "地图头像")
            ModelSelect("weapon_1", "上武器", choices=datasets.WEAPONS)
            ModelSelect("weapon_2", "下武器", choices=datasets.WEAPONS)
            ModelInput("mobile", "机动")
            ModelInput("strength", "强度")
            ModelInput("defense", "防卫")
            ModelInput("speed", "速度")
            ModelInput("hp", "HP")
            ModelInput("hpmax", "HP上限")
            ModelInput("move", "行动次数")
            ModelInput("spiritual", "精神")
            ModelInput("spiritual_max", "精神上限")

        self.lazy_group(Group("items", "道具", None), self.render_items)
        # self.lazy_group(Group("weapons", "武器", self.weapon), self.render_weapons)

        # with Group("enemy", "敌人", None, cols=4):
        #     for addr, name in models.ENEMY_ATTRS:
        #         Input(name, None, addr, size=1)

        with StaticGroup("快捷键"):
            ui.Text("恢复HP: alt+h")

    def render_items(self):
        for i, item in enumerate(datasets.ITEMS):
            ModelInput("items.%d" % i, item)

    # def render_weapons(self):
    #     Choice("武器", datasets.WEAPONS, self.on_weapon_change)
    #     ModelInput("range_max", "远射程")
    #     ModelInput("hit", "命中")
    #     ModelInput("range_min", "近射程")
    #     ModelInput("atk_air", "空攻击力")
    #     ModelInput("atk_land", "陆攻击力")
    #     ModelInput("atk_sea", "海攻击力")

    # def get_hotkeys(self):
    #     this = self.weak
    #     return (
    #         (VK.MOD_ALT, VK.H, this.pull_through),
    #     )

    def on_person_change(self, lb):
        self.person.addr = lb.index

    # def on_weapon_change(self, lb):
    #     self.weapon.index = self._global.weapons.addr_at(lb.index - 1)

    def persons(self):
        person = models.Person(0, self.handler)
        for i in range(len(datasets.PARTNERS)):
            person.addr = i
            yield person
