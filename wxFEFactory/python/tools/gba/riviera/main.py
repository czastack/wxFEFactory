from lib.hack.forms import (
    Group, StaticGroup, ModelInput, ModelArrayInput, ModelSelect, ModelArraySelect, ModelFlagWidget, Choice
)
from lib.win32.keys import VK
from lib import ui
from ..base import BaseGbaHack
from . import models, datasets


class Main(BaseGbaHack):
    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self.character = models.Character(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            self.render_global()
        self.lazy_group(Group("character", "角色", self.character, cols=4), self.render_character)
        self.lazy_group(Group("favors", "好感度", self._global), self.render_favors)
        self.lazy_group(Group("items", "道具", self._global, cols=4), self.render_items)
        self.lazy_group(Group("event_items", "事件道具", self._global), self.render_event_items)
        self.lazy_group(Group("character_battles", "战斗中", self._global, cols=4), self.render_character_battles)
        self.lazy_group(StaticGroup("功能"), self.render_buttons_own)

        with StaticGroup("快捷键"):
            ui.Text("恢复HP: alt+h")

    def render_global(self):
        ModelInput("tp")
        ModelInput("kill_slot").set_help("Lv1: 128, Lv2: 256, Lv3: 384, break: 389+")
        ModelInput("rage")
        ModelInput("member_num")
        ModelArraySelect("members", choices=datasets.PERSONS)
        ModelInput("item_num")

    def render_character(self):
        Choice("角色", datasets.PERSONS, self.on_character_change)
        ModelInput("hpmax")
        ModelInput("resist")
        ModelInput("str")
        ModelInput("mgc")
        ModelInput("agl")
        ModelInput("vit")
        ModelInput("hp_heal")
        ModelArrayInput("resistance", label=["%s抗性" % item for item in datasets.ATTRIBUTE])
        ModelFlagWidget("adaptive", cols=3, labels=datasets.ATTRIBUTE)

        with Group.active_group().footer:
            ui.Button("全技能", onclick=self.weak.all_skills)

    def render_favors(self):
        i = 0
        for item in datasets.GIRLS:
            ModelInput("favors.%d" % i, "%s累计好感度" % item)
            i += 1
        for item in datasets.GIRLS:
            ModelInput("favors.%d" % i, "%s本章好感度" % item)
            i += 1

    def render_items(self):
        with ModelSelect.choices_cache:
            for i in range(16):
                ModelSelect("items.%d.item" % i, "道具%d" % (i + 1), choices=datasets.ITEMS)
                ModelInput("items.%d.count" % i, "数量")

    def render_event_items(self):
        for i, labels in enumerate(datasets.EVENT_ITEMS):
            ModelFlagWidget("event_items.%d" % i, "", labels=labels, values=datasets.EVENT_ITEM_FLAGS,
                checkbtn=True, cols=4)

    def render_character_battles(self):
        for i in range(3):
            ModelInput("character_battles.%d.hp" % i, "我方单位%dHP" % (i + 1))
        for i in range(3):
            ModelInput("character_battles.%d.hp" % (i + 3), "敌方单位%dHP" % (i + 1))

    def render_buttons_own(self):
        self.render_buttons(('enable_extra', 'all_cg', 'all_item_book', 'all_music', 'all_face', 'all_dubbing',
            'enable_chapter8', 'all_item_desc', 'over_drive', 'rage_clear', 's_ranking'))

    def get_hotkeys(self):
        return (
            (VK.MOD_ALT, VK.H, self.weak.pull_through),
        )

    def on_character_change(self, lb):
        self.character.addr = models.Character.SIZE * lb.index

    def characters(self):
        character = models.Character(0, self.handler)
        for i in range(len(datasets.PERSONS)):
            character.addr = i * models.Character.SIZE
            yield character

    def pull_through(self):
        for character in self.characters():
            character.hp = character.hpmax

    def enable_extra(self, btn):
        """附加项开启"""
        self.handler.write16(0x0200AFDA, 0xFFFF)

    def all_cg(self, btn):
        """全CG"""
        self.handler.write_uint(0x02008570, 0xFFFFFFFFFF, 5)

    def all_item_book(self, btn):
        """全道具图鉴"""
        self.handler.write(0x02008534, b'\xff' * 0x1E)

    def all_music(self, btn):
        """全音乐"""
        self.handler.write_uint(0x020086C4, 0xFFFFFFFFFF, 5)

    def all_face(self, btn):
        """全表情"""
        self.handler.write(0x020084D8, b'\xff' * 0x22)
        self.handler.write16(0x02008504, 0xFFFF)

    def all_dubbing(self, btn):
        """全配音"""
        self.handler.write(0x020086CC, b'\xff' * 0x16)

    def enable_chapter8(self, btn):
        """第8章开启"""
        self.handler.write16(0x020084D6, 0xFFFF)

    def all_item_desc(self, btn):
        """全道具说明"""
        self.handler.write(0x020086F0, b'\xff' * 0x78)

    def over_drive(self, btn):
        """必杀槽最大"""
        self._global.kill_slot = 0x180

    def rage_clear(self, btn):
        """rage槽清空"""
        self._global.rage = 0

    def all_skills(self, btn):
        """当前角色全技能"""
        self.character.skills = b'\xff' * 0x48

    def s_ranking(self, btn):
        """获得S评价"""
        self._global.battle_time = 0
