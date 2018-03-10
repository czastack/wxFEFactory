from ..base import BaseGbaHack
from lib.hack.form import Group, DialogGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseGbaHack):
    from . import models, datasets
    PERSON_ADDR_START = 0x02000414

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self.person_index = 0
    
    def render_main(self):
        datasets = self.datasets
        with Group("global", "全局", self._global, handler=self.handler):
            ModelInput("partner_count", "我方人数")
            ModelInput("enemy_count", "敌方人数")

        with Group("player", "角色", self._person, handler=self.handler, cols=4) as group:
            # ModelInput("addr_hex", "地址", readonly=True)
            ui.Text("角色", className="label_left expand")
            with ui.Horizontal(className="fill"):
                ui.Choice(className="fill", choices=("国夫", "阿力"), onselect=self.on_person_change).setSelection(0)
            ModelInput("punch", "拳")
            ModelInput("foot", "脚")
            ModelInput("arms", "武器")
            ModelInput("defense", "防御")
            ModelInput("strong", "强壮")
            ModelInput("attack", "攻击")
            ModelInput("agile", "敏捷")
            ModelInput("jump", "跳跃")
            ModelInput("stamina", "体力")
            ModelInput("hp", "生命")
            ModelInput("hpmax", "生命上限")
            ModelInput("money", "金钱")

        with group.footer:
            dialog_style = {'width': 1200, 'height': 640}
            indexs = (0, 6, 1, 7, 2, 8, 3, 9, 4, 10, 5, 11)
            for name, label, choices, values in (
                    ("tools", "道具", datasets.ITEMS, None),
                    ("skills", "技能", datasets.SKILLS, datasets.SKILL_VALUES),
                    ("skillkeys", "技能按键", datasets.SKILLKEYS, None)
                ):
                with DialogGroup(name, label, self._person, handler=self.handler, cols=4, dialog_style=dialog_style) as dialog_group:
                    self.add_close_callback(dialog_group.onRelease)
                    for i in indexs:
                        ModelSelect("%s.%d" % (name, i), "%s%02d" % (label, i + 1), None, None, choices, values)

    def on_person_change(self, lb):
        self.person_index = lb.index

    def _person(self):
        person_addr = self.PERSON_ADDR_START + self.person_index * 0x9c
        if person_addr:
            person = getattr(self, '_personins', None)
            if not person:
                person = self._personins = self.models.Person(person_addr, self.handler)
            elif person.addr != person_addr:
                person.addr = person_addr
            return person

    person = property(_person)

