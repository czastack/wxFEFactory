from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems, VariableType, Delta, AssemblySwitch
from tools.base.assembly_code import AssemblyGroup, ORIGIN, Offset, Cmp, Variable


ADDRESS_SOURCES = {
    'steam': {
        'item_keep': 0x004FF000,
        'item_keep_5': 0x004FF000,
        'inf_ammo': 0x00F3D000,
        'inf_clip1': 0x004FD000,
        'inf_clip2': 0x004FB000,
        'max_backpack': 0x006B5000,
        'inf_modai': 0x004FF000,
        'inf_knife': 0x004FD000,
        'reset_save_count': 0x01C1E000,
        'quick_aim': 0x00EC4000,
        'no_recoil': 0x007CE000,
        'inf_health_base_1': 0x0042A000,
        'inf_health_base_2': 0x00F87000,
        'baojun_down_1': 0x00F4A000,
        'baojun_down_2': 0x0137F000,
        'enemy_speed_multi': 0x01C8F000,
        'show_action': 0x022C8000,
        'through_wall_xy': 0x01DD2000,
        'through_wall': 0x01DD2000,
        'reset_time': 0x00EA7000,
        'lock_timer': 0x01037000,
    },
    'codex': {
        'item_keep': 0x00E8A800,
        'item_keep_5': 0x00E8A800,
        'inf_ammo': 0x00401000,
        'inf_clip1': 0x00E88000,
        'inf_clip2': 0x00E86000,
        'max_backpack': 0,
        'inf_modai': 0x00E8A800,
        'inf_knife': 0x00E88000,
        'reset_save_count': 0x00BA0000,
        'quick_aim': 0x01705000,
        'no_recoil': 0x01125000,
        'inf_health_base_1': 0x004CD400,
        'inf_health_base_2': 0x00C58600,
        'baojun_down_1': 0x0178F000,
        'baojun_down_2': 0x01C62000,
        'enemy_speed_multi': 0,
        'show_action': 0x022BE000,
        'through_wall_xy': 0x01DC8000,
        'through_wall': 0x01DC8000,
        'reset_time': 0x00B7F000,
        'lock_timer': 0x0187A000,
    }
}


delta = Delta(0x2000)

