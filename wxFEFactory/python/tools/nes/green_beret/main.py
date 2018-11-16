from ..base import BaseNesHack
from lib.hack.forms import Group, StaticGroup, ModelInput, ModelSelect
from lib.hack.models import Model, Field, ByteField, ArrayField
from lib import utils


class Player(Model):
    SIZE = 0x20
    invincible = ByteField(0x050C, label='金身无敌')
    weapon = ByteField(0x051D, label='武器')
    ammo = ByteField(0x051C, label='武器数量')
    nocollision = ByteField(0x0500, label='撞人不死')
    fly = ByteField(0x050A, label='可飞天')


class Global(Model):
    p1_lives = ByteField(0x0022, label='P1人数')
    p2_lives = ByteField(0x0023, label='P2人数')


WEAPONS = ('无', 'RPG', '手雷', '星', '手枪')


class Main(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)
        self.p1 = Player(0, self.handler)
        self.p2 = Player(0x20, self.handler)

        with Group("global", "全局", self._global):
            ModelInput('p1_lives')
            ModelInput('p2_lives')

        for key in ('p1', 'p2'):
            with Group(key, key, getattr(self, key)):
                ModelInput('invincible')
                ModelSelect('weapon', choices=WEAPONS)
                ModelInput('ammo')
                ModelInput('nocollision')
                ModelInput('fly')
