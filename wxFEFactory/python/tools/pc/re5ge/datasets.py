from lib.hack.utils import ItemProviders, OptionProvider


CHARACTERS = ('克里斯', '莎娃')

INVENTORY_OPTIONS = (
    (0x0101, '小刀(不可见)'),
    (0x0102, 'M92F手枪（HG）'),
    (0x0103, 'VZ61冲锋手枪（MG）'),
    (0x0104, '伊萨卡M37（SG）'),
    (0x0105, 'S75狙击步枪（RIF）'),
    (0x0106, '手雷'),
    (0x0107, '燃烧弹'),
    (0x0108, '闪光弹'),
    (0x0109, 'SIG 556步枪（MG）'),
    (0x010A, '地雷'),
    (0x010B, 'S&W M29转轮手枪（MAG）'),
    (0x010C, '榴弹发射器'),
    (0x010D, '火箭筒'),
    (0x010E, '小刀(不可见)'),
    (0x010F, '长弓'),
    (0x0110, 'H&K P8'),
    (0x0111, 'SIG P226手枪（HG）'),
    (0x0113, 'H&K MP5冲锋枪（MG）'),
    (0x0115, '加特林机枪'),
    (0x0116, 'M3冲锋枪（SG）'),
    (0x0117, 'Jail Breaker霰弹枪（SG）'),
    (0x0119, 'Hydra霰弹枪（SG）'),
    (0x011A, '沙鹰（MAG）'),
    (0x011B, 'S&W M500转轮手枪（MAG）'),
    (0x011C, 'H&K PSG-1狙击枪（RIF）'),
    (0x011D, 'AK-74冲锋枪（MG）'),
    (0x011E, 'M93R冲锋手枪（HG）'),
    (0x011F, 'Px4手枪(HG)'),
    (0x0120, 'Dragunov SVD狙击枪'),
    (0x0121, '火焰喷射器(临时)'),
    (0x0122, '电棒'),
    (0x0125, '榴弹发射器（爆炸弹）'),
    (0x0126, '榴弹发射器（硫酸弹）'),
    (0x0127, '榴弹发射器（冰冻弹）'),
    (0x012F, '炮塔'),
    (0x0134, 'L.T.D'),
    (0x0136, '蛋（腐坏）'),
    (0x0139, '榴弹发射器（火焰弹）'),
    (0x013A, '榴弹发射器（闪光弹）'),
    (0x013B, '榴弹发射器（电击弹）'),
    (0x013C, '蛋（白色）'),
    (0x013D, '蛋（褐色）'),
    (0x013E, '蛋（金色）'),
    (0x0201, '手枪弹药'),
    (0x0202, '冲锋枪弹药'),
    (0x0203, '散弹枪弹药'),
    (0x0204, '狙击枪弹药'),
    (0x0206, '爆炸弹'),
    (0x0207, '硫酸弹'),
    (0x0208, '冰冻弹'),
    (0x0209, '马格南手枪弹药'),
    (0x020E, '火焰榴弹'),
    (0x020F, '闪光榴弹'),
    (0x0210, '电击榴弹'),
    (0x0304, '急救喷剂'),
    (0x0305, '草药（绿）'),
    (0x0306, '草药（红）'),
    (0x0307, '草药（绿+绿）'),
    (0x0309, '草药（绿+红）'),
    (0x0601, '防暴背心'),
    (0x0606, '防弹背心'),
)

TREASURE_OPTIONS = (
    (0x0417, '金戒指'),
    (0x0418, '亡灵新娘项链'),
    (0x0419, '毒牙'),
    (0x041A, '古董钟台'),
    (0x041B, '圣杯（银色）'),
    (0x041C, '圣杯（金色）'),
    (0x041D, '佛像（银色）'),
    (0x041E, '佛像（金色）'),
    (0x041F, '祭祀面具'),
    (0x0420, '象牙护身符'),
    (0x0421, '甲虫（褐色）'),
    (0x0422, '宝石甲虫'),
    (0x0423, '王室项链'),
    (0x0424, '宝石手镯'),
    (0x0425, '甲虫（金色）'),
    (0x0450, '黄宝石（梨形）'),
    (0x0451, '红宝石（橄榄形）'),
    (0x0452, '蓝宝石（梨形）'),
    (0x0453, '翡翠（梨形）'),
    (0x0454, '钻石（梨形）'),
    (0x0457, '黄宝石（方形）'),
    (0x0458, '红宝石（方形）'),
    (0x0459, '蓝宝石（方形）'),
    (0x045A, '翡翠（方形）'),
    (0x045B, '钻石（方形）'),
    (0x045E, '黄宝石（椭圆形）'),
    (0x045F, '红宝石（椭圆形）'),
    (0x0460, '蓝宝石（椭圆形）'),
    (0x0461, '翡翠（椭圆形）'),
    (0x0462, '钻石（椭圆形）'),
    (0x0465, '黄宝石（三角形）'),
    (0x0466, '红宝石（三角形）'),
    (0x0467, '蓝宝石（三角形）'),
    (0x0468, '翡翠（三角形）'),
    (0x0469, '钻石（三角形）'),
    (0x046C, '秘石'),
    (0x046D, '狮子之心'),
    (0x046E, '蓝色秘石'),
    (0x046F, '灵魂石'),
    (0x0470, '非洲之心'),
    (0x0473, '黄宝石（橄榄形）'),
    (0x0474, '红宝石（橄榄形）'),
    (0x0475, '蓝宝石（橄榄形）'),
    (0x0476, '翡翠（橄榄形）'),
    (0x0477, '钻石（橄榄形）'),
    (0x047A, '黄宝石（多面形形）'),
    (0x047B, '红宝石（多面形形）'),
    (0x047C, '蓝宝石（多面形形）'),
    (0x047D, '翡翠（多面形形）'),
    (0x047E, '钻石（多面形形）'),
)


INVENTORY_ITEMS = OptionProvider(INVENTORY_OPTIONS)
TREASURE_ITEMS = OptionProvider(TREASURE_OPTIONS)
INVENTORY_TREASURE_ITEMS = ItemProviders(INVENTORY_ITEMS, TREASURE_ITEMS)
