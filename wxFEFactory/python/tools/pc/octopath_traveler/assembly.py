from tools.base.assembly_hacktool import AssemblyItem, Delta, AssemblySwitch, VariableType
from tools.base.assembly_code import AssemblyGroup, Cmp, Offset, Variable, ForwardCall, ORIGIN

delta = Delta(0x20000)

ASSEMBLY_ITEMS = (
    AssemblyItem(
        'health_base', 'health_base', '48 8B 03 48 89 D9 FF 90 38 01 00 00 48 85 C0', 0x0B57A000, delta, b'',
        AssemblyGroup(
            '48 8B 03 3D 8889B541 75 72 83 BB 58010000 00 74 69 8B 83 E0030000 83 F8 00 7E 42 83 F8 09 7D 3D',
            Cmp('b_inf_health', 1),
            '75 0A C7 83 E4030000 0F270000 ',
            Cmp('b_inf_sp', 1),
            '75 0A C7 83 E8030000 0F270000',
            Cmp('b_inf_bp', 1),
            '75 0C 8B 83 30040000 89 83 28040000 EB 1C',
            Cmp('b_one_hit_kill', 1),
            '75 13 83 BB E4030000 01 7E 0A C7 83 E4030000 01000000',
            '48 8B 03 48 8B CB'
        ),
        args=(
            'b_inf_health',
            'b_inf_sp',
            'b_inf_bp',
            'b_one_hit_kill',
        ),
        inserted=True, replace_len=6, hidden=True),
    AssemblySwitch('b_inf_health', '无限生命', depends=('health_base')),
    AssemblySwitch('b_inf_sp', '无限SP', depends=('health_base')),
    AssemblySwitch('b_inf_bp', '无限BP', depends=('health_base')),
    AssemblySwitch('b_one_hit_kill', '一击必杀', depends=('health_base')),

    AssemblyItem(
        'battle_result', '战斗结果', '41 FF 54 C5 00 48 85 DB', 0x0605B000, delta, b'',
        AssemblyGroup(
            '41 FF 54 C5 00 41 83 F8 04 0F85 5F000000 48 83 FB 00 0F85 55000000 41 83 FF 00'
            '0F85 4B000000 48 81 FD 90ED8C00 0F85 3E000000 49 81 FA F4EE8C00 0F85 31000000 51 8B 08',
            '0FAF 0D', Offset('money_multi'),
            '89 08 8B 48 04'
            '0FAF 0D', Offset('exp_multi'),
            '89 48 04 8B 48 08'
            '0FAF 0D', Offset('jp_multi'),
            '89 48 08 59'
            '48 A3', Variable('br_ptr'),
        ),
        args=(
            VariableType('money_multi', value=2),
            VariableType('exp_multi', value=2),
            VariableType('jp_multi', value=2),
            VariableType('br_ptr', size=8),
        ),
        inserted=True, replace_len=5
    ),

    AssemblyItem(
        'easy_steal', '容易偷盗、探查等', '49 8B CA 0F AF 46 30 4C 63 C0', 0x00367000, delta, b'',
        AssemblyGroup(
            ForwardCall(),
            '53 48 BB 48 EA 89 42 01 00 00 00 48 8B 1B 41 83 FE 01 0F 85 40 01 00 00 41 83 F8 04 0F 85 36 01 00 00'
            '48 8B 9B 70 03 00 00 48 8B 9B C8 01 00 00 83 7A FC 03 0F 84 23 00 00 00 83 7A FC 04 0F 84 48 00 00 00'
            '83 7A FC 06 0F 84 6D 00 00 00 83 7A FC 08 0F 84 85 00 00 00 E9 FB 00 00 00 48 8D 9B 94 01 00 00 48 39 DA'
            '0F 85 EB 00 00 00 49 81 FF 28 70 8C 00 0F 84 9F 00 00 00 49 81 FF 88 E4 8C 00 0F 84 92 00 00 00'
            'E9 CC 00 00 00 48 8D 9B 5C 02 00 00 48 39 DA 0F 85 BC 00 00 00 49 81 FF 18 DE 8C 00 0F 84 70 00 00 00'
            '49 81 FF F8 65 8C 00 0F 84 63 00 00 00 E9 9D 00 00 00 48 8D 9B EC 03 00 00 48 39 DA 0F 85 8D 00 00 00'
            '49 81 FF 48 DE 8C 00 0F 84 63 00 00 00 E9 7B 00 00 00 48 8D 9B 7C 05 00 00 48 39 DA 0F 85 6B 00 00 00'
            '49 81 FF E8 C3 8C 00 0F 84 41 00 00 00 49 81 FF E8 DF 8C 00 0F 84 34 00 00 00 49 81 FF 08 61 8C 00'
            '0F 84 27 00 00 00 E9 3F 00 00 00 83 3A 00 0F 8C 36 00 00 00 83 3A 63 0F 8F 2D 00 00 00 B9 63 00 00 00'
            'C7 00 63 00 00 00 E9 1D 00 00 00 83 3A 00 0F 8C 14 00 00 00 83 3A 63 0F 8F 0B 00 00 00 B9 C8 00 00 00'
            'C7 00 C8 00 00 00 5B'
        ),
        inserted=True, replace_len=5, replace_offset=10,
    ),
)
