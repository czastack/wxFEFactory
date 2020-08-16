from lib.hack.forms import Group, DialogGroup, ModelInput, ModelSelect, Choice
from lib import ui
from ..base import BaseGbaHack


class ExTool(BaseGbaHack):
    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self.character = self.models.Character(0, self.handler)

    def render_main(self):
        datasets = self.datasets
        character = self.character

        with Group("global", "全局", self._global):
            ModelInput("partner_count", "我方人数")
            ModelInput("enemy_count", "敌方人数")

        with Group("player", "角色", character, cols=4) as group:
            Choice("角色", ("国夫", "阿力"), self.on_character_change)
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
            for name, label, choices in (
                    ("tools", "道具", datasets.ITEMS),
                    ("skills", "技能", datasets.SKILLS),
                    ("skillkeys", "技能按键", datasets.SKILLKEYS)):
                with DialogGroup(name, label, character, cols=4, dialog_style=dialog_style) as dialog_group:
                    with ModelSelect.choices_cache:
                        for i in indexs:
                            ModelSelect("%s.%d" % (name, i), "%s%02d" % (label, i + 1), choices=choices)

    def on_character_change(self, lb):
        self.character.addr = self.PERSON_ADDR_START + lb.index * 0x9c
