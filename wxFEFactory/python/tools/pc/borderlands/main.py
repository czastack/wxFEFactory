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
        self.lazy_group(Group("ammo", "弹药", self._global, cols=4), self.render_ammo)
        self.lazy_group(Group("weapon_prof", "武器熟练度", self._global, cols=4), self.render_weapon_prof)

    def render_global(self):
        another_mgr = (lambda: self._global.another_mgr, models.AnotherManager)

        ModelInput('move_speed', instance=another_mgr)

    def render_character(self):
        health = (self._character_health, models.Value)
        shield = (self._character_shield, models.Value)
        experience = (self._experience, models.Value)
        ability_cooldown = (self._ability_cooldown, models.Value)
        character_config = (lambda: self._global.mgr.play_mgr.character_config, models.CharacterConfig)

        Title('生命')
        ModelInput('value', instance=health)
        ModelInput('scaled_maximum', instance=health)
        ModelInput('base_maximum', instance=health)
        # ModelInput('regen_rate', instance=health)
        # ModelSelect('status', instance=health,
        #     choices=datasets.SHIELD_HEALTH_STATUS_CHOICES, values=datasets.SHIELD_HEALTH_STATUS_VALUES)

        Title('护甲')
        ModelInput('value', instance=shield)
        ModelInput('scaled_maximum', instance=shield)
        ModelInput('base_maximum', instance=shield)
        # ModelInput('regen_rate', instance=shield)
        # ModelSelect('status', instance=shield,
        #     choices=datasets.SHIELD_HEALTH_STATUS_CHOICES, values=datasets.SHIELD_HEALTH_STATUS_VALUES)

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
        for i, label in enumerate(('狙击枪', '连发枪', '手雷', '左轮手枪', '冲锋枪', '霰弹枪', '战斗步枪', '火箭筒')):
            with ModelInput('mgr.play_mgr.character.weapon_ammos.%d.value' % i, label).container:
                ui.Button(label="最大", className='btn_sm', onclick=partial(self.weapon_ammo_max, i=i))
            ModelInput('mgr.play_mgr.character.weapon_ammos.%d.regen_rate' % i, '恢复速度')

    def render_weapon_prof(self):
        for i, label in enumerate(('手枪', '冲锋枪', '霰弹枪', '战斗步枪', '狙击枪', '火箭筒', '外星枪')):
            ModelInput('another_mgr.weapon_profs.%d.level' % i, '%s等级' % label)
            ModelInput('another_mgr.weapon_profs.%d.exp' % i, '经验')

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr

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

    def weapon_ammo_max(self, _=None, i=0):
        weapon = self._current_weapon()
        if weapon:
            self._global.mgr.weapon_ammos[i].value_max()
