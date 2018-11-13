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

    def render_main(self):
        character = (self._character, models.Character)
        # weapon = (self._current_weapon, models.Weapon)

        with Group("global", "全局", self._global):
            self.render_global()
        self.lazy_group(Group("character", "角色", character, cols=4), self.render_character)
        self.lazy_group(Group("ammo", "弹药", character, cols=4), self.render_ammo)
        self.lazy_group(Group("weapon_prof", "武器熟练度", self._global, cols=4), self.render_weapon_prof)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)

    def render_global(self):
        another_mgr = (lambda: self._global.another_mgr, models.AnotherManager)

        ModelInput('move_speed', instance=another_mgr)

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

        Title('能力冷却')
        ModelInput('value', instance=ability_cooldown)
        ModelInput('scaled_maximum', instance=ability_cooldown)
        ModelInput('base_maximum', instance=ability_cooldown)

        ModelInput('level', instance=character_config)
        ModelInput('money', instance=character_config)
        ModelInput('skill_points', instance=character_config)

    def render_ammo(self):
        for i, label in enumerate(('狙击枪', '手枪', '手雷', '左轮手枪', '冲锋枪', '霰弹枪', '战斗步枪', '火箭筒')):
            with ModelInput('weapon_ammos.%d.value' % i, label).container:
                ui.Button(label="最大", className='btn_sm', onclick=partial(self.weapon_ammo_max, i=i))
            ModelInput('weapon_ammos.%d.regen_rate' % i, '恢复速度')

    def render_weapon_prof(self):
        for i, label in enumerate(('手枪', '冲锋枪', '霰弹枪', '战斗步枪', '狙击枪', '火箭筒', '外星枪')):
            ModelInput('another_mgr.weapon_profs.%d.level' % i, '%s等级' % label)
            ModelInput('another_mgr.weapon_profs.%d.exp' % i, '经验')

    def render_assembly_functions(self):
        functions = (
            AssemblyItem('accuracy_keep', '精准度不减', b'\xF3\x0F\x10\x40\x68\xF3\x0F\x11\x44\x24\x08',
                0x008D0000, 0x008F0000, b'\x0F\x57\xC0\x90\x90'),
            AssemblyItem('rapid_fire', '快速射击', b'\xF3\x0F\x10\x81\x94\x02\x00\x00\x0F\x2F',
                0x00330000, 0x00340000, b'\x0F\x57\xC0\x90\x90\x90\x90\x90'),
            AssemblyItem('no_recoil', '无后坐力', b'\xF3\x0F\x10\x8B\xD8\x0B\x00\x00\xF3\x0F\x10\x83\xD4\x0B\x00\x00',
                0x010C0000, 0x010D0000, b'\x0F\x57\xC0\x0F\x57\xC9' + b'\x90' * 10),
            AssemblyItem('no_reload', '无需换弹', b'\x2B\x86\xCC\x03\x00\x00\x39\x86\x90\x03\x00\x00',
                0x01130000, 0x01140000, b'',
                b'\xC7\x86\xCC\x03\x00\x00\x63\x00\x00\x00',
                inserted=True, replace_len=6),
        )
        super().render_assembly_functions(functions)

    def render_hotkeys(self):
        ui.Text("H: 回复护甲+血量\n"
            ";: 弹药全满\n")

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr

    def get_hotkeys(self):
        this = self.weak
        return (
            (0, VK.H, this.pull_through),
            (0, VK.getCode(';'), this.all_ammo_full),
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

    def all_ammo_full(self):
        ammos = self._weapon_ammos()
        if ammos:
            for ammo in ammos:
                ammo.value_max()
