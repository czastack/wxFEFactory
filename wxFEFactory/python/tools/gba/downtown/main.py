from ..base import BaseGbaHack
from lib.hack.forms import Group, DialogGroup, ModelInput, ModelSelect, Choice
from fefactory_api import ui


class ExTool(BaseGbaHack):
    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self.person = self.models.Person(0, self.handler)

    def render_main(self):
        datasets = self.datasets
        person = self.person

        with Group("global", "全局", self._global):
            ModelInput("partner_count", "我方人数")
            ModelInput("enemy_count", "敌方人数")

        with Group("player", "角色", person, cols=4) as group:
            # ModelInput("addr_hex", "地址", readonly=True)
            Choice("角色", ("国夫", "阿力"), self.on_person_change)
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
                    ("skillkeys", "技能按键", datasets.SKILLKEYS, None)):
                with DialogGroup(name, label, person, cols=4, dialog_style=dialog_style) as dialog_group:
                    for i in indexs:
                        ModelSelect("%s.%d" % (name, i), "%s%02d" % (label, i + 1), choices=choices, values=values)

    def on_person_change(self, lb):
        self.person.addr = self.PERSON_ADDR_START + lb.index * 0x9c
