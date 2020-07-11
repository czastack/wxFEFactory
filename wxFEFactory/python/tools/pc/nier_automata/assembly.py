from tools.base.assembly_code import AssemblyGroup, Offset, ORIGIN
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems, VariableType, Delta


delta = Delta(0x1000)

ASSEMBLY_ITEMS = (
    AssemblyItem(
        'inf_health', '无限生命', '89 87 58 08 00 00 8B 9F 68 06 01 00', 0x001A6800, delta,
        b'', 'C7 87 58 08 00 00 7F 96 98 00 8B 9F 68 06 01 00', inserted=True),
    AssemblyItem(
        'locked_item', '锁定物品', '44 01 40 08 83 78 08', 0x005DCC00, delta, b'',
        '41 83 F8 00 7D 09 83 78 08 01 7E 03 45 31 C0 44 01 40 08 83 78 08 00',
        inserted=True),
    AssemblyItem(
        'inf_item', '无限物品', '8B 40 08 48 83 C4 28 C3 41', 0x005DCC00, delta, b'',
        '83 78 08 01 7E 07 C7 40 08 63 00 00 00 8B 40 08 48 83 C4 28',
        replace_len=7, inserted=True),
    # AssemblyItem(
    # 'double_jump', '无限二段跳', '44 39 82 A8 14 00 00', 0x004E1900, delta, b'',
    #     'C7 82 A8 14 00 00 00 00 00 00 44 39 82 A8 14 00 00', inserted=True),
    AssemblyItem(
        'double_jump', '无限二段跳', '83 BB A8 14 00 00 02 0F 8D', 0x001E2C00, delta,
        'FF 0F 8C', replace_offset=6, replace_len=3),
    AssemblyItem(
        'air_dashes', '无限冲刺', 'C7 83 88 0A 01 00 01 00 00 00', 0x001E2C00, delta,
        '00', replace_offset=6, replace_len=1),
    AssemblyItem(
        'pod_no_cd', 'pod技能无冷却', 'F3 0F 10 8C C1 24 6A 01 00', 0x00148200, delta, b'',
        '0F 57 C9 F3 0F 11 8C C1 24 6A 01 00', inserted=True),
    AssemblyItem(
        'chip_cost_1', '芯片占用1', '8B AC CA 60 1F 00 00', 0x006DB200, delta, b'',
        'BD 01 00 00 00 89 AC CA 60 1F 00 00', inserted=True),
    AssemblyItem(
        'chip_position', '芯片位置', '45 03 B4 CA 60 1F 00 00', 0x005EB800, delta,
        '4D 31 F6', replace_len=8, help='芯片自适应后叠加'),
    AssemblyItem(
        'weapon_upgrade_freely', '武器自由升级', '45 8B 94 D4 94 00 00 00',
        0x005EE400, delta, b'', '45 31 D2 45 89 94 D4 94 00 00 00', inserted=True),
    AssemblyItem(
        'pod_upgrade_freely', 'Pod自由升级', '45 8B 94 D7 94 00 00 00',
        0x005EE400, delta, b'', '45 31 D2 45 89 94 D7 94 00 00 00', inserted=True),
    AssemblyItem(
        'hacking_inf_health', '入侵时无限生命', '75 08 89 B1 DC 28 01 00',
        0x0020D800, delta, 'EB 0E', replace_len=2),
    AssemblyItem(
        'hacking_inf_time', '入侵时无限时间', 'F3 0F 10 49 08 F3 0F 58 41 04',
        0x0078A000, delta, b'', 'F3 0F 10 49 08 0F 57 C0 F3 0F 11 41 04 F3 0F 58 41 04',
        inserted=True),
    AssemblyItem(
        'hacking_one_hit', '一击回满入侵槽', 'F3 0F 58 B3 78 6D 01 00',
        0x0025B200, delta, b'', 'C7 83 78 6D 01 00 00 3C 1C 46 F3 0F 58 B3 78 6D 01 00',
        inserted=True),
    AssemblyItems(
        '穿墙',
        AssemblyItem(
            'throu_wall', None, '0F 29 42 50 44 39 82 68 05 00 00',
            0x00135200, delta, '90 90 90 90', replace_len=4),
        AssemblyItem(
            'throu_wall_2', None, '0F 29 43 50 39 93 68 05 00 00 7E 39',
            0x00135500, delta, '90 90 90 90', replace_len=4),
    ),
    AssemblyItem(
        'easy_kill', '容易击杀', '4D 8B C7 8B D3 FF C9',
        0x002F5200, delta, b'', '4D 8B C7 BA 40 54 89 00 FF C9', inserted=True),
    AssemblyItem(
        'exp_mult', '多倍经验', '03 CF B8 7F 96 98 00',
        0x00596000, delta, b'', AssemblyGroup('0F AF 3D', Offset('exp_mult'), ORIGIN), inserted=True,
        args=(VariableType('exp_mult', value=2),)),
)
