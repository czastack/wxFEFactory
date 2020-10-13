from tools.base.assembly_hacktool import (
    AssemblyItem, AssemblyItems, Delta, VariableType, VariableSwitch, VariableRadio
)
from tools.base.assembly_code import AssemblyGroup, Cmp, Offset, Variable, ForwardCall, ORIGIN

ADDRESS_SOURCES = {
    'hack': {
        'health_base_1': 0x004AD000,
        'health_base_2': 0x004BE000,
        'no_hurt_base': 0x004BD000,
        'inf_ammo': 0x006A2000,
        'no_reload': 0x00699000,
        'inf_grenades': 0x0069A000,
        'perfect_accuraty': 0x0069A000,
        'rapid_fire': 0x0069C000,
        'no_recoil': 0x003B8000,
        'speed_base': 0x005A4000,
    },
    'steam': {}
}


delta = Delta(0x20000)

ASSEMBLY_ITEMS = (
    AssemblyItems(
        '玩家地址依赖',
        AssemblyItem(
            'health_base_1', None, '8B 87 84 01 00 00 89 83 EC 01 00 00', None, delta, b'',
            AssemblyGroup('48 89 3D', Offset('character_addr'), '8B 87 84 01 00 00'),
            inserted=True,
            replace_len=6,
            args=(
                'b_no_hurt',
                'b_one_hit_kill',
                VariableType('character_addr', size=8),
            )),
        AssemblyItem(
            'health_base_2', None, '2B C6 89 87 84 01 00 00',
            None, delta, b'',
            AssemblyGroup(
                '29 F0 53 48 BB',
                Variable('character_addr'),
                '48 39 3B 75 10',
                Cmp('b_no_hurt', 1),
                '75 12 B8 0F 27 00 00 EB 0B',
                Cmp('b_one_hit_kill', 1),
                '75 02 31 C0 5B 89 87 84010000'
            ),
            inserted=True, replace_len=8),
    ),
    AssemblyItem(
        'no_hurt_base', '无伤害判定', 'F6 87 6C 01 00 00 01 75 51', None, delta, b'',
        AssemblyGroup(
            Cmp('b_no_hurt_2', 1),
            '75 17 50',
            '48 A1', Variable('character_addr'),
            '48 39 F8 58 75 06 48 83 FC 00 EB 07 F6 87 6C 01 00 00 01'
        ),
        inserted=True,
        replace_len=7,
        args=('b_no_hurt_2',),
        depends=('health_base_1',),
        hidden=True),
    VariableSwitch('b_no_hurt', '无限生命', depends=('health_base_1',)),
    VariableSwitch('b_one_hit_kill', '一击必杀', depends=('health_base_1',)),
    VariableSwitch('b_no_hurt_2', '无伤害判定', depends=('no_hurt_base',)),
    AssemblyItem(
        'inf_ammo', '无限子弹', '01 58 08 48 8B 5C 24 08', None, delta,
        b'', 'C7 40 08 E7 03 00 00 48 8B 5C 24 08', inserted=True),
    AssemblyItem(
        'no_reload', '无需装弹', '83 F8 FF 74 4E F7 43 58 00 30 00 00', None, delta, '31 C0 90', replace_len=3),
    AssemblyItem(
        'inf_grenades', '无限手雷', '41 B9 01 00 00 00 45 33 C0', None, delta, '41 B9 00', replace_len=3),
    AssemblyItem(
        'no_recoil', '无后坐力', '80 BC 24 A8 00 00 00 00 74 2C', None, delta,
        b'\xEB', replace_len=1, replace_offset=8),
    AssemblyItem(
        'perfect_accuraty', '超级精准度', 'F3 0F 58 83 D4 03 00 00', None, delta,
        b'\xEB\x1E', replace_len=8, replace_offset=-8),
    AssemblyItem(
        'rapid_fire', '快速射击', '2B C8 89 8C BB B4 02 00 00', None, delta, b'\x31\xC9', replace_len=2),
    AssemblyItem(
        'speed_base', '速度依赖', 'F3 0F 10 58 10 0F 2E D9', None, delta, b'',
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
