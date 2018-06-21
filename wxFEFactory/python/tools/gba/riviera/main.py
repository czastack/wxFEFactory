from ..base import BaseGbaHack
from lib.hack.form import Group, StaticGroup, ModelInput, ModelSelect, ModelFlagWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from . import models, datasets
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseGbaHack):
    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self.person = models.Person(0, self.handler)
    
    def render_main(self):
        person = self.person
        with Group("global", "全局", self._global):
            ModelInput("tp", "TP")
            ModelInput("kill_slot", "必杀槽").view.setToolTip("Lv1: 128, Lv2: 256, Lv3: 384, break: 389+")
            ModelInput("rage", "RAGE")
            ModelInput("member_num", "队伍人数")
            for i in range(5):
                ModelSelect("members.%d" % i, "第%d位队员" % (i + 1), choices=datasets.PERSONS)
            ModelInput("item_num", "道具数量")

        with Group("favors", "好感度", self._global):
            i = 0
            for item in datasets.GIRLS:
                ModelInput("favors.%d" % i, "%s累计好感度" % item)
                i += 1
            for item in datasets.GIRLS:
                ModelInput("favors.%d" % i, "%s本章好感度" % item)
                i += 1

        with Group("items", "道具", self._global, cols=4):
            for i in range(16):
                ModelSelect("items.%d.item" % i, "道具%d" % (i + 1), choices=datasets.ITEMS)
                ModelInput("items.%d.count" % i, "数量")

        with Group("event_items", "事件道具", self._global):
            for i, labels in enumerate(datasets.EVENT_ITEMS):
                ModelFlagWidget("event_items.%d" % i, "", labels=labels, values=datasets.EVENT_ITEM_FLAGS, checkbtn=True)

        with Group("person_battles", "战斗中", self._global, cols=4):
            for i in range(3):
                ModelInput("person_battles.%d.hp" % i, "我方单位%dHP" % (i + 1))
            for i in range(3):
                ModelInput("person_battles.%d.hp" % (i + 3), "敌方单位%dHP" % (i + 1))

        with Group("player", "角色", person, cols=4) as person_group:
            ui.Text("角色", className="input_label expand")
            ui.Choice(className="fill", choices=datasets.PERSONS, onselect=self.on_person_change).setSelection(0)
            ModelInput("hpmax", "HP上限")
            ModelInput("resist", "RESIST")
            ModelInput("str", "STR")
            ModelInput("mgc", "MGC")
            ModelInput("agl", "AGL")
            ModelInput("vit", "VIT")
            ModelInput("_resist", "抗性")

            with person_group.footer:
                ui.Button("全技能", onclick=self.weak.all_skills)

        with StaticGroup("功能"):
            self.render_functions(('enable_addition', 'all_cg', 'all_item_book', 'all_music',
                        'all_face', 'all_dubbing', 'enable_chapter8', 'all_item_desc'))


        with StaticGroup("快捷键"):
            with ui.ScrollView(className="fill"):
                ui.Text("恢复HP: alt+h")

    def get_hotkeys(self):
        return (
            ('pull_through', MOD_ALT, getVK('h'), self.weak.pull_through),
        )

    def on_person_change(self, lb):
        self.person.addr = self.person_index * lb.index

    def persons(self):
        person = models.Person(0, self.handler)
        for i in range(len(datasets.PERSONS)):
            person.addr = i * models.Person.SIZE
            yield person

    def pull_through(self, _=None):
        for person in self.persons():
            person.hp = person.hpmax

    def enable_addition(self, btn):
        """附加项开启"""
        self.handler.write16(0x0200AFDA, 0xFFFF)

    def all_cg(self, btn):
        """全CG"""
        self.handler.writeUint(0x02008570, 0xFFFFFFFFFF, 5)

    def all_item_book(self, btn):
        """全道具图鉴"""
        self.handler.write(0x02008534, b'\xff' * 0x1E)

    def all_music(self, btn):
        """全音乐"""
        self.handler.writeUint(0x020086C4, 0xFFFFFFFFFF, 5)

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

    def all_skills(self, btn):
        self.person.skills = b'\xff' * 0x48