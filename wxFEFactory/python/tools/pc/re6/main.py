import pyapi
from functools import partial
from lib.hack.forms import (
    Group, StaticGroup, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget,
    ModelChoiceDisplay
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from lib import ui
from tools.base.native_hacktool import NativeHacktool, AssemblyItem, Delta
from . import models, datasets


class Main(NativeHacktool):
    CLASS_NAME = WINDOW_NAME = 'RESIDENT EVIL 6'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global_ins = models.Global(0, self.handler)
        self.ingame_item = models.IngameItem(0, self.handler)
        self.char_index = self._global_ins.char_index = 0
        self.char_choice = None

    def render_main(self):
        character = (self._character, models.Character)

        with Group("player", "全局", (self._global, models.Global)):
            self.version_view = Choice("版本", datasets.VERSIONS, self.on_version_change)
            ModelInput("skill_points", instance=(self._skill_points, models.SkillPoints))

        with Group("player", "角色", character):
            self.char_choice = Choice("角色", datasets.PERSONS, self.weak.on_character_change)
            ModelInput("health")
            ModelInput("health_max")
            ModelInput("stamina")
            ModelInput("stamina_max")
            ModelInput("moving_speed")
            ModelInput("rapid_fire")
            ModelInput("is_wet")
            ModelCoordWidget("coord", labels=('X坐标', 'Z坐标', 'Y坐标'), savable=True)
            ModelCheckBox("invincible")

        self.lazy_group(Group("character_items", "角色物品", character, serializable=False, cols=4), self.render_character_items)
        self.lazy_group(Group("character_skills", "角色技能", (self._global, models.Global), cols=4), self.render_character_skills)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)
        self.lazy_group(StaticGroup("功能"), self.render_buttons_own)

    def render_character_items(self):
        """游戏中物品"""
        for label, index_range in (('水平武器', (0, 7)), ('药丸', (7, 8)), ('垂直武器', (8, 13)), ('其他物品', (15, 24))):
            row = 1
            for i in range(*index_range):
                prop = "items.%d" % i
                select = ModelChoiceDisplay(
                    prop + ".type", "%s%d" % (label, row),
                    choices=datasets.INVENTORY_ITEMS.choices, values=datasets.INVENTORY_ITEMS.values)
                with select.container:
                    ui.Button("详情", class_="btn_sm", onclick=partial(
                        __class__.show_ingame_item, self.weak,
                        instance=self._character, prop=prop))
                row += 1

    def render_character_skills(self):
        with ModelSelect.choices_cache:
            for i in range(3):
                ModelSelect("char_skills.$char_index.%d" % i, "技能%d" % (i + 1), choices=datasets.SKILLS)

    def render_assembly_buttons_own(self):
        nop_8 = b'\x90' * 8
        delta = Delta(0x200000)
        self.render_assembly_buttons((
            AssemblyItem('ammo_keep', '子弹不减', '66 29 54 41 0A 79 07', 0x900000, delta, '66 4A 90 90 90'),
            AssemblyItem('no_recoil', '无后坐力', 'F3 0F 10 8E FC 4A 00 00', 0x680000, delta, nop_8),
            AssemblyItem(
                'rapid_fire', '快速射击', 'F3 0F 5C C2 F3 0F 11 86 4C 4F 00 00', 0x680000, delta,
                b'', 'F3 0F 58 D2 F3 0F 58 D2 F3 0F 5C C2 F3 0F 11 86 4C 4F 00 00', inserted=True),
            AssemblyItem(
                'merce_timer_keep', '佣兵模式时间不减',
                'F3 0F 11 86 6C 48 00 00 F3 0F 11 8E 74 48 00 00', 0x100000, delta, nop_8),
            AssemblyItem(
                'god_on_hit_kill', '血不减+一击必杀', '66 8b 44 24 04 66 29 81 10 0f 00 00', 0x540000, delta, b'',
                '83 79 38 01 75 0A C7 81 10 0F 00 00 00 00 00 00', inserted=True),
            AssemblyItem(
                'skill_points', '技能点数', '8B BE 88 05 00 00 8B 8E 8C 05 00 00', 0x580000, delta,
                b'', b'\x8B\xBE\x88\x05\x00\x00\x8B\x8E\x8C\x05\x00\x00\x89\x35%s',
                inserted=True, args=('skill_points_base',)),
        ))

    def render_buttons_own(self):
        self.render_buttons(('unlock_guns', 'give_rocket_launcher'))

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
                ui.Button("复制", class_='btn_sm', onclick=self.weak.ingame_item_copy)
                ui.Button("粘贴", class_='btn_sm', onclick=self.weak.ingame_item_paste)

            setattr(self, name, dialog)
        return dialog

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.H, this.pull_through_all),
            (VK.MOD_ALT, VK.E, this.set_ammo_one),
            (VK.MOD_ALT, VK.R, this.set_ammo_full),
            (VK.MOD_ALT, VK(','), this.save_coord),
            (VK.MOD_ALT, VK('.'), this.load_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK(','), this.undo_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK('.'), this.reload_coord),
            (VK.MOD_ALT, VK.O, this.p1_go_p2),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.O, this.p2_go_p1),
        )

    def onattach(self):
        super().onattach()
        self._global_ins.addr = self.handler.base_addr

    def on_version_change(self, lb):
        self.version = lb.text
        self._global_ins = models.SPECIFIC_GLOBALS[self.version](self._global_ins.addr, self.handler)
        self._global_ins.char_index = self.char_index

    def _global(self):
        return self._global_ins

    def _character(self):
        if self.handler.active:
            chars = self._global_ins.character_struct.chars
            character = chars[self.char_index]
            if character.addr == 0:
                for i in range(len(datasets.PERSONS)):
                    if chars[i].addr:
                        self.char_choice.index = self.char_index = i
                        character = chars[i]
                        break
            return character

    def _character_config(self):
        if self.handler.active:
            return self._global_ins.character_config.chars[self.char_index]

    def _skill_points(self):
        skill_points_base = self.get_variable('skill_points_base')
        if skill_points_base:
            return models.SkillPoints(self.handler.read32(skill_points_base.addr), self.handler)
        print('未初始化')

    @property
    def saved_items(self):
        return self._global_ins.character_config.saved_items[self.char_index].items

    character = property(_character)
    character_config = property(_character_config)

    def on_character_change(self, lb):
        self.char_index = self._global_ins.char_index = lb.index

    def show_ingame_item(self, view, instance, prop):
        """显示物品详情对话框"""
        if callable(instance):
            instance = instance()
        item = getattr(instance, prop)
        if item and item.addr:
            self.ingame_item.addr = item.addr
            dialog = self.get_ingame_item_dialog()
            if self.handler.active:
                dialog.read()
            dialog.show()
        else:
            print("没有数据")

    @property
    def saved_item_manager(self):
        addr = self.handler.remote_call(self.handler.base_addr + self._global_ins.item_manager_func, 0)
        addr = self.handler.read32(addr + 0x658)
        return models.SavedItemManager(addr, self.handler)

    def set_ingame_item(self, slot, type, ammo, character=0):
        """设置物品 TODO: 加载物品模型"""
        func_addr = self.get_cached_address('_set_ingame_item', b'\x51\x53\x55\x8B\x6C\x24\x14\xC1', 0x600000, 0x700000)
        self.native_call_auto(func_addr, '5L', slot, type, ammo, 0, 0, this=character or self.character.addr)

    def set_ingame_saved_item(self, slot, type, quantity=0):
        """检查点间有效"""
        targets = []
        temp = self.saved_item_manager
        targets.append(temp.saved_items[self.char_index].items[slot])
        targets.append(temp.saved_items2[self.char_index].items[slot])
        targets.append(self._global_ins.character_config.saved_item_manager.saved_items2[self.char_index].items[slot])
        for item in targets:
            item.type = type
            if quantity:
                item.quantity = quantity

    def ingame_item_copy(self, _):
        pyapi.set_clipboard(self.ingame_item.hex())

    def ingame_item_paste(self, _):
        self.ingame_item.fromhex(pyapi.get_clipboard())

    def pull_through(self):
        self.character.set_with('health', 'health_max').set_with('stamina', 'stamina_max')

    def pull_through_all(self):
        character_struct = self._global_ins.character_struct
        for i in range(character_struct.chars_count):
            character_struct.chars[i].set_with('health', 'health_max')

    def set_ammo_full(self):
        character = self.character
        character.items[character.cur_item].set_with('quantity', 'max_quantity')

    def set_ammo_one(self):
        character = self.character
        character.items[character.cur_item].quantity = 1

    def save_coord(self):
        self.last_coord = self.character.coord.values()

    def load_coord(self):
        if hasattr(self, 'last_coord'):
            character = self.character
            self.prev_coord = character.coord.values()
            character.coord = self.last_coord

    def undo_coord(self):
        if hasattr(self, 'prev_coord'):
            self.character.coord = self.prev_coord

    def reload_coord(self):
        if hasattr(self, 'last_coord'):
            self.character.coord = self.last_coord

    def p1_go_p2(self):
        self._character()  # 确保当前角色正确
        chars = self._global_ins.character_struct.chars
        chars[self.char_index].coord = chars[self.char_index + 1].coord.values()

    def p2_go_p1(self):
        self._character()  # 确保当前角色正确
        chars = self._global_ins.character_struct.chars
        chars[self.char_index + 1].coord = chars[self.char_index].coord.values()

    def unlock_guns(self, _):
        """解锁横向武器"""
        items = self._global_ins.character_config.saved_item_manager.saved_items2[self.char_index].items
        character = self.character
        for i in range(7):
            if items[i].type:
                character.items[i].enable = True

    def give_rocket_launcher(self, _):
        """火箭发射器(检查点)"""
        self.set_ingame_saved_item(12, 0x11b, 1)
