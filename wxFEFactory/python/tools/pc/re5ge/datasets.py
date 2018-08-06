from lib.hack.utils import OptionProvider


PERSONS = ('Chris', 'Sheva')

INVENTORY_OPTIONS = (
    ('小刀', 0x0101),
    ('M92F手枪（HG）', 0x0102),
    ('VZ61冲锋手枪（MG）', 0x0103),
    ('伊萨卡M37（SG）', 0x0104),
    ('S75狙击步枪（RIF）', 0x0105),
    ('手雷', 0x0106),
    ('燃烧弹', 0x0107),
    ('闪光弹', 0x0108),
    ('SIG 556步枪（MG）', 0x0109),
    ('地雷', 0x010A),
    ('S&W M29转轮手枪（MAG）', 0x010B),
    ('榴弹发射器', 0x010C),
    ('火箭筒', 0x010D),
    ('长弓', 0x010F),
    ('H&K P8', 0x0110),
    ('SIG P226手枪（HG）', 0x0111),
    ('H&K MP5冲锋枪（MG）', 0x0113),
    ('加特林机枪', 0x0115),
    ('M3冲锋枪（SG）', 0x0116),
    ('Jail Breaker霰弹枪（SG）', 0x0117),
    ('Hydra霰弹枪（SG）', 0x0119),
    ('沙鹰（MAG）', 0x011A),
    ('S&W M500转轮手枪（MAG）', 0x011B),
    ('H&K PSG-1狙击枪（RIF）', 0x011C),
    ('AK-74冲锋枪（MG）', 0x011D),
    ('M93R冲锋手枪（HG）', 0x011E),
    ('Dragunov SVD狙击枪', 0x0120),
    ('电棒', 0x0122),
    ('榴弹发射器（爆炸弹）', 0x0125),
    ('榴弹发射器（硫酸弹）', 0x0126),
    ('榴弹发射器（冰冻弹）', 0x0127),
    ('蛋（腐坏）', 0x0136),
    ('榴弹发射器（火焰弹）', 0x0139),
    ('榴弹发射器（闪光弹）', 0x013A),
    ('榴弹发射器（电击弹）', 0x013B),
    ('蛋（白色）', 0x013C),
    ('蛋（褐色）', 0x013D),
    ('蛋（金色）', 0x013E),
    ('手枪弹药', 0x0201),
    ('冲锋枪弹药', 0x0202),
    ('散弹枪弹药', 0x0203),
    ('狙击枪弹药', 0x0204),
    ('爆炸弹', 0x0206),
    ('硫酸弹', 0x0207),
    ('冰冻弹', 0x0208),
    ('马格南手枪弹药', 0x0209),
    ('火焰榴弹', 0x020E),
    ('闪光榴弹', 0x020F),
    ('电击榴弹', 0x0210),
    ('急救喷剂', 0x0304),
    ('草药（绿）', 0x0305),
    ('草药（红）', 0x0306),
    ('草药（绿+绿）', 0x0307),
    ('草药（绿+红）', 0x0309),
    ('防暴背心', 0x0601),
    ('防弹背心', 0x0606),
)

TREASURE_OPTIONS = (
    ('金戒指', 0x0417),
    ('亡灵新娘项链', 0x0418),
    ('毒牙', 0x0419),
    ('古董钟台', 0x041A),
    ('圣杯（银色）', 0x041B),
    ('圣杯（金色）', 0x041C),
    ('佛像（银色）', 0x041D),
    ('佛像（金色）', 0x041E),
    ('祭祀面具', 0x041F),
    ('象牙护身符', 0x0420),
    ('甲虫（褐色）', 0x0421),
    ('宝石甲虫', 0x0422),
    ('王室项链', 0x0423),
    ('宝石手镯', 0x0424),
    ('甲虫（金色）', 0x0425),
    ('黄宝石（梨形）', 0x0450),
    ('红宝石（橄榄形）', 0x0451),
    ('蓝宝石（梨形）', 0x0452),
    ('翡翠（梨形）', 0x0453),
    ('钻石（梨形）', 0x0454),
    ('黄宝石（方形）', 0x0457),
    ('红宝石（方形）', 0x0458),
    ('蓝宝石（方形）', 0x0459),
    ('翡翠（方形）', 0x045A),
    ('钻石（方形）', 0x045B),
    ('黄宝石（椭圆形）', 0x045E),
    ('红宝石（椭圆形）', 0x045F),
    ('蓝宝石（椭圆形）', 0x0460),
    ('翡翠（椭圆形）', 0x0461),
    ('钻石（椭圆形）', 0x0462),
    ('黄宝石（三角形）', 0x0465),
    ('红宝石（三角形）', 0x0466),
    ('蓝宝石（三角形）', 0x0467),
    ('翡翠（三角形）', 0x0468),
    ('钻石（三角形）', 0x0469),
    ('秘石', 0x046C),
    ('狮子之心', 0x046D),
    ('蓝色秘石', 0x046E),
    ('灵魂石', 0x046F),
    ('非洲之心', 0x0470),
    ('黄宝石（橄榄形）', 0x0473),
    ('红宝石（橄榄形）', 0x0474),
    ('蓝宝石（橄榄形）', 0x0475),
    ('翡翠（橄榄形）', 0x0476),
    ('钻石（橄榄形）', 0x0477),
    ('黄宝石（多面形形）', 0x047A),
    ('红宝石（多面形形）', 0x047B),
    ('蓝宝石（多面形形）', 0x047C),
    ('翡翠（多面形形）', 0x047D),
    ('钻石（多面形形）', 0x047E),
)


INVENTORY_ITEMS = OptionProvider(INVENTORY_OPTIONS)
TREASURE_ITEMS = OptionProvider(TREASURE_OPTIONS)