ASSEMBLY_ITEMS = (
    AssemblyItem('item_keep', '数量不减', '2B DF 44 8B C3 48 8B D5', None, delta, b'\x90\x90', replace_len=2),
    AssemblyItem(
        'item_keep_5', '数量不减(<5)', '2B DF 44 8B C3 48 8B D5', None, delta, b'',
        '83 FB 05 72 02 29 FB 44 8B C3', inserted=True, replace_len=5),
    AssemblyItem(
        'inf_ammo', '备弹999', '48 8B 48 10 48 85 C9 74 05 8B 41 20 EB 02 33 C0 48 85 D2',
        None, delta, b'',
        '48 8B 48 10 48 85 C9 74 07 C7 41 20 E7030000',
        inserted=True, replace_len=7),
    AssemblyItems(
        '弹夹99',
        AssemblyItem(
            'inf_clip1', None, '48 8B 48 10 48 85 C9 74 03 8B 59 20 85 DB', None, delta, b'',
            '48 8B 48 10 48 85 C9 74 13 83 79 1C 00 74 0D 83 79 14 FF 74 07 C7 41 20 63 00 00 00 48 85 C9',
            inserted=True, replace_len=7),
        AssemblyItem(
            'inf_clip2', None, '48 8B 46 10 48 85 C0 75 1E 45 33 C0 48 8B CF 41 8D 50 38 48', None, delta, b'',
            '48 8B 46 10 48 85 C0 74 14 83 78 1C 00 74 0E 83 78 14 FF 74 08 BB 63 00 00 00 89 58 20 48 85 C0',
            inserted=True, replace_len=7),
    ),
    AssemblyItem(
        'max_backpack', '最大背包空间', '39 B2 90 00 00 00 7E * 44 8D 46 FF', None, delta, b'',
        'C7 82 90 00 00 00 14 00 00 00 39 B2 90 00 00 00',
        inserted=True, replace_len=6),
    AssemblyItem(
        'inf_modai', '保存时墨带无限', '48 8B 42 10 48 85 C0 74 03 8B 58 20', None, delta,
        b'', '48 8B 42 10 48 85 C0 74 07 C7 40 20 0A000000 48 85 C0 74 03 8B 58 20',
        inserted=True, replace_len=7),
    AssemblyItem(
        'inf_knife', '小刀无限耐久', '48 8B 48 10 48 85 C9 74 05 8B 41 20 EB 02 33 C0 66 0F 6E C6',
        None, delta, b'',
        '48 8B 48 10 48 85 C9 74 0B 83 79 14 2E 75 05 8B C6 89 41 20 48 85 C9',
        inserted=True, replace_len=7),
    AssemblyItem('reset_save_count', '最小保存次数', '8D 42 01 89 41 24', None, delta, '31 C0', replace_len=3),
    AssemblyItem(
        'quick_aim', '快速瞄准', 'F3 0F 10 87 20010000 48', None, delta,
        b'', 'C7 87 20010000 0000C842F3 0F10 87 20010000',
        inserted=True, replace_len=8),
    AssemblyItem(
        'no_recoil', '稳定射击', 'F3 0F 10 48 20 F2 0F 58 D6 F3 0F 11 4D 6F', None, delta,
        b'', AssemblyGroup('C7 40 10 00000000 C7 40 14 00000000', ORIGIN),
        inserted=True, replace_len=5),
    AssemblyItems(
        '玩家地址依赖',
        AssemblyItem(
            'inf_health_base_1', None, '48 8B 87 30 02 00 00 48 85 C0 75', None, delta, b'',
            AssemblyGroup(
                '48 8B 87 30 02 00 00 48 85 C0 74 1D 50 8F 05',
                Offset('character_addr'),
                Cmp('b_inf_health', 1),
                '75 0D 53 51 48 8D 58 58 8B 4B FC 89 0B 59 5B',
                # 快速射击
                Cmp('b_rapid_fire', 1),
                '75 52',
                Cmp('character_addr', 0),
                '74 49 50 51 52 48 A1', Variable('character_addr'),
                '48 8B 80 F8 00 00 00 48 8B 88 08 01 00 00 48 8B 49 54 48 8B 90 30 01 00 00'
                '48 83 F9 10 74 0F 48 83 F9 20 74 09 48 8B 0D',
                Offset('normal_speed'),
                'EB 07 48 8B 0D',
                Offset('rapid_fire_speed'),
                '48 89 4A 50 5A 59 58',
            ),
            inserted=True,
            replace_len=7,
            args=(
                'b_inf_health',
                'b_no_hurt',
                'b_one_hit_kill',
                'b_rapid_fire',
                VariableType('character_addr', size=8),
                VariableType('normal_speed', type=float, value=1.0),
                VariableType('rapid_fire_speed', type=float, value=10.0),
            )),
        AssemblyItem(
            'inf_health_base_2', None, '8B 4A 58 41 8B C0 99 33 C2 2B C2 2B C8 33 C0',
            None, delta, b'',
            AssemblyGroup(
                '48 8D 4A 58 48 A1',
                Variable('character_addr'),
                '48 39 D0 75 13',
                Cmp('b_no_hurt', 1),
                '75 08 8B 41 FC 89 01 45 31 C0 EB 15',
                Cmp('b_one_hit_kill', 1),
                '75 0C 41 83 F8 00 7E 06 41 B8 9F 86 01 00 8B 09 41 8B C0'
            ),
            inserted=True, replace_len=6),
    ),
    AssemblySwitch('b_inf_health', '无限生命', depends=('inf_health_base_1')),
    AssemblySwitch('b_no_hurt', '不会受伤', depends=('inf_health_base_1')),
    AssemblySwitch('b_one_hit_kill', '一击必杀', depends=('inf_health_base_1')),
    AssemblySwitch('b_rapid_fire', '快速射击', depends=('inf_health_base_1')),
    AssemblyItems(
        '暴君一击倒地且无法起身',
        AssemblyItem(
            'baojun_down_1', None, '39 71 58 0F 9F *', None, delta,
            b'', '83 79 58 01 7E 07 C7 41 58 01000000 39 71 58 0F 9F C0',
            inserted=True, fuzzy=True),
        AssemblyItem(
            'baojun_down_2', None,
            'F2 0F 5C F0 66 0F 5A CE F3 0F 11 8F F4 01 00 00 48 8B 43 50 48 39 48 18 75 1F',
            None, delta,
            b'', '68 00 00 C8 41 F3 0F 10 0C 24 48 83 C4 08',
            inserted=True, replace_len=8),
    ),
    AssemblyItem(
        'enemy_speed_multi', '敌人速度', 'F3 0F 11 40 4C 48 8B 47',
        None, delta, b'', AssemblyGroup(
            'F3 0F 59 05',
            Offset('enemy_speed_multi_value'),
            'F3 0F 11 40 4C'
        ),
        inserted=True, replace_len=5,
        args=(VariableType('enemy_speed_multi_value', type=float, value=0.0),)),
    AssemblyItem(
        'show_action', '显示可互动及可收集物品', 'F3 0F 59 63 6C F2 0F 10 D6', None, delta, b'',
        AssemblyGroup(
            '50 51 0F 29 05',
            Offset('float_1'),
            'F3 0F 10 43 6C 48 8B 4B 28 48 85 C9 74 35 48 8B 89 80 00 00 00 48 85 C9 74 29'
            '48 B8 2F 00 4E 00 6F 00 74 00 48 39 41 30 75 19 48 B8 69 00 63 00 65 00 2F 00'
            '48 39 41 38 75 09 B8 28 00 00 00 F3 0F 2A C0 F3 0F 59 E0 0F 28 05',
            Offset('float_1'),
            '59 58',
        ),
        inserted=True,
        replace_len=5,
        args=(VariableType('float_1', size=40, align=16, type=float, value=1.0),)
    ),
    AssemblyItem(
        'through_wall_xy', '穿墙(忽略地面)', '89 47 30 41 8B 46 04 89 47 34 41 8B 46 08 89 47 38',
        None, delta, '90 90 90 41 8B 46 04 89 47 34 41 8B 46 08 90 90 90'),
    AssemblyItem(
        'through_wall', '穿墙(包括地面)', '89 47 30 41 8B 46 04 89 47 34 41 8B 46 08 89 47 38',
        None, delta, '90 90 90 41 8B 46 04 90 90 90 41 8B 46 08 90 90 90'),
    AssemblyItem(
        'reset_time', '重置游戏时间',
        '48 8D 04 2A 48 89 41 18 48 8B 43 50 4C 39 70 18 0F 85 * * * * 44 38 77 53', None, delta,
        b'', AssemblyGroup(
            '48 8D 04 2A 48 89 41 18 48 2B 41 20 81 3D',
            Offset('reset_time_temp1', size=8),
            '00879303 7C 0A C7 05',
            Offset('reset_time_temp1', size=8),
            '00000000 81 05',
            Offset('reset_time_temp1', size=8),
            '40420F00 48 2B 05',
            Offset('reset_time_temp1'),
            '48 89 41 30 48 31 C0 48 89 41 28',
        ), inserted=True, replace_len=8, fuzzy=True,
        args=(VariableType('reset_time_temp1', 8),)),
    AssemblyItem(
        'lock_timer', '锁定倒计时', 'F3 0F 10 47 78 0F 57 F6', None, delta,
        b'', 'C7 47 78 00 A0 0C 47 F3 0F 10 47 78', replace_len=5, inserted=True),
)
