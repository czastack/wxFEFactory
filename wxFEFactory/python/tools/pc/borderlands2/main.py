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
    WINDOW_NAME = 'Borderlands 2 (32-bit, DX9)'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)

    def render_main(self):
        character = (self._character, models.Character)
        team_config = (self._team_config, models.TeamConfig)
        weapon = (self._current_weapon, models.Weapon)

        with Group("global", "全局", self._global):
            self.render_global()
        self.lazy_group(Group("character", "角色", character, cols=4), self.render_character)
        self.lazy_group(Group("character_ext", "角色额外", character), self.render_character_ext)
        self.lazy_group(Group("vehicle", "载具", self._global), self.render_vehicle)
        self.lazy_group(Group("ammo", "弹药", self._global, cols=4), self.render_ammo)
        self.lazy_group(Group("weapon", "武器", weapon, cols=4), self.render_weapon)
        self.lazy_group(Group("team", "团队", team_config), self.render_team)
        self.lazy_group(Groups("技能", self.weak.onNotePageChange, addr=team_config), self.render_skill)
        self.lazy_group(Group("drop_rates", "掉落率", None), self.render_drop_rates)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)
        self.lazy_group(Group("assembly_variable", "代码变量", self.variable_model), self.render_assembly_variable)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)

    def render_global(self):
        system_config = (lambda: self._global.mgr.system_config, models.SystemConfig)
        physics_config = (lambda: self._global.mgr.player_mgr.physics_config, models.PhysicsConfig)

        ModelInput('time_scale_multiplier', instance=system_config)
        ModelInput('gravity', instance=system_config)

        ModelInput('move_speed', instance=physics_config)
        ModelInput('jump_height', instance=physics_config)
        ModelInput('friction', instance=physics_config)
        ModelInput('viewing_height', instance=physics_config)

    def render_character(self):
        health = (self._character_health, models.ShieldHealth)
        shield = (self._character_shield, models.ShieldHealth)
        experience = (self._experience, models.Experience)
        player_mgr = (self._player_mgr, models.PlayerManager)

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
        ModelInput('multiplier', instance=experience)

        ModelInput('exp_next_level')
        ModelInput('level')
        ModelInput('money')
        ModelInput('eridium')
        ModelInput('seraph_crystals')
        ModelInput('torgue_tokens')
        ModelInput('skill_points')

        ModelInput('bank_size', instance=player_mgr)
        ModelInput('weapon_deck_size', instance=player_mgr)
        ModelInput('backpack_size', instance=player_mgr)
        ModelInput('backpack_used_space', instance=player_mgr)

    def render_character_ext(self):
        player_config = (self._player_config, models.PlayerConfig)

        ModelCoordWidget('coord', instance=player_config, savable=True)
        ModelInput('player_visibility', instance=player_config).set_help('216: 对敌人不可见')
        ModelInput('move_speed_mult', instance=player_config)
        ModelInput('second_wind.multiplier', '原地复活生命倍数', instance=player_config)
        ModelInput('second_wind.fight_time_multiplier', '原地复活时间倍数', instance=player_config)

    def render_vehicle(self):
        ModelInput('mgr.vehicle_mgrs.0.health.value', '载具1血量')
        ModelInput('mgr.vehicle_mgrs.0.boost.value', '载具1推进')
        ModelInput('mgr.vehicle_mgrs.1.health.value', '载具2血量')
        ModelInput('mgr.vehicle_mgrs.1.boost.value', '载具2推进')

    def render_ammo(self):
        for i, label in enumerate(('突击步枪子弹', '霰弹枪子弹', '手雷', '冲锋枪子弹', '手枪子弹', '火箭炮弹药', '狙击步枪子弹')):
            with ModelInput('mgr.weapon_ammos.%d.value' % i, label).container:
                ui.Button(label="最大", className='btn_sm', onclick=partial(self.weapon_ammo_max, i=i))
            ModelInput('mgr.weapon_ammos.%d.regen_rate' % i, '恢复速度')

    def render_weapon(self):
        ModelInput('addr_hex', '地址', readonly=True)
        ModelInput('display_level')
        ModelInput('actual_level')
        ModelInput('item_actual_level')
        ModelInput('specification_level')
        ModelInput('base_damage')
        ModelInput('base_accuracy')
        ModelInput('base_fire_rate')
        ModelInput('base_projectile_speed')
        ModelInput('calculated_projectile_speed')
        ModelInput('base_reload_speed')
        ModelInput('base_burst_length')
        ModelInput('base_projectiles_per_shot')
        ModelInput('base_bullets_used')
        ModelInput('base_extra_shot_chance')
        ModelInput('magazine_size')
        ModelInput('current_bullets')
        ModelInput('clip_ammo')
        ModelInput('item_price')
        ModelInput('item_quantity')
        ModelInput('item_state')

    def render_team(self):
        ModelInput('team_ammo_regen')
        ModelInput('badass_tokens')

    def render_skill(self):
        with Group('main_skill', "主技能"):
            ModelInput('skill_mgr.main_skill', '主技能状态')
            ModelInput('skill_mgr.main_skill_duration', '主技能持续时间')
            ModelInput('main_skill_cooldown_timer')
            ModelInput('main_skill_cooldown_mult')

        def render_sub_skill(data):
            i = 0
            for page in data:
                with Group(None, page[0], cols=4):
                    for item in page[1]:
                        ModelInput('skill_mgr.skills.%d.status' % i, item)
                        i += 1

        for i, item in enumerate(datasets.SKILL_NAMES):
            self.lazy_group(Groups(item[0]), partial(render_sub_skill, item[2]))

    def render_drop_rates(self):
        self._drop_rates_scan_data = (b'\x00\x00\x00????????????????????\x00\x00\x00\x00\x01\x00\x00\x00????'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x3F\x00\x00\x80\x3F')

        self._drop_rates_table = (
            (b'\x2C', 'very_common', '药'),
            (b'\x2E', 'common', '白'),
            (b'\x30', 'uncommon', '绿'),
            (b'\x31', 'very_uncommon', '粉'),
            (b'\x32', 'rare', '蓝'),
            (b'\x33', 'very_rare', '紫'),
            (b'\x34', 'legendary', '橙/珠光')
        )

        self._drop_rates_preset = (
            ('原始', (200, 100, 10, 5, 1, 0.1, 0.01)),
            ('仅橙', (0.001, 0.001, 0.001, 0.001, 0.001, 100, 10000)),
            ('仅紫', (0.001, 0.001, 0.001, 0.001, 0.001, 1000, 0.001)),
            ('仅蓝', (0.001, 0.001, 0.001, 0.001, 1000, 0.001, 0.001)),
            ('10x橙', (200, 100, 10, 5, 1, 0.1, 0.1)),
            ('100x橙', (200, 100, 10, 5, 1, 0.1, 1)),
            ('1000x橙', (200, 100, 10, 5, 1, 0.1, 10)),
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
            # AssemblyItems('子弹不减+精准+无后坐',
            #     AssemblyItem('ammo_keep', None, b'\x88\x5D\xFC\x8B\x86',
            #         0x00DE0000, 0x00EF0000, b'',
            #         b'\x9C\x60\xA1\x04\x09\xB7\x03\x8B\x80\x70\x04\x00\x00\x39\xF0\x0F\x85\x5E\x00\x00\x00'
            #         b'\xC7\x86\xDC\x09\x00\x00\x00\x00\x00\x00\x8B\x80\xD0\x09\x00\x00\xC7\x80\x04\x01\x00\x00'
            #         b'\x02\x00\x00\x00\xC7\x86\xEC\x08\x00\x00\x00\x7C\x12\x48\xC7\x86\xD8\x08\x00\x00\xCD\xCC\x4C\x3D'
            #         b'\xC7\x86\xC4\x08\x00\x00\xCD\xCC\x4C\x3D\x31\xC9\x8B\x3D\x08\x09\xB7\x03\x89\x8F\x0C\x0E\x00\x00'
            #         b'\x89\x8F\x10\x0E\x00\x00\x89\x8F\x14\x0E\x00\x00\x89\x8F\x18\x0E\x00\x00\x89\x8F\x1C\x0E\x00\x00'
            #         b'\x61\x9D\x8B\x86\x28\x0A\x00\x00',
            #         inserted=True, replace_len=6, replace_offset=3),
            #     AssemblyItem('ammo_keep2', None, b'\x89\x7D?\x89\x7D?\x89\x7D?\x8B\x06\x8B\x55',
            #         0x008A0000, 0x008B0000, b'',
            #         b'\x9C\x60\x8B\x0D\x04\x09\xB7\x03\x8B\x89\x70\x04\x00\x00\x39\xC8\x0F\x85\x08\x00\x00\x00'
            #         b'\xC7\x44\x24\x2C\x00\x00\x00\x00\x61\x9D\x55\x8B\xEC\x6A\xFF',
            #         inserted=True, replace_len=5, replace_offset=-0x2F, fuzzy=True)),
            AssemblyItem('ammo_inf', '子弹不减+精准不减', b'\xF3\x0F\x58\x45\x08\x51',
                0x007F0000, 0x00810000, b'',
                AssemblyGroup(
                    b'\x83\x79\x48\x00\x75\x24\x83\x79\x4C\x00\x75\x1E\x0F\xAE\x05',
                    assembly_code.Variable('fxbuff'),
                    b'\xF3\x0F\x10\x4D\x08\x0F\x57\xDB\x0F\x2F\xCB\x7E\x31\xF3\x0F\x11\x5D\x08\xE9\x27\x00\x00\x00'
                    b'\x0F\xAE\x05', assembly_code.Variable('fxbuff'),
                    b'\xF3\x0F\x10\x4D\x08\x0F\x57\xDB\x0F\x2F\xCB\x7A\x13\x72\x11\xF3\x0F\x10\x25',
                    assembly_code.Variable('minus_one'), b'\xF3\x0F\x59\xCC\xF3\x0F\x11\x4D\x08\x0F\xAE\x0D',
                    assembly_code.Variable('fxbuff'), b'\xF3\x0F\x58\x45\x08'
                ),
                inserted=True, replace_len=5,
                args=(VariableType('fxbuff', size=512, align=16), VariableType('minus_one', value=0xBF800000))),
            AssemblyItem('ammo_inf2', '无需换弹', b'\x3B\xC1\x7C\x0B\x8B\x55\x0C\x89\x02\x8B\xE5\x5D\xC2\x08\x00',
                0x002A0000, 0x002B0000, b'', b'\x8B\x02\x89\x02\x8B\xE5\x5D',
                inserted=True, replace_len=5, replace_offset=7),
            AssemblyItem('no_recoil', '无后坐力', b'\xF3\x0F\x2C\x8F\x10\x0E\x00\x00',
                0x001A0000, 0x001B0000, b'',
                b'\x31\xC9\x89\x8F\x0C\x0E\x00\x00\x89\x8F\x10\x0E\x00\x00\x89\x8F\x14\x0E\x00\x00'
                    b'\x89\x8F\x18\x0E\x00\x00\x89\x8F\x1C\x0E\x00\x00',
                inserted=True, replace_len=8),
            AssemblyItem('without_golden_keys', '无需金钥匙', b'\x74\x1D\x8A\x54',
                0x00500000, 0x00510000, b'\xEB\x1D\x8A\x54'),
            AssemblyItem('raid_boss_before', '无限刷BOSS（杀怪前）', b'\x89\x44\xF7\x04\x5E\x5F',
                0x00080000, 0x00090000, b'\x90\x90\x90\x90'),
            AssemblyItem('raid_boss_after', '无限刷BOSS（杀怪后）', b'\x8B\x44\xF7\x04\x53\x50\xe8',
                0x00850000, 0x00860000, b'', b'\xC7\x44\xF7\x04\x00\x00\x00\x00\x8B\x44\xF7\x04\x53',
                replace_len=5, inserted=True),
            AssemblyItem('ammo_upgrade_mod', '弹药上限升级', b'\xFF\x04\xB0\x8B\x8F\xE0\x00\x00\x00',
                0x003B0000, 0x003C0000, b'',
                AssemblyGroup(b'\x83\xFE\x07\x0F\x84\x14\x00\x00\x00\x83\xFE\x08\x0F\x84\x0B\x00\x00\x00\x8B\x0D',
                    assembly_code.Variable('ammo_upgrade_level'),
                    b'\x01\x0C\xB0\xEB\x03\xFF\x04\xB0\x8B\x8F\xE0\x00\x00\x00'),
                inserted=True, args=(VariableType('ammo_upgrade_level', value=100),)),
            AssemblyItem('super_speed_jump', '超级速度和跳跃', b'\xF3\x0F\x11\x44\x24\x04\xF3\x0F\x10\x43\x08\x8D\x95',
                0x00DF0000, 0x00E00000, b'',
                AssemblyGroup(b'\xF3\x0F\x10\x05', assembly_code.Variable('super_jump_mult'),
                    b'\xF3\x0F\x59\x05', assembly_code.Variable('super_jump_store'),
                    b'\xF3\x0F\x11\x86\xEC\x02\x00\x00\xF3\x0F\x10\x86\xA8\x02\x00\x00',
                    b'\xF3\x0F\x59\x05', assembly_code.Variable('super_speed_mult'),
                    b'\xF3\x0F\x11\x44\x24\x04',),
                inserted=True, replace_len=6, args=(
                    VariableType('super_speed_mult', type=float, value=0x40000000),
                    VariableType('super_jump_mult', type=float, value=0x3FA00000),
                    VariableType('super_jump_store', type=float, value=0x441D8000),
                )),
            AssemblyItem('instant_main_skill_timer', '主动技能冷却时间', b'\x8B\x84\x90\x88\x01\x00\x00\x89\x43\x08',
                0x002B0000, 0x002C0000, b'',
                b'\x8B\x84\x90\x88\x01\x00\x00\x85\xC0\x74\x0C\x83\xFA\x09\x75\x07\xC7\x40\x6C\x00\x00\x00\x00',
                inserted=True, replace_len=7),
            AssemblyItem('mission_timer_freeze', '任务时间锁定', b'\xF3\x0F\x2C\x54\x03\x04\x89\x11',
                0x00EF0000, 0x00F00000, b'',
                AssemblyGroup(b'\xF3\x0F\x2C\x54\x18\x04\x80\x7C\x18\x08\x00\x74\x2E\x83\x3D',
                    assembly_code.Variable('mission_timer_loaded'),
                    b'\x01\x74\x10\x89\x15', assembly_code.Variable('mission_timer_temp'),
                    b'\xC7\x05', assembly_code.Variable('mission_timer_loaded'),
                    b'\x01\x00\x00\x00\xDB\x05', assembly_code.Variable('mission_timer_temp'),
                    b'\xD9\x5C\x18\x04\x8B\x15', assembly_code.Variable('mission_timer_temp'),
                    b'\xE9\x0A\x00\x00\x00\xC7\x05', assembly_code.Variable('mission_timer_loaded'),
                    b'\x00\x00\x00\x00',),
                inserted=True, replace_len=6, args=('mission_timer_loaded', 'mission_timer_temp')),
            AssemblyItem('selected_item', '选中的物品', b'\x8B\x81\xD0\x01\x00\x00\xC3\xCC\xCC',
                0x00EA0000, 0x00EB0000, b'',
                AssemblyGroup(b'\x89\x0D', assembly_code.Variable('selected_item_addr'), b'\x8B\x81\xD0\x01\x00\x00'),
                inserted=True, replace_len=6, args=('selected_item_addr',)),
            AssemblyItem('faster_collecting', '快速收集任务物品', b'\xFF\x04\x99\x8B\x14\x99\x8D\x1C\x99\x89\x55\xFC',
                0x00DA0000, 0x00DB0000, b'',
                b'\x8B\x14\x99\x83\xC2\x05\x3B\x56\x44\x7E\x03\x8B\x56\x44\x89\x14\x99',
                inserted=True, replace_len=6),
            AssemblyItem('enemy_fast_evolution', '敌人快速升级', b'\x8B\x49\x4C\x8B\xC6\x3B\xC8',
                0x00290000, 0x002A0000, b'', b'\x83\xFA\x0B\x75\x04\x8B\xCA\xEB\x03\x8B\x49\x4C\x8B\xC6',
                inserted=True, replace_len=5),
        )
        super().render_assembly_functions(functions)

    def render_assembly_variable(self):
        ModelInput('ammo_upgrade_level', '弹药上限等级')
        ModelInput('super_speed_mult', '超级速度倍数')
        ModelInput('super_jump_mult', '超级跳跃倍数')

    def render_hotkeys(self):
        ui.Text("H: 回复护甲+血量\n"
            "P: 回复推进+血量\n"
            "B: 前进\n"
            "N: 向上\n"
            ";: 弹药全满\n"
            ".: 升级\n"
            "/: 武器等级与人物等级同步(装备中的武器需切到背包再装备)")

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr

    def get_hotkeys(self):
        this = self.weak
        return (
            (0, VK.H, this.pull_through),
            (0, VK.P, this.vehicle_full),
            (0, VK.B, this.go_forward),
            (0, VK.N, this.go_up),
            (VK.MOD_SHIFT, VK.N, this.go_down),
            (0, VK.getCode(';'), this.all_ammo_full),
            (0, VK.getCode('.'), this.level_up),
            (0, VK.getCode('/'), this.sync_weapon_level),
        )

    def _character(self):
        return self._global.mgr.character

    def _character_health(self):
        character = self._character()
        return character and character.health

    def _character_shield(self):
        character = self._character()
        return character and character.shield

    def _experience(self):
        character = self._character()
        return character and character.experience

    def _player_mgr(self):
        return self._global.mgr.player_mgr

    def _player_config(self):
        player_mgr = self._player_mgr()
        return player_mgr and player_mgr.player_config

    def _current_weapon(self):
        player_config = self._player_config()
        weapon = player_config and player_config.current_weapon
        if weapon:
            if not weapon.addr:
                weapon.addr = self.get_variable_value('selected_item_addr', 0)
        return weapon

    def _team_config(self):
        return self._global.mgr.team_config

    def weapon_ammo_max(self, _=None, i=0):
        weapon = self._current_weapon()
        if weapon:
            self._global.mgr.weapon_ammos[i].value_max()

    def pull_through(self):
        health = self._character_health()
        if health:
            health.value_max()
        shield = self._character_shield()
        if shield:
            shield.value_max()

    def go_forward(self):
        player_config = self._player_config()
        if player_config:
            vector = player_config.move_vector.values()
            coord = player_config.coord
            coord += (vector[0] * 5, vector[1] * 5, max(abs(vector[2] * 3), 500))

    def go_up(self):
        player_config = self._player_config()
        if player_config:
            player_config.coord.z += 500

    def go_down(self):
        player_config = self._player_config()
        if player_config:
            player_config.coord.z -= 500

    def vehicle_full(self):
        vehicle_mgrs = self._global.mgr.vehicle_mgrs
        if vehicle_mgrs.addr:
            if vehicle_mgrs[0].addr:
                vehicle_mgrs[0].boost.value_max()
                vehicle_mgrs[0].health.value_max()
            if vehicle_mgrs[1].addr:
                vehicle_mgrs[1].boost.value_max()
                vehicle_mgrs[1].health.value_max()

    def all_ammo_full(self):
        for ammo in self._global.mgr.weapon_ammos:
            ammo.value_max()

    def level_up(self):
        """升级"""
        character = self._character()
        if character:
            character.experience.value = character.exp_next_level

    def sync_weapon_level(self):
        """同步武器等级"""
        character = self._character()
        level = character and character.level
        if level:
            weapon = self._current_weapon()
            if weapon and weapon.addr:
                weapon.set_level(level)

    def read_drop_rates(self, _):
        for _id, key, label in self._drop_rates_table:
            addr = self.handler.find_bytes(_id + self._drop_rates_scan_data, 0x14E00000, 0x18000000, fuzzy=True)
            if addr is -1:
                raise ValueError('找不到地址, ' + label)
            setattr(self._drop_rates, key, addr + 0x20)

    def get_drop_rates_item(self, key):
        addr = getattr(self._drop_rates, key, 0)
        if addr is 0:
            print('未读取地址')
        return addr

    def set_drop_rates_preset(self, _, index):
        for view, value in zip(self._drop_rates_views, self._drop_rates_preset[index][1]):
            view.input_value = value
