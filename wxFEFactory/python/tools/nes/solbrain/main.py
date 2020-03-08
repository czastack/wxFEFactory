from lib.hack.forms import Group, StaticGroup, ModelInput, ModelSelect
from lib.hack.models import Model, Field, ByteField, WordField, MulFieldPrep
from lib import utils
from ..base import BaseNesHack


class Global(Model):
    invincible = ByteField(0x05A3)
    hp = ByteField(0x05C5)
    helper_hp = ByteField(0x06FC)
    p = MulFieldPrep(10, WordField(0x05C6))
    powerup = ByteField(0x05C8)
    highjump = ByteField(0x05EA)
    gun = ByteField(0x05C2)
    fire_helper = ByteField(0x065C)
    own_helper = ByteField(0x060C)
    form = ByteField(0x05C4)
    lives = ByteField(0x071C)
    level = ByteField(0x0055)


FORMS = (
    (0x15, "ααα"),
    (0x16, "βαα"),
    (0x19, "αβα"),
    (0x1a, "ββα"),
    (0x25, "ααβ"),
    (0x26, "βαβ"),
    (0x29, "αββ"),
    (0x2a, "βββ"),
)
FORM_LABELS, FORM_VALUES = utils.split_tuple_reverse(FORMS)


class Main(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("hp", "血量(max:8)")
            ModelInput("helper_hp", "助手血量(max:16)")
            ModelInput("lives", "生命(max:9)")
            ModelInput("powerup_2", "威力加强(max:3)")
            ModelInput("fire_helper", "喷火助手(4)")
            ModelInput("own_helper", "拥有助手(4)")
            ModelInput("level", "关卡")
            ModelInput("invincible", "无敌时间(max:73)")
            ModelInput("powerup", "威力加强(max:100)")
            ModelInput("p", "P")
            ModelInput("highjump", "高跳(max:255)")
            ModelInput("ammo", "枪形态时间(max:255)")
            ModelSelect("form", "形态", choices=FORM_LABELS, values=FORM_VALUES)
