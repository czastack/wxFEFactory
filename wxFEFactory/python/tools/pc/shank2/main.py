from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.hack.handlers import MemHandler
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, Delta
)
# from . import models


class Main(AssemblyHacktool):
    CLASS_NAME = 'Shank 2'
    WINDOW_NAME = 'Shank 2'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        # self._global = models.Global(0, self.handler)

    def render_main(self):
        # with Group("global", "全局", self._global):
        #     pass
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_assembly_buttons_own(self):
        delta = Delta(0x10000)
        self.render_assembly_buttons((
            AssemblyItem(
                'inf_health', '无限生命', 'D8 9B A0 00 00 00 DF E0 F6 C4 01', 0x000F1000, delta, b'',
                '81 BB A0000000 0000803F7E 16  81 BB A0000000 0000F0427F 0A  C7 83 A0000000 0000F042D8 9B A0000000',
                inserted=True, replace_len=6),
            AssemblyItem(
                'inf_score', '无限点数', '8B 40 50 8B E5 5D',
                0x0000E000, delta, b'', 'C7 40 50 7F969800  8B 40 50  8B E5',
                inserted=True, replace_len=5),
            AssemblyItem(
                'inf_grenade', '无限爆炸物', '89 4D FC 8B 45 FC 8B 40 4C 8B E5',
                0x00074000, delta, b'', 'C7 40 4C 05000000  8B 40 4C  8B E5',
                inserted=True, replace_len=5, replace_offset=6),
            AssemblyItem(
                'inf_combo', '无限连击', '89 77 24 85 F6 74', 0x000F2000, delta, b'',
                '83 7F 24 04  7C 0E  81 7F 24 0F270000  7D 05  BE 0F270000  89 77 24  85 F6',
                inserted=True, replace_len=5),
            AssemblyItem(
                'no_overheating', '机枪不会过热', 'D9 58 10 C2 08 00', 0x00082000, delta, b'',
                '81 78 10 0000A040  7C 0C  D9 58 10  C7 40 10 00000000  EB 03  D9 58 10  C2 0800',
                inserted=True, replace_len=6),
            AssemblyItems(
                '2倍分数',
                AssemblyItem(
                    'score_mult_1_1', None, '01 57 50 8D 44 24 44', 0x000D5000, delta,
                    b'', 'C1 E2 01  01 57 50  8D 44 24 44', inserted=True),
                AssemblyItem(
                    'score_mult_1_2', None, '8B 4E 08 01 7E 50', 0x000D6000, delta,
                    b'', '8B 4E 08  C1 E7 01  01 7E 50', inserted=True),
            ),
            AssemblyItems(
                '4倍分数',
                AssemblyItem(
                    'score_mult_2_1', None, '01 57 50 8D 44 24 44', 0x000D5000, delta,
                    b'', 'C1 E2 02  01 57 50  8D 44 24 44', inserted=True),
                AssemblyItem(
                    'score_mult_2_2', None, '8B 4E 08 01 7E 50', 0x000D6000, delta,
                    b'', '8B 4E 08  C1 E7 02  01 7E 50', inserted=True),
            ),
        ))
