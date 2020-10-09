from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, Delta, AssemblySwitch
)
from tools.base.assembly_code import AssemblyGroup, ORIGIN, Offset, Cmp, Variable
from . import models


class Main(AssemblyHacktool):
    CLASS_NAME = 'TalesOfVesperiaClass'
    WINDOW_NAME = 'Tales of Vesperia Definitive Edition'

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            self.render_global()
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_global(self):
        ModelInput("money_multi_value", "金钱倍数", instance=self.variable_model)
        ModelInput("exp_multi_value", "经验倍数", instance=self.variable_model)

    def render_assembly_buttons_own(self):
        delta = Delta(0x10000)
        self.render_assembly_buttons((
            AssemblyItem(
                'inf_health_base', '无限生命/无限TP', 'FF C8 83 F8 08 0F 87 * 00 00 00 BA 16 00 00 00',
                0x005C6000, delta, b'',
                AssemblyGroup(
                    'FF C8 83 F8 08 77 1E',
                    Cmp('b_inf_health', 1),
                    '75 06 8B 46 54 89 46 4C',
                    Cmp('b_inf_tp', 1),
                    '75 06 8B 46 58 89 46 50 83 F8 08'
                ),
                args=('b_inf_health', 'b_inf_tp'),
                inserted=True, replace_len=5, hidden=True, fuzzy=True),
            AssemblySwitch('b_inf_health', '无限生命', depends=('inf_health_base')),
            AssemblySwitch('b_inf_tp', '无限TP', depends=('inf_health_base')),
            AssemblyItem(
                'item_keep', '物品不减', '41 8B D8 8B 7C 81 38',
                0x005B9000, delta, b'', '8B 7C 81 38 41 83 F8 00 7D 0A 8B DF 44 01 C3 7E 03 44 29 C7 41 8B D8',
                inserted=True, replace_len=7),
            AssemblyItem(
                'item_no_cd', '物品立即冷却', 'F3 0F 58 49 08 F3 0F 10 41 0C',
                0x00505000, delta, '0F 57 C9', replace_len=5),
            AssemblyItem(
                'drop_rate_100p', '100%掉宝率', '89 86 50 01 00 00 8B 86 F8 00 00 00',
                0x005C5000, delta, b'', '83 7E 44 00 74 0B 83 7E 44 08 77 05 B8 40 42 0F 00 89 86 50 01 00 00',
                inserted=True, replace_len=6),
            AssemblyItem(
                'inf_sp', '无限SP', '39 B3 F8 24 00 00 7D 04',
                0x005C9000, delta, b'', 'C7 83 F8 24 00 00 9F 86 01 00 39 B3 F8 24 00 00',
                inserted=True, replace_len=6),
            AssemblyItem(
                'full_extremity', '满极限突破槽', 'F3 0F 58 91 58 3C 00 00 F3 0F 11 91 58 3C 00 00',
                0x005BB000, delta, 'C7 81 58 3C 00 00 00 00 48 44 EB 0D 90 90 90 90'),
            AssemblyItem(
                'one_hit_kill', '一击必杀', '89 46 58 8B 46 6C',
                0x005C5000, delta, b'', '89 46 58 8B 46 6C 83 7E 44 00 74 0B 83 7E 44 08 77 05 05 20 4E 00 00',
                inserted=True, replace_len=6),

            AssemblyItem(
                'extremity_base', '无限极限突破持续时间/最高极限突破等级', 'F3 0F 58 89 70 40 00 00',
                0x005CA000, delta, b'',
                AssemblyGroup(
                    '53 48 8D 99 70400000',
                    Cmp('b_inf_extremity_time', 1),
                    '75 03 0F57 C9',
                    Cmp('b_extremity_level', 1),
                    '75 12 83 3B 00 7E 0D 83 7B 04 00 7E 07 C7 43 04 04000000 F3 0F58 0B 5B',
                ),
                args=('b_inf_extremity_time', 'b_extremity_level'),
                inserted=True, replace_len=8, hidden=True),
            AssemblySwitch('b_inf_extremity_time', '无限极限突破持续时间', depends=('extremity_base')),
            AssemblySwitch('b_extremity_level', '最高极限突破等级', depends=('extremity_base')),
            AssemblyItem(
                'save_anytime', '随时存档', '84 C0 8D 4F 07 0F 45 DF',
                0x003C0000, delta, '0C 01', replace_len=2),

            AssemblyItem(
                'money_multi', '金钱倍数', '01 51 30 48 8B D9', 0x005B9000, delta, b'',
                AssemblyGroup(
                    '83 FA 00 7E 10',
                    Cmp('money_multi_value', 0),
                    '74 07 0FAF 15',
                    Offset('money_multi_value'),
                    '01 51 30 48 8B D9',
                ),
                args=('money_multi_value',),
                inserted=True, replace_len=6),

            AssemblyItem(
                'exp_multi', '经验倍数', '8B 49 60 03 CA 3B C8', 0x005C7000, delta, b'',
                AssemblyGroup(
                    '8B 49 60',
                    Cmp('b_inf_exp', 1),
                    '75 04 8B C8 EB 10',
                    Cmp('exp_multi_value', 0),
                    '74 07 0FAF 15',
                    Offset('exp_multi_value'),
                    '01 D1',
                ),
                args=('exp_multi_value', 'b_inf_exp'),
                inserted=True, replace_len=5),
            AssemblySwitch('b_inf_exp', '无限经验', depends=('exp_multi')),
            AssemblyItem(
                'inf_lp', '无限LP/快速学习技能', 'B8 1F 85 EB 51 F7 E1 48 8B CF C1 EA 05',
                0x00496000, delta, b'', '48 8B CF BA 40 42 0F 00',
                inserted=True, replace_len=6, replace_offset=7),
        ))
