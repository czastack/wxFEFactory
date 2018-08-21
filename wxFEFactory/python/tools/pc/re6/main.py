from functools import partial
from lib.hack.forms import (
    Group, StaticGroup, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget,
    ModelChoiceDisplay
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.native_hacktool import NativeHacktool
from fefactory_api import ui
from . import models, datasets
import fefactory_api


class Main(NativeHacktool):
    CLASS_NAME = WINDOW_NAME = 'RESIDENT EVIL 6'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)
        self.ingame_item = models.IngameItem(0, self.handler)
        self.char_index = self._global.char_index = 0

    def render_main(self):
        person = (self._person, models.Character)

        with Group("player", "全局", self._global):
            ModelInput("skill_points", instance=(self._skill_points, models.SkillPoints))

        with Group("player", "角色", person):
            Choice("角色", datasets.PERSONS, self.weak.on_person_change)
            ModelInput("health")
            ModelInput("health_max")
            ModelInput("stamina")
            ModelInput("stamina_max")
            ModelInput("moving_speed")
            ModelInput("rapid_fire")
            ModelInput("is_wet")
            ModelCoordWidget("coord", labels=('X坐标', 'Z坐标', 'Y坐标'), savable=True)
            ModelCheckBox("invincible")

        self.lazy_group(Group("person_items", "角色物品", person, serializable=False, cols=4), self.render_person_items)
        self.lazy_group(Group("person_skills", "角色技能", self._global, cols=4), self.render_person_skills)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)
        self.lazy_group(StaticGroup("功能"), self.render_functions)

    def render_person_items(self):
        """游戏中物品"""
        for label, index_range in (('水平武器', (0, 7)), ('药丸', (7, 8)), ('垂直武器', (8, 13)), ('其他物品', (15, 24))):
            r = 1
            for i in range(*index_range):
                prop = "items.%d" % i
                select = ModelChoiceDisplay(prop + ".type", "%s%d" % (label, r),
                    choices=datasets.INVENTORY_ITEMS.choices, values=datasets.INVENTORY_ITEMS.values)
                with select.container:
                    ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_ingame_item, self.weak,
                        instance=self._person, prop=prop))
                r += 1

    def render_person_skills(self):
        for i in range(3):
            ModelSelect("char_skills.$char_index.%d" % i, "技能%d" % (i + 1), choices=datasets.SKILLS)

    def render_assembly_functions(self):
        # NOP_7 = b'\x90' * 7
        NOP_8 = b'\x90' * 8
        # NOP_9 = b'\x90' * 9
        functions = (
            ('子弹不减', ('ammo_keep', b'\x66\x29\x54\x41\x0A\x79\x07', 0x900000, 0xA00000,
                b'\x66\x4A\x90\x90\x90', None, True)),
            ('无后坐力', ('no_recoil', b'\xF3\x0F\x10\x8E\xFC\x4A\x00\x00', 0x680000, 0x700000, NOP_8, None, True)),
            ('快速射击', ('rapid_fire', b'\xF3\x0F\x5C\xC2\xF3\x0F\x11\x86\x4C\x4F\x00\x00', 0x680000, 0x700000, b'',
                b'\xF3\x0F\x58\xD2\xF3\x0F\x58\xD2\xF3\x0F\x5C\xC2\xF3\x0F\x11\x86\x4C\x4F\x00\x00',
                True, True)),
            ('佣兵模式时间不减', ('merce_timer_keep', b'\xF3\x0F\x11\x86\x6C\x48\x00\x00\xF3\x0F\x11\x8E\x74\x48\x00\x00',
                0x100000, 0x200000, NOP_8, None, True)),
            ('血不减+一击必杀', ('god_on_hit_kill', b'\x66\x8b\x44\x24\x04\x66\x29\x81\x10\x0f\x00\x00', 0x600000, 0x700000,
                b'', b'\x83\x79\x38\x01\x75\x0A\xC7\x81\x10\x0F\x00\x00\x00\x00\x00\x00', True, True)),
            ('技能点数', ('skill_points', b'\x8B\xBE\x88\x05\x00\x00\x8B\x8E\x8C\x05\x00\x00', 0x580000, 0x640000,
                b'', b'\x8B\xBE\x88\x05\x00\x00\x8B\x8E\x8C\x05\x00\x00\x89\x35%s',
                True, True, False, ('skill_points_base',))),
        )
        super().render_assembly_functions(functions)

    def render_functions(self):
        super().render_functions(('unlock_guns', 'give_rocket_launcher'))

    def get_ingame_item_dialog(self):
        """物品信息对话框"""
        name = 'ingame_item_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(name, "物品详情", self.ingame_item, cols=1, dialog_style={'width': 800, 'height': 1400},
                    closable=False, horizontal=False, button=False) as dialog:
                ModelCheckBox("enabled")
                ModelInput("slot")
                ModelSelect("type", choices=datasets.INVENTORY_ITEMS.choices, values=datasets.INVENTORY_ITEMS.values,
                    instance=self.ingame_item)
                ModelInput("quantity")
                ModelInput("max_quantity")
                ModelInput("model", hex=True)
            with dialog.footer:
                ui.Button("复制", className='btn_sm', onclick=self.weak.ingame_item_copy)
                ui.Button("粘贴", className='btn_sm', onclick=self.weak.ingame_item_paste)

            setattr(self, name, dialog)
        return dialog

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.H, this.pull_through_all),
            (VK.MOD_ALT, VK.R, this.set_ammo_full),
            (VK.MOD_ALT, VK.getCode(','), this.save_coord),
            (VK.MOD_ALT, VK.getCode('.'), this.load_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode(','), this.undo_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode('.'), this.reload_coord),
            (VK.MOD_ALT, VK.O, this.p1_go_p2),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.O, this.p2_go_p1),
        )

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr

    def _person(self):
        if self.handler.active:
            return self._global.character_struct.chars[self.char_index]

    def _person_config(self):
        if self.handler.active:
            return self._global.character_config.chars[self.char_index]

    def _skill_points(self):
        skill_points_base = self.get_variable('skill_points_base')
        if skill_points_base:
            return models.SkillPoints(self.handler.read32(skill_points_base), self.handler)
        print('未初始化')

    @property
    def saved_items(self):
        return self._global.character_config.saved_items[self.char_index].items

    person = property(_person)
    person_config = property(_person_config)

    def on_person_change(self, lb):
        self.char_index = self._global.char_index = lb.index

    def show_ingame_item(self, view, instance, prop):
        """显示物品详情对话框"""
        if callable(instance):
            instance = instance()
        item = getattr(instance, prop)
        if item and item.addr:
            self.ingame_item.addr = item.addr
            dialog = self.get_ingame_item_dialog()
            dialog.read()
            dialog.show()
        else:
            print("没有数据")

    @property
    def saved_item_manager(self):
        addr = self.handler.remote_call(0x4F7230, 0)
        addr = self.handler.read32(addr + 0x658)
        return models.SavedItemManager(addr, self.handler)

    def set_ingame_item(self, slot, type, ammo, character=0):
        """设置物品 TODO: 加载物品模型"""
        func_addr = self.get_cached_address('_set_ingame_item', b'\x51\x53\x55\x8B\x6C\x24\x14\xC1', 0x600000, 0x700000)
        self.native_call_auto(func_addr, '5L', slot, type, ammo, 0, 0, this=character or self.person.addr)

    def set_ingame_saved_item(self, slot, type, quantity=0):
        """检查点间有效"""
        targets = []
        temp = self.saved_item_manager
        targets.append(temp.saved_items[self.char_index].items[slot])
        targets.append(temp.saved_items2[self.char_index].items[slot])
        targets.append(self._global.character_config.saved_item_manager.saved_items2[self.char_index].items[slot])
        for item in targets:
            item.type = type
            if quantity:
                item.quantity = quantity

    def ingame_item_copy(self, _):
        fefactory_api.set_clipboard(self.ingame_item.hex())

    def ingame_item_paste(self, _):
        self.ingame_item.fromhex(fefactory_api.get_clipboard())

    def pull_through(self, _=None):
        self.person.set_with('health', 'health_max').set_with('stamina', 'stamina_max')

    def pull_through_all(self, _=None):
        character_struct = self._global.character_struct
        for i in range(character_struct.chars_count):
            character_struct.chars[i].set_with('health', 'health_max')

    def set_ammo_full(self, _):
        person = self.person
        person.items[person.cur_item].set_with('quantity', 'max_quantity')

    def save_coord(self, _):
        self.last_coord = self.person.coord.values()

    def load_coord(self, _):
        person = self.person
        self.prev_coord = person.coord.values()
        person.coord = self.last_coord

    def undo_coord(self, _):
        self.person.coord = self.prev_coord

    def reload_coord(self, _):
        self.person.coord = self.last_coord

    def p1_go_p2(self, _):
        chars = self._global.character_struct.chars
        chars[self.char_index].coord = chars[self.char_index + 1].coord.values()

    def p2_go_p1(self, _):
        chars = self._global.character_struct.chars
        chars[self.char_index + 1].coord = chars[self.char_index].coord.values()

    def unlock_guns(self, _):
        """解锁横向武器"""
        items = self._global.character_config.saved_item_manager.saved_items2[self.char_index].items
        person = self.person
        for i in range(7):
            if items[i].type:
                person.items[i].enabled = True

    def give_rocket_launcher(self, _):
        """火箭发射器(检查点)"""
        self.set_ingame_saved_item(12, 0x11b, 1)
