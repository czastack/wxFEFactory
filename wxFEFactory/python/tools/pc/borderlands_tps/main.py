import fefactory_api
import types
from functools import partial
from lib.hack.forms import (
    Group, Groups, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelCoordWidget, Input, Title
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from lib import ui
from tools.base.assembly_hacktool import AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType
from tools.base.assembly_code import AssemblyGroup, Variable
from tools.base import assembly_code
from styles import styles
from . import models, datasets


class Main(AssemblyHacktool):
    CLASS_NAME = 'LaunchUnrealUWindowsClient'
    WINDOW_NAME = 'Borderlands: The Pre-Sequel (32-bit, DX9)'

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
        self.lazy_group(Group("team", "团队", team_config, cols=4), self.render_team)
        self.lazy_group(Groups("技能", self.weak.onNotePageChange, addr=team_config), self.render_skill)
        self.lazy_group(Group("drop_rates", "掉落率", None), self.render_drop_rates)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)
        self.lazy_group(Group("assembly_variable", "代码变量", self.variable_model), self.render_assembly_variable)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)

    def render_global(self):
        player_config = (self._player_config, models.PlayerConfig)
        physics_config = (lambda: self._global.mgr.player_mgr.physics_config, models.PhysicsConfig)

        ModelInput('time_scale_multiplier', instance=player_config)
        ModelInput('gravity', instance=player_config)

        ModelInput('move_speed', instance=physics_config)
        ModelInput('jump_height', instance=physics_config)
        ModelInput('friction', instance=physics_config)
        ModelInput('viewing_height', instance=physics_config)

    def render_character(self):
        health = (self._character_health, models.ShieldHealth)
        shield = (self._character_shield, models.ShieldHealth)
        oxygen = (self._character_oxygen, models.ShieldHealth)
        experience = (self._experience, models.Experience)
        player_mgr = (self._player_mgr, models.PlayerManager)

        for label, instance in (('生命', health), ('护甲', shield), ('氧气', oxygen)):
            Title(label)
            ModelInput('value', instance=instance)
            ModelInput('scaled_maximum', instance=instance)
            ModelInput('base_maximum', instance=instance)
            ModelInput('regen_rate', instance=instance)
            ModelSelect('status', instance=instance,
                choices=datasets.STATUS_CHOICES, values=datasets.STATUS_VALUES)

        Title('经验值')
        ModelInput('value', instance=experience)
        ModelInput('scaled_maximum', instance=experience)
        ModelInput('base_maximum', instance=experience)
        ModelInput('multiplier', instance=experience)

        ModelInput('exp_next_level')
        ModelInput('level')
        ModelInput('money')
        ModelInput('moon_shards')
        ModelInput('shift_coins')
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
        ModelInput('ffyl_time_mult', '原地复活生命倍数', instance=player_config)
        ModelInput('ffyl_Health_mult', '原地复活时间倍数', instance=player_config)

    def render_vehicle(self):
        ModelInput('mgr.vehicle_mgrs.0.health.value', '载具1血量')
        ModelInput('mgr.vehicle_mgrs.0.boost.value', '载具1推进')
        ModelInput('mgr.vehicle_mgrs.0.boost.scaled_maximum', '载具1推进最大值')
        ModelCoordWidget('mgr.vehicle_mgrs.0.coord', '载具1坐标', savable=True)
        ModelInput('mgr.vehicle_mgrs.1.health.value', '载具2血量')
        ModelInput('mgr.vehicle_mgrs.1.boost.value', '载具2推进')
        ModelInput('mgr.vehicle_mgrs.1.boost.scaled_maximum', '载具2推进最大值')
        ModelCoordWidget('mgr.vehicle_mgrs.1.coord', '载具1坐标', savable=True)

    def render_ammo(self):
        for i, label in enumerate(('突击步枪子弹', '霰弹枪子弹', '手雷', '冲锋枪子弹', '手枪子弹', '火箭炮弹药', '狙击步枪子弹', '激光子弹')):
            with ModelInput('mgr.weapon_ammos.%d.value' % i, label).container:
                ui.Button(label="最大", class_='btn_sm', onclick=partial(self.weapon_ammo_max, i=i))
            with ModelInput('mgr.weapon_ammos.%d.regen_rate' % i, '恢复速度').container:
                ModelCheckBox('mgr.weapon_ammos.%d.infinite' % i, '不减', alone=True)

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
        ModelInput('calculated_projectiles_per_shot')
        ModelInput('calculated_bullets_used')
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
        ModelInput('ability_cooldown.value', '能力冷却时间')
        ModelInput('ability_cooldown.mult', '能力冷却倍数')

        for i, label in enumerate(datasets.BADASS_BONUSES):
            ModelInput('badass_bonuses.%d' % i, label).set_help('100% = 464, 200% = 1169, Max = 8388607')

    def render_skill(self):
        with Group('ability', "主技能"):
            ModelInput('skill_mgr.ability_status', '主技能状态')
            ModelInput('skill_mgr.ability_duration', '主技能持续时间')

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
            (b'\x2D', 'very_common', '药'),
            (b'\x2F', 'common', '白'),
            (b'\x32', 'uncommon', '绿'),
            (b'\x33', 'very_uncommon', '月'),
            (b'\x34', 'rare', '蓝'),
            (b'\x35', 'very_rare', '紫'),
            (b'\x36', 'legendary', '橙/珠光')
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
        with ui.Horizontal(class_='expand'):
            ui.Button('读取地址', onclick=self.read_drop_rates)
            for i, item in enumerate(self._drop_rates_preset):
                ui.Button(item[0], class_='btn_md', onclick=partial(self.set_drop_rates_preset, index=i))
        self._drop_rates_views = [Input(key, label, addr=partial(__class__.get_drop_rates_item, self.weak, key=key),
            type=float) for _id, key, label in self._drop_rates_table]

    def render_assembly_functions(self):
        super().render_assembly_functions((
            AssemblyItem('ammo_inf', '子弹不减+精准不减', b'\xF3\x0F\x58\x45\x08\x51',
                0x005C0000, 0x008D0000, b'',
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
                # old: 0x00460000, 0x00470000,
                # steam
                0x00050000, 0x00060000,
                b'', b'\x8B\x02\x89\x02\x8B\xE5\x5D',
                inserted=True, replace_len=5, replace_offset=7),
            AssemblyItem('no_recoil', '无后坐力', b'\xF3\x0F\x2C\x8F\x98\x0F\x00\x00\x01\x0E',
                0x009D0000, 0x00CE0000, b'',
                b'\x31\xC9\x89\x8F\x94\x0F\x00\x00\x89\x8F\x98\x0F\x00\x00\x89\x8F\x9C\x0F\x00\x00'
                    b'\x89\x8F\xA0\x0F\x00\x00\x89\x8F\xA4\x0F\x00\x00\x89\x8F\xA8\x0F\x00\x00',
                inserted=True, replace_len=8),
            AssemblyItem('without_golden_keys', '无需金钥匙', b'\x74\x1D\x8A\x54',
                # old: 0x00440000, 0x00450000,
                # steam
                0x00B40000, 0x00B50000,
                b'\xEB\x1D\x8A\x54'),
            AssemblyItem('ammo_upgrade_mod', '弹药上限升级', b'\xFF\x04\xB0\x8B\x8F\xE0\x00\x00\x00',
                0x009FF000, 0x00C10000, b'',
                AssemblyGroup(b'\x83\xFE\x07\x0F\x84\x14\x00\x00\x00\x83\xFE\x08\x0F\x84\x0B\x00\x00\x00\x8B\x0D',
                    assembly_code.Variable('ammo_upgrade_level'),
                    b'\x01\x0C\xB0\xEB\x03\xFF\x04\xB0\x8B\x8F\xE0\x00\x00\x00'),
                inserted=True, args=(VariableType('ammo_upgrade_level', value=100),)),
            AssemblyItem('mission_timer_freeze', '任务时间锁定', b'\xF3\x0F\x2C\x54\x03\x04\x89\x11',
                0x00A50000, 0x00DF0000, b'',
                AssemblyGroup(b'\xF3\x0F\x2C\x54\x18\x04\x80\x7C\x18\x08\x00\x74\x2E\x83\x3D',
                    assembly_code.Variable('mission_timer_loaded'),
                    b'\x01\x74\x10\x89\x15', assembly_code.Variable('mission_timer_temp'),
                    b'\xC7\x05', assembly_code.Variable('mission_timer_loaded'),
                    b'\x01\x00\x00\x00\xDB\x05', assembly_code.Variable('mission_timer_temp'),
                    b'\xD9\x5C\x18\x04\x8B\x15', assembly_code.Variable('mission_timer_temp'),
                    b'\xE9\x0A\x00\x00\x00\xC7\x05', assembly_code.Variable('mission_timer_loaded'),
                    b'\x00\x00\x00\x00',),
                inserted=True, replace_len=6, args=('mission_timer_loaded', 'mission_timer_temp')),
            AssemblyItems('选中的物品',
                AssemblyItem('selected_gun', None, b'\x8B\x8F\x78\x0E\x00\x00\x33',
                    0x00B8F000, 0x00E00000, b'',
                    AssemblyGroup(b'\x8B\x8F\x78\x0E\x00\x00\x89\x3D', assembly_code.Variable('selected_item_addr')),
                    inserted=True, replace_len=6, args=('selected_item_addr',)),
                AssemblyItem('selected_item', None, b'\x8B\x81\xA4\x08\x00\x00\x85\xC0\x74\x14',
                    0x00A40000, 0x00C50000, b'',
                    AssemblyGroup(b'\x8B\x81\xA4\x08\x00\x00\x89\x0D', assembly_code.Variable('selected_item_addr')),
                    inserted=True, replace_len=6, args=('selected_item_addr',))),
            # AssemblyItem('no_equip_level_limit', '解除装备等级限制', b'\x8B\x80\x58\x02\x00\x00\x5F\x5E\xC3',
            #     0x00830000, 0x00840000, b'\x90\x90\x90\x90\x90\x90', replace_len=6),
            AssemblyItem('no_unique_weapon_spreadfire_patterns', '无扩散', b'\x99\xF7\xFE\x8B\xC1\x89\x17',
                0x00C00000, 0x00D10000, b'', b'\x99\xF7\xFE\x8B\xC1\xC7\x07\x00\x00\x00\x00',
                inserted=True, replace_len=8),
            AssemblyItem('free_world_usage', '免费世界使用', b'\x8B\x44\x81\x60\x8B\x4D\x14',
                0x00440000, 0x00B50000, b'', b'\xB8\x00\x00\x00\x00\x8B\x4D\x14', inserted=True),
            AssemblyItem('free_moxi_drinks', '免费喝酒', b'\x8B\x81\xDC\x00\x00\x00\x8B\x4D\x10',
                0x00680000, 0x00C00000, b'\xB8\x00\x00\x00\x00\x90', replace_len=6),
            AssemblyItem('unlimited_moxi_drink_duration', '无限喝酒时长', b'\xF3\x0F\x11\x8E\xBC\x10\x00\x00',
                # old: 0x00090000, 0x000A0000,
                # steam
                0x00C00000, 0x00D00000,
                b'\x90\x90\x90\x90\x90\x90\x90\x90'),
            AssemblyItem('infinite_double_jump', '无限二段跳', b'\x8B\x8B\x98\x0B\x00\x00\xC1\xE9\x09',
                0x00B00000, 0x00ED0000, b'', b'\x8B\x8B\x98\x0B\x00\x00\xC6\x83\x99\x0B\x00\x00\x10',
                inserted=True, replace_len=6),
            AssemblyItem('no_backpack_pickup_limit', '解除背包限制', b'\x8B\x81\x00\x02\x00\x00\xC3\xCC\xCC',
                0x00790000, 0x00C00000, b'\xB8\x00\x00\x00\x00\x90', replace_len=6),
        ))

    def render_assembly_variable(self):
        ModelInput('ammo_upgrade_level', '弹药上限等级')
        ModelInput('super_speed_mult', '超级速度倍数')
        ModelInput('super_jump_mult', '超级跳跃倍数')

    def render_hotkeys(self):
        ui.Text("H: 回复护甲+血量\n"
            "P: 回复载具推进+血量\n"
            "B: 前进\n"
            "N: 向上\n"
            "Shift+N: 向下\n"
            "F3: 切换2倍移动速度\n"
            ";: 弹药全满\n"
            ".: 升级\n"
            "': 当前武器高精准，高射速\n"
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
            (0, VK.X, this.current_ammo_full),
            (VK.MOD_SHIFT, VK.N, this.go_down),
            (VK.MOD_ALT, VK.F, this.ability_cooldown),
            (0, VK.F3, this.move_quickly),
            (0, VK.getCode(';'), this.all_ammo_full),
            (0, VK.getCode('.'), this.level_up),
            (0, VK.getCode("'"), this.make_weapon_useful),
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

    def _character_oxygen(self):
        character = self._character()
        return character and character.oxygen

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
        oxygen = self._character_oxygen()
        if oxygen:
            oxygen.value_max()

    def vehicle_full(self):
        vehicle_mgrs = self._global.mgr.vehicle_mgrs
        if vehicle_mgrs.addr:
            if vehicle_mgrs[0].addr:
                vehicle_mgrs[0].boost.value_max()
                vehicle_mgrs[0].health.value_max()
            if vehicle_mgrs[1].addr:
                vehicle_mgrs[1].boost.value_max()
                vehicle_mgrs[1].health.value_max()

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

    def current_ammo_full(self):
        weapon = self._current_weapon()
        if weapon.addr:
            weapon.ammo.value_max()

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

    def make_weapon_useful(self):
        weapon = self._current_weapon()
        if weapon and weapon.addr:
            weapon.base_accuracy = 0.1
            weapon.base_fire_rate = 0.1 if weapon.base_fire_rate < 0.2 else 0.2

    def move_quickly(self):
        config = self._player_config()
        if config and config.addr:
            config.move_speed_mult = 2 if config.move_speed_mult == 1 else 1

    def ability_cooldown(self):
        """技能冷却"""
        team_config = self._team_config()
        if team_config:
            team_config.ability_cooldown.value = 0

    def read_drop_rates(self, _):
        for _id, key, label in self._drop_rates_table:
            addr = self.handler.find_bytes(_id + self._drop_rates_scan_data, 0x1B000000, 0x1E000000, fuzzy=True)
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
