from ..base import BaseNesHack
from lib.hack.form import Group, DialogGroup, StaticGroup, ModelInput, ModelCheckBox, ModelSelect, ModelFlagWidget, Input
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib import utils
from . import models, datasets
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseNesHack):

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self._personins = models.Person(0, self.handler)
        self.person_index = 0
    
    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("money", "金钱")
            ModelInput("exp", "驾驶员经验")

        with Group("player", "我方角色", self.weak._person, cols=4):
            ui.Text("角色", className="input_label expand")
            with ui.Horizontal(className="fill"):
                ui.Choice(className="fill", choices=datasets.PARTNERS, onselect=self.on_person_change).setSelection(0)
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
            

        # with Group("enemy", "敌人", None, cols=4):
        #     for addr, name in models.ENEMY_ATTRS:
        #         Input(name, None, addr, size=1)

        with StaticGroup("快捷键"):
            with ui.ScrollView(className="fill"):
                ui.Text("恢复HP: alt+h")

    def get_hotkeys(self):
        this = self.weak
        return (
            ('pull_through', MOD_ALT, getVK('h'), this.pull_through),
        )

    def on_person_change(self, lb):
        self.person_index = lb.index

    def _person(self):
        self._personins.addr = self.person_index
        return self._personins

    person = property(_person)

    def persons(self):
        person = models.Person(0, self.handler)
        for i in range(2):
            person.addr = i
            yield person

    def pull_through(self, _=None):
        for person in self.persons():
            person.set_with("体力最大值", "体力当前值")
            person.set_with("气力最大值", "气力当前值")