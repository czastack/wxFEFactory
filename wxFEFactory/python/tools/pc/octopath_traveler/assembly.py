from tools.base.assembly_hacktool import AssemblyItem, Delta, AssemblySwitch
from tools.base.assembly_code import AssemblyGroup, Cmp

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
)
