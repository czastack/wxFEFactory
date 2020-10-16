from tools.base.assembly_hacktool import (
    AssemblyItem, AssemblyItems, Delta, VariableType, VariableSwitch, VariableRadio
)
from tools.base.assembly_code import AssemblyGroup, Cmp, Offset, Variable, ForwardCall, ORIGIN

ADDRESS_SOURCES = {
    'hack': {
        'health_base_1': 0x0025B000,
        'health_base_2': 0x0026A000,
        'inf_ammo': 0x00431000,
        'no_reload': 0x0042E000,
        'accuraty_rapid': 0x00429000,
        'no_recoil': 0x00435000,
        'inf_hold_time': 0x00425000,
        'speed_base': 0x00353000,
    },
    'steam': {}
}


delta = Delta(0x20000)

ASSEMBLY_ITEMS = (
    AssemblyItems(
        '玩家地址依赖',
        AssemblyItem(
            'health_base_1', None, '8B 87 84 01 00 00 89 83 DC 01 00 00', None, delta, b'',
            AssemblyGroup('48 89 3D', Offset('character_addr'), '8B 87 84 01 00 00'),
            inserted=True,
            replace_len=6,
            args=(
                'inf_health',
                'b_one_hit_kill',
                VariableType('character_addr', size=8),
            )),
        AssemblyItem(
            'health_base_2', None, '2B C6 89 87 84 01 00 00',
            None, delta, b'',
            AssemblyGroup(
                '53 48 BB',
                Variable('character_addr'),
                '48 39 3B 75 0D',
                Cmp('inf_health', 1),
                '75 12 31 F6 EB 0E',
                Cmp('b_one_hit_kill', 1),
                '75 05 BE 7F969800 5B 29 F0 89 87 84010000'
            ),
            inserted=True, replace_len=8),
    ),
    VariableSwitch('inf_health', '无限生命', depends=('health_base_1',)),
    VariableSwitch('b_one_hit_kill', '一击必杀', depends=('health_base_1',)),
    AssemblyItem(
        'inf_ammo', '无限子弹', '01 58 08 48 8B 5C 24 08', None, delta,
        b'', 'C7 40 08 E7 03 00 00 48 8B 5C 24 08', inserted=True),
    AssemblyItem(
        'no_reload', '无需装弹+手雷不减', '29 7C 88 08 48 8B 5C 24 30', None, delta, '90 90 90 90', replace_len=4),
    AssemblyItem(
        'accuraty_rapid', '超级精准度+快速射击依赖', 'F3 0F 58 83 A0 03 00 00 F3 0F',
        None, delta, b'',
        AssemblyGroup(
            Cmp('b_perfect_accuraty', 1),
            '75 0B 0F57 C0 F3 0F11 83 A0030000',
            Cmp('b_rapid_fire', 1),
            '75 07 83 A3 98020000 00 F3 0F58 83 A0030000'
        ),
        inserted=True,
        replace_len=8,
        hidden=True,
        args=('b_perfect_accuraty', 'b_rapid_fire')),
    VariableSwitch('b_perfect_accuraty', '超级精准度', depends=('accuraty_rapid',)),
    VariableSwitch('b_rapid_fire', '快速射击', depends=('accuraty_rapid',)),
    AssemblyItem(
        'no_recoil', '无后坐力', 'F3 0F 11 0C 0B 0F 28 D9', None, delta,
        b'', '0F 57 C9 F3 0F 11 0C 0B', inserted=True, replace_len=5),
    AssemblyItem(
        'inf_hold_time', '无限屏息时间', '01 B3 44 02 00 00', None, delta,
        b'', '83 A3 44 02 00 00 00', inserted=True),

    AssemblyItem(
        'speed_base', '速度依赖', 'F3 0F 10 58 10 0F 2E D8', None, delta, b'',
        AssemblyGroup(
            Cmp('game_speed', 0xFF),
            '74 29',
            Cmp('game_speed', 0),
            '74 0F',
            'F3 0F10 1D', Offset('game_speed'),
            'F3 0F11 58 10 EB 11 C7 40 10 0000803F',
            'C7 05', Offset('game_speed', size=8), 'FFFFFFFF'
            'F3 0F10 58 10'
        ),
        inserted=True,
        args=(
            VariableType('game_speed', type=float, value=0),
        ),
        replace_len=5),
    VariableRadio(
        'super_speed', '超级速度', variable='game_speed', enable_value=2.5, disable_value=0, depends=('speed_base',)),
    VariableRadio(
        'bullet_time', '子弹时间', variable='game_speed', enable_value=0.3, disable_value=0, depends=('speed_base',)),
)
