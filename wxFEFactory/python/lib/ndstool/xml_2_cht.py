import xml.etree.ElementTree as ET
import re


text = """
<game>
    <folder>
        <name>杂项码</name>
        <cheat>
            <name>金钱最大</name>
            <codes>021947D8 05F5E0FF</codes>
        </cheat>
        <cheat>
            <name>经验值最大</name>
            <codes>021AAE90 05F5E0FF</codes>
        </cheat>
        <cheat>
            <name>[SELECT]邮票最大</name>
            <codes>94000130 FFFB0000 12194844 0000270F D2000000 00000000</codes>
        </cheat>
        <cheat>
            <name>画面切换高速化</name>
            <codes>52027164 47702000 12027164 00002001 D0000000 00000000</codes>
        </cheat>
        <cheat>
            <name>高速移动</name>
            <codes>121911FC 00001000</codes>
        </cheat>
        <cheat>
            <name>贩卖机绝对会中奖</name>
            <codes>52042B54 DD014287 12042B56 000046C0 D0000000 00000000</codes>
        </cheat>
        <cheat>
            <name>消费道具用后不减</name>
            <codes>5206DD4C 1C16B5F8 1206DD4E 00002600 D0000000 00000000</codes>
        </cheat>
        <cheat>
            <name>[SELECT+L/R=开/关]地图广域化显示</name>
            <codes>94000130 FEFB0000 12029FAA 00001100 12029FAC 00000042 0202A1AC 02002001 1202A1B0 00005829 1202A1CE 00002001 0202A1D0 58280200 1202A2BA 00001100 1202A2BC 00000040 1202A392 00002001 0202A394 58290200 1202A3B2 00002001 0202A3B4 58280200 0202AA30 E0500001 0202AA34 03A02702 0202AA38 0A000015 D0000000 00000000 94000130 FDFB0000 12029FAA 000010C2 12029FAC 00003AFF 0202A1AC 08416980 1202A1B0 00001809 1202A1CE 00006940 0202A1D0 18080841 1202A2BA 000010C0 1202A2BC 000038FF 1202A392 00006980 0202A394 18090841 1202A3B2 00006940 0202A3B4 18080841 0202AA30 E2811A0A 0202AA34 E0400001 0202AA38 E1A00000 D0000000 00000000</codes>
        </cheat>
        <cheat>
            <name>等级上升时随机数值最大</name>
            <codes>5206FC64 21001C18 0206FC64 1E482100 D0000000 00000000 520DF908 F7F32064 020DF908 E0002000 D0000000 00000000</codes>
        </cheat>
        <cheat>
            <name>游戏时间归零</name>
            <codes>021295DC 00000000</codes>
        </cheat>
        <cheat>
            <name>按[SELECT]将1号车的第一个物品复制到第2栏</name>
            <codes>94000130 FFFB0000 C0000000 00000004 D9000000 02196DD8 D6000000 02196DEC D2000000 00000000</codes>
        </cheat>
        <cheat>
            <name>装甲除底盘外重量为0</name>
            <codes>5206F37C 18248D48 0206F39C 80022200 0206F37C 85482000 D0000000 00000000</codes>
        </cheat>
        <cheat>
            <name>装备限制解除</name>
            <codes>5206E16C F85CF7C3 02000120 F882F031 02000124 1E5B2300 02000128 BDF8802B 1206E112 0000F792 1206E114 0000F805 0206E16C FFD8F791 D0000000 00000000</codes>
        </cheat>
        <cheat>
            <name>艺术家制作不需要素材</name>
            <codes>5204E9F0 88601884 1204EC06 0000E00A 1204E9F2 0000E014 D0000000 00000000</codes>
        </cheat>
        <cheat>
            <name>全车种双引擎</name>
            <codes>52074648 1892D841 12074646 00002201 12074648 00007762 D0000000 00000000</codes>
        </cheat>
        <cheat>
            <name>敌人掉落的都是3星</name>
            <codes>5206FEB4 0E000600 1206FEB6 00002003 D0000000 00000000</codes>
        </cheat>
    </folder>
</game>
"""

root = ET.fromstring(text)
INDENT = '\t'
codrbr = re.compile('(\\w{8} \\w{8}) ')


class BufferedPrinter:
    def __init__(self):
        self.buff = []

    def start(self):
        an.stdout = self

    def end(self):
        an.stdout = None
        _print('123')
        print("".join(self.buff), end="")
        self.buff.clear()

    def write(self, s):
        self.buff.append(s)

    def flush(self):
        pass


def parse(node, lv=0):
    tag = node.tag
    indent = INDENT * lv
    if tag == 'folder':
        print(indent + '+' + node.find('name').text)
        for child in node:
            parse(child, lv + 1)

    if tag == 'cheat':
        code = codrbr.sub('\\1\n%s' % indent, node.find('codes').text)
        print("%s[%s]" % (indent, node.find('name').text))
        print("%s%s\n" % (indent, code))


printer = BufferedPrinter()
printer.start()

for child in root:
    parse(child)

printer.end()
