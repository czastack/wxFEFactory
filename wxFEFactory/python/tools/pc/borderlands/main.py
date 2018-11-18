from functools import partial
from lib.hack.forms import (
    Group, Groups, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelCoordWidget, Input, Title
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.assembly_hacktool import AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType
from tools.assembly_code import AssemblyGroup, Variable
from tools import assembly_code
from fefactory_api import ui
from styles import styles
from . import models, datasets
import fefactory_api
import types


class Main(AssemblyHacktool):
    CLASS_NAME = 'LaunchUnrealUWindowsClient'
    WINDOW_NAME = 'Borderlands'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)
        self._weapon = models.Weapon(0, self.handler)

    def render_main(self):
        character = (self._character, models.Character)
        weapon = (self._current_weapon, models.Weapon)

        with Group("global", "全局", self._global):
            self.render_global()
        self.lazy_group(Group("character", "角色", character, cols=4), self.render_character)
        self.lazy_group(Group("character_ext", "角色额外", character), self.render_character_ext)
        self.lazy_group(Group("vehicle", "载具", self._global), self.render_vehicle)
        self.lazy_group(Group("ammo", "弹药", character, cols=4), self.render_ammo)
        self.lazy_group(Group("weapon_prof", "武器熟练度", self._global, cols=4), self.render_weapon_prof)
        self.lazy_group(Group("weapon", "武器", weapon, cols=4), self.render_weapon)
        self.lazy_group(Group("drop_rates", "掉落率", None), self.render_drop_rates)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)

    def render_global(self):
        movement_mgr = (self._movement_mgr, models.MovementManager)

        ModelInput('base_move_speed', instance=movement_mgr)
        ModelInput('current_move_speed', instance=movement_mgr)
        ModelInput('current_jump_height', instance=movement_mgr)

    def render_character(self):
        health = (self._character_health, models.ShieldHealth)
        shield = (self._character_shield, models.ShieldHealth)
        experience = (self._experience, models.Value)
        ability_cooldown = (self._ability_cooldown, models.Value)
        character_config = (lambda: self._global.mgr.play_mgr.character_config, models.CharacterConfig)

        Title('生命')
        ModelInput('value', instance=health)
        ModelInput('scaled_maximum', instance=health)
        ModelInput('base_maximum', instance=health)
        ModelInput('regen_rate', instance=health)
        ModelSelect('status', instance=health,
            choices=datasets.SHIELD_HEALTH_STATUS_CHOICES, values=datasets.SHIELD_HEALTH_STATUS_VALUES)

        Title('护甲')
        ModelInput('value', instance=shield)
        ModelInput('scaled_maximum', instance=shield)
        ModelInput('base_maximum', instance=shield)
        ModelInput('regen_rate', instance=shield)
        ModelSelect('status', instance=shield,
            choices=datasets.SHIELD_HEALTH_STATUS_CHOICES, values=datasets.SHIELD_HEALTH_STATUS_VALUES)

        Title('经验值')
        ModelInput('value', instance=experience)
        ModelInput('scaled_maximum', instance=experience)
        ModelInput('base_maximum', instance=experience)
        # ModelInput('multiplier', instance=experience)

        Title('技能冷却')
        ModelInput('value', instance=ability_cooldown)
        ModelInput('scaled_maximum', instance=ability_cooldown)
        ModelInput('base_maximum', instance=ability_cooldown)

        ModelInput('level', instance=character_config)
        ModelInput('money', instance=character_config)
        ModelInput('skill_points', instance=character_config)

    def render_character_ext(self):
        movement_mgr = (self._movement_mgr, models.MovementManager)

        ModelCoordWidget('coord', instance=movement_mgr, savable=True)

    def render_vehicle(self):
        ModelInput('vehicle_mgr.health.value', '载具血量')
        ModelInput('vehicle_mgr.boost.value', '载具推进')
        ModelInput('vehicle_mgr.boost.scaled_maximum', '载具推进最大值')
        # ModelInput('vehicle_mgr.vehicle_2.health.value', '载具2血量')
        # ModelInput('vehicle_mgr.vehicle_2.boost.value', '载具2推进')
        # ModelInput('vehicle_mgr.vehicle_2.boost.scaled_maximum', '载具2推进最大值')

    def render_ammo(self):
        for i, label in enumerate(('狙击枪', '手枪', '手雷', '左轮手枪', '冲锋枪', '霰弹枪', '战斗步枪', '火箭筒')):
            with ModelInput('weapon_ammos.%d.value' % i, label).container:
                ui.Button(label="最大", className='btn_sm', onclick=partial(self.weapon_ammo_max, i=i))
            ModelInput('weapon_ammos.%d.regen_rate' % i, '恢复速度')

    def render_weapon_prof(self):
        for i, label in enumerate(('手枪', '冲锋枪', '霰弹枪', '战斗步枪', '狙击枪', '火箭筒', '外星枪')):
            ModelInput('another_mgr.weapon_profs.%d.level' % i, '%s等级' % label)
            ModelInput('another_mgr.weapon_profs.%d.exp' % i, '经验')

    def render_weapon(self):
        ModelInput('addr_hex', '地址', readonly=True)
        ModelInput('item_price')
        # ModelInput('display_level')
        # ModelInput('actual_level')
        # ModelInput('item_actual_level')
        # ModelInput('specification_level')
        ModelInput('base_damage')
        ModelInput('base_accuracy')
        ModelInput('base_fire_rate')
        ModelInput('calculated_bullets_used')

    def render_drop_rates(self):
        self._drop_rates_scan_data = (b'\xFF\xFF\xFF\xFF', b'\x00\x00\x00????????????????????'
            b'\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

        self._drop_rates_table = (
            (b'\x4C', 'chest_awesome_ini', 'ChestAwesomeIni'),
            (b'\x53', 'verycommon', '遍地'),
            (b'\x54', 'verycommon_lower', '遍地 lower'),
            (b'\x55', 'common', '普通'),
            (b'\x57', 'uncommon', '罕见'),
            (b'\x58', 'uncommoner', '更罕见'),
            (b'\x59', 'rare', '稀有'),
            (b'\x5A', 'veryrare', '非常稀有'),
            (b'\x5B', 'awesome_verycommon', '特殊遍地'),
            (b'\x5C', 'awesome_common', '特殊普通'),
            (b'\x5D', 'awesome_uncommon', '特殊罕见'),
            (b'\x5E', 'awesome_uncommoner', '特殊更罕见'),
            (b'\x5F', 'awesome_rare', '特殊稀有'),
            (b'\x60', 'awesome_veryrare', '特殊非常稀有'),
            (b'\x61', 'awesome_legendary', '特殊传说'),
        )

        self._drop_rates_preset = (
            ('原始', (1, 200, 100, 10, 5, 1, 0.1, 0.05, 1, 1, 1, 1, 1, 0.1, 0.01)),
            ('更好', (10, 40, 20, 5, 2.5, 1, 1, 0.5, 1, 1, 1, 1, 1, 1, 0.5)),
            ('最好', (1, 0.01, 0.01, 0.01, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1, 25, 50, 100)),
            ('5x橙', (1, 200, 100, 10, 5, 1, 0.1, 0.05, 1, 1, 1, 1, 1, 0.1, 0.05)),
            ('10x橙', (1, 200, 100, 10, 5, 1, 0.2, 0.1, 1, 1, 1, 1, 1, 0.2, 0.1)),
            ('50x橙', (1, 200, 100, 10, 5, 1, 1, 0.5, 1, 1, 1, 1, 1, 1, 0.5)),
        )

        self._drop_rates = types.SimpleNamespace()

        ui.Hr()
        with ui.Horizontal(className='expand'):
            ui.Button('读取地址', onclick=self.read_drop_rates)
            for i, item in enumerate(self._drop_rates_preset):
                ui.Button(item[0], className='btn_md', onclick=partial(self.set_drop_rates_preset, index=i))
        self._drop_rates_views = [Input(key, label, addr=partial(__class__.get_drop_rates_item, self.weak, key=key),
            type=float) for _id, key, label in self._drop_rates_table]

    def render_assembly_functions(self):
        functions = (
            # AssemblyItem('accuracy_keep', '精准度不减', b'\xF3\x0F\x10\x40\x68\xF3\x0F\x11\x44\x24\x08',
            #     0x008D0000, 0x008F0000, b'\x0F\x57\xC0\x90\x90'),
            AssemblyItem('rapid_fire', '快速射击', b'\xF3\x0F\x10\x81\x94\x02\x00\x00\x0F\x2F',
                0x00330000, 0x00340000, b'\x0F\x57\xC0\x90\x90\x90\x90\x90'),
            AssemblyItem('no_recoil', '无后坐力', b'\xF3\x0F\x10\x8B\xD8\x0B\x00\x00\xF3\x0F\x10\x83\xD4\x0B\x00\x00',
                0x010C0000, 0x010D0000, b'\x0F\x57\xC0\x0F\x57\xC9' + b'\x90' * 10),
            AssemblyItem('no_reload', '无需换弹', b'\x2B\x86\xCC\x03\x00\x00\x39\x86\x90\x03\x00\x00',
                0x01130000, 0x01140000, b'',
                b'\xC7\x86\xCC\x03\x00\x00\x63\x00\x00\x00',
                inserted=True, replace_len=6),
            AssemblyItem('cur_weapon', '当前武器', b'\x8B\x86\xCC\x03\x00\x00\x33\xC9',
                0x01070000, 0x01080000, b'',
                AssemblyGroup(b'\x89\x35', assembly_code.Variable('selected_item_addr'), b'\x8B\x86\xCC\x03\x00\x00'),
                inserted=True, replace_len=6, args=('selected_item_addr',)),
        )
        super().render_assembly_functions(functions)

    def render_hotkeys(self):
        ui.Text("H: 回复护甲+血量\n"
            "P: 回复载具推进+血量\n"
            "B: 前进\n"
            "N: 向上\n"
            "Shift+N: 向下\n"
            "Alt+F: 技能冷却\n"
            ";: 弹药全满\n"
            ".: 升级\n")

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr

    def get_hotkeys(self):
        this = self.weak
        return (
            (0, VK.H, this.pull_through),
            (0, VK.U, this.vehicle_full),
            (0, VK.B, this.go_forward),
            (0, VK.N, this.go_up),
            (VK.MOD_SHIFT, VK.N, this.go_down),
            (VK.MOD_ALT, VK.F, this.ability_cooldown),
            (0, VK.getCode(';'), this.all_ammo_full),
            (0, VK.getCode('.'), this.level_up),
        )

    def _character(self):
        return self._global.mgr.play_mgr.character

    def _character_health(self):
        character = self._character()
        return character and character.health

    def _character_shield(self):
        character = self._character()
        return character and character.shield

    def _experience(self):
        character = self._character()
        return character and character.experience

    def _ability_cooldown(self):
        character = self._character()
        return character and character.ability_cooldown

    def _weapon_ammos(self):
        character = self._character()
        return character and character.weapon_ammos

    def _current_weapon(self):
        # player_config = self._player_config()
        # weapon = player_config and player_config.current_weapon
        # if weapon:
        #     if not weapon.addr:
        #         weapon.addr = self.get_variable_value('selected_item_addr', 0)
        self._weapon.addr = self.get_variable_value('selected_item_addr', 0)
        return self._weapon

    def _movement_mgr(self):
        return self._global.physics_mgr.movement_mgr

    def weapon_ammo_max(self, _=None, i=0):
        ammos = self._weapon_ammos()
        if ammos:
            ammos[i].value_max()

    def pull_through(self):
        health = self._character_health()
        if health:
            health.value_max()
        shield = self._character_shield()
        if shield:
            shield.value_max()

    def vehicle_full(self):
        vehicle_mgr = self._global.vehicle_mgr
        if vehicle_mgr.addr > 0x100000:
            vehicle_mgr.boost.value_max()
            vehicle_mgr.health.value_max()
            # if vehicle_mgr.vehicle_1.addr > 0x100000:
            #     vehicle_mgr.vehicle_1.boost.value_max()
            #     vehicle_mgr.vehicle_1.health.value_max()
            # if vehicle_mgr.vehicle_2.addr > 0x100000:
            #     vehicle_mgr.vehicle_2.boost.value_max()
            #     vehicle_mgr.vehicle_2.health.value_max()

    def go_forward(self):
        movement_mgr = self._movement_mgr()
        if movement_mgr:
            vector = movement_mgr.move_vector.values()
            coord = movement_mgr.coord
            delta_z = max(abs(vector[2] * 3), 500) if coord.z < 1500 else 0
            coord += (vector[0] * 5, vector[1] * 5, delta_z)

    def go_up(self):
        movement_mgr = self._movement_mgr()
        if movement_mgr:
            movement_mgr.coord.z += 500

    def go_down(self):
        movement_mgr = self._movement_mgr()
        if movement_mgr:
            movement_mgr.coord.z -= 500

    def all_ammo_full(self):
        ammos = self._weapon_ammos()
        if ammos:
            for ammo in ammos:
                ammo.value_max()

    def level_up(self):
        """升级"""
        character = self._character()
        if character:
            character.experience.value = self._global.mgr.play_mgr.character_config.exp_next_level

    def ability_cooldown(self):
        """技能冷却"""
        character = self._character()
        if character:
            character.ability_cooldown.value = 0

    def read_drop_rates(self, _):
        start = 0x1E000000
        end = 0x1F000000
        for _id, key, label in self._drop_rates_table:
            find_data = _id.join(self._drop_rates_scan_data)
            addr = self.handler.find_bytes(find_data, start, end, fuzzy=True)
            if addr is -1:
                addr = self.handler.find_bytes(find_data, start - 0x10000, end - 0x10000, fuzzy=True)
                if addr is -1:
                    raise ValueError('找不到地址, ' + label)
            if start == 0x1E000000:
                start = addr & 0xFFFF0000
                end = start + 0x10000
            setattr(self._drop_rates, key, addr + 0x30)

    def get_drop_rates_item(self, key):
        addr = getattr(self._drop_rates, key, 0)
        if addr is 0:
            print('未读取地址')
        return addr

    def set_drop_rates_preset(self, _, index):
        for view, value in zip(self._drop_rates_views, self._drop_rates_preset[index][1]):
            view.input_value = value
