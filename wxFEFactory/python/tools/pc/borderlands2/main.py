from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelCoordWidget, Title
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.assembly_hacktool import AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch
from tools.assembly_code import AssemblyGroup, Variable
from tools import assembly_code
from fefactory_api import ui
from styles import styles
from . import models, datasets
import fefactory_api


class Main(AssemblyHacktool):
    CLASS_NAME = 'LaunchUnrealUWindowsClient'
    WINDOW_NAME = 'Borderlands 2 (32-bit, DX9)'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)

    def render_main(self):
        character = (self._character, models.Character)

        with Group("global", "全局", self._global):
            self.render_global()
        self.lazy_group(Group("character", "角色", character, cols=4), self.render_character)
        self.lazy_group(Group("character_ext", "角色额外", character), self.render_character_ext)
        self.lazy_group(Group("ammo", "弹药", self._global), self.render_ammo)
        self.lazy_group(Group("weapon", "武器", (self._current_weapon, models.Weapon)), self.render_weapon)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)

    def render_global(self):
        pass

    def render_character(self):
        health = (self._character_health, models.ShieldHealth)
        shield = (self._character_shield, models.ShieldHealth)
        experience = (self._experience, models.Experience)

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
        ModelInput('to_next_level', instance=experience)

        ModelInput('level')
        ModelInput('money')
        ModelInput('eridium')
        ModelInput('seraph_crystals')
        ModelInput('torgue_tokens')
        ModelInput('skill_points')

    def render_character_ext(self):
        player_config = (self._player_config, models.PlayerConfig)
        ModelCoordWidget('coord', instance=player_config, savable=True)

    def render_ammo(self):
        ModelInput('mgr.weapon_mgrs.0.ammo', '突击步枪子弹')
        ModelInput('mgr.weapon_mgrs.1.ammo', '霰弹枪子弹')
        ModelInput('mgr.weapon_mgrs.2.ammo', '手雷')
        ModelInput('mgr.weapon_mgrs.3.ammo', '冲锋枪子弹')
        ModelInput('mgr.weapon_mgrs.4.ammo', '手枪子弹')
        ModelInput('mgr.weapon_mgrs.5.ammo', '火箭炮弹药')
        ModelInput('mgr.weapon_mgrs.6.ammo', '狙击步枪子弹')

    def render_weapon(self):
        ModelInput('actual_level')
        ModelInput('base_damage')
        ModelInput('base_accuracy')
        ModelInput('base_fire_rate')
        ModelInput('base_projectile_speed')
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
            AssemblyItems('无需换弹+精准不减',
                AssemblyItem('ammo_inf', None, b'\xF3\x0F\x58\x45\x08\x51',
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
                    inserted=True, replace_len=5, args=(('fxbuff', 512), ('minus_one', 4, 0xBF800000))),
                AssemblyItem('ammo_inf2', None, b'\x3B\xC1\x7C\x0B\x8B\x55\x0C\x89\x02\x8B\xE5\x5D\xC2\x08\x00',
                    0x002A0000, 0x002B0000, b'', b'\x8B\x02\x89\x02\x8B\xE5\x5D',
                    inserted=True, replace_len=5, replace_offset=7)),
            AssemblyItem('no_recoil', '无后坐力', b'\xF3\x0F\x2C\x8F\x10\x0E\x00\x00',
                0x001A0000, 0x001B0000, b'',
                b'\x83\x3D\x3B\x00\x37\x3E\x01\x75\x25\x31\xC9\x89\x8F\x0C\x0E\x00\x00\x89\x8F\x10\x0E\x00\x00'
                b'\x89\x8F\x14\x0E\x00\x00\x89\x8F\x18\x0E\x00\x00\x89\x8F\x1C\x0E\x00\x00\xE9\xD1\x64\xE9\xC2'
                b'\xF3\x0F\x2C\x8F\x10\x0E\x00\x00',
                inserted=True, replace_len=5),
            AssemblyItem('without_golden_keys', '无需金钥匙', b'\x74\x1D\x8A\x54',
                0x00500000, 0x00510000, b'\xEB\x1D\x8A\x54'),
            AssemblyItem('raid_boss_before', '无限刷BOSS（杀怪前）', b'\x89\x44\xF7\x04\x5E\x5F',
                0x00080000, 0x00090000, b'\x90\x90\x90\x90'),
        )
        super().render_assembly_functions(functions)

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr

    def get_hotkeys(self):
        this = self.weak
        return (
            (0, VK.H, this.pull_through),
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

    def _player_config(self):
        return self._global.mgr.player_mgr.player_config

    def _current_weapon(self):
        player_config = self._player_config()
        return player_config and player_config.current_weapon

    def pull_through(self):
        self.toggle_assembly_button('health_inf')
