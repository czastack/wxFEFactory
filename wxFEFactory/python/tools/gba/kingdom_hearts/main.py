from ..base import BaseGbaHack
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.exui.components import Pagination
from lib.hack.models import Model, Field, ByteField, WordField, ToggleField, ArrayField
from lib.win32.keys import VK
from fefactory_api import ui


class Global(Model):
    hp = WordField(0x02039B52, label="HP")
    hpmax = WordField(0x02039C18, label="总HP")
    cpmax = WordField(0x02039C1A, label="总CP")
    exp = WordField(0x02039C20, label="EXP")
    mp = WordField(0x02039C94, label="M点数")
    dark = WordField(0x02039C1C, label="Dark点数")
    atk = WordField(0x02039C1E, label="攻击力")
    battle_hp = WordField(0x0203314C, label="战斗HP")
    battle_hpmax = WordField(0x0203314E, label="战斗总HP")

    # 全特技
    # 02039CBC:FFFFFFFF
    # 02039CD0:FFFFFFFF
    # 02039CD4:FFFFFFFF
    skills = Field(0x02039C2C, bytes, 0x1C)
    map_cards = ArrayField(0x0203A830, 0x104, Field(0))
    battle_cards = ArrayField(0x02039FF0, 0x232, WordField(0))
    event_book = Field(0x02039C54, bytes, 0x40)

    riku_enable = ToggleField(0x02039B28, enable=0x20, disable=0, label="利库篇开启")


BATTLE_CARD_CLASS = (
    '王国之键',
    '心愿神灯',
    '红蟹之键',
    '南瓜脑袋',
    '精灵竖琴',
    '希望之星',
    '雷电之键',
    '金属路行鸟',
    '英雄神威',
    '狮子心',
    '幸运之键',
    '圣洁玫瑰',
    '约定之守护',
    '往昔之记忆',
    '钻石星辰',
    '片翼天使',
    '创世兵器',
    '火焰',
    '冰雪',
    '雷电',
    '回复',
    '重力',
    '停止',
    '强风',
    '唐老鸭',
    '高飞',
    '辛巴',
    '精灵',
    '斑比',
    '达博',
    '汀克',
    '木须',
    '克劳德',
    '阿拉丁',
    '爱丽儿',
    '杰克',
    '彼得潘',
    '伤药',
    '高级伤药',
    '魔力药',
    '高级魔力药',
    '究极炼金药',
)

ENEMY_CARDS = (
    '【黑影】卡片数字+1。2R',
    '【小兵】连击数+1。3R',
    '【巨身】防御所有正面攻击。1R',
    '【红色小夜曲】火焰威力增强。1R',
    '【蓝色狂想曲】冰雪威力增强。1R',
    '【黄色歌剧】雷电威力增强。1R',
    '【绿色安魂曲】回复效果增强。1R',
    '【狂力野猴】将卡片数字按照X→10-X的规则变换。1R',
    '【蹦蹦野猴】增大对经验球、Hp球的吸引范围。5R',
    '【飞兵】能够在移动中Reload。3R',
    '【强盗】普通攻击全部变为终结技。1R',
    '【肥盗】从背后攻击敌人时伤害增大。2R',
    '【木桶蜘蛛】Reload速度提高。3R',
    '【寻物妖怪】普通攻击附带吸血效果，但是敌人掉落的经验球减少。1R',
    '【海生霓虹】卡片数字随机变化。1R',
    '【螺旋枪兵】卡片数字-1。1R',
    '【海洋坦克】卡片用完后自动重装。1R',
    '【长臂骑士】重力减弱。3R',
    '【石像鬼】隐身。1R',
    '【海盗】卡片数字变为0。1R',
    '【飞行海盗】自己用的道具卡不会被敌人破坏。3R',
    '【黑暗球】隐藏自己的卡片，不被敌人看见。3R',
    '【防御大帝】受到的物理伤害减少。1R',
    '【双足飞龙】该敌人卡生效期间Reload计量数不会随Reload次数增加。3R',
    '【巫师】魔法威力上升但不能使用召唤类魔法卡。1R',
    '【进化黑影】敌人Hp随时间逐渐减少。1R',
    '【白蘑菇】使用友情卡时Hp回复。3R',
    '【黑毒蘑】随机发动一张敌人卡的效果。1R',
    '【爬行花】自己的【回复】不会被破坏。1R',
    '【龙卷步】Reload计量数-2。1E',
    '【大嗓门】增强召唤魔法，但是不能使用一般魔法。1R',
    '【防御盔甲】攻击范围提高。30A',
    '【寄生牢笼】破坏对手的敌人卡。1E',
    '【杂技大师】自己的卡片被破坏时，敌人用于破坏的卡片数字下降。10E',
    '【暗黑侧影】模仿敌人使用的敌人卡。',
    '【纸牌兵】攻速提高。30A',
    '【哈迪斯】濒死时攻击力大幅提高。30A。卡片生效期间火系伤害减少，受到冰系伤害时气绝。',
    '【贾方】攻击卡不会被破坏。20A',
    '【奥吉】Hp回复。当前Hp越少回复量越大。10E',
    '【黑毒蘑】1R的持续时间指的是如果你用了【黑毒蘑】但是一张卡都没出就Reload的话，那么这张【黑毒蘑】就宣告作废……',
    '【阿苏拉】敌人造成的魔法伤害减半，对召唤魔法造成的伤害无效。5E',
    '【虎克】Hp在2以上时，受到敌人必死一击(一套?待测试)后也还会剩下1Hp。卡片生效期间雷系伤害减少，受到火系伤害时气绝。3E',
    '【梅菲尔森特龙】攻击力大幅上升，Reload速度减慢。30A',
    '【利库】无视储卡副作用。卡片生效期间火系、雷系、冰系伤害减少。5E',
    '【阿克赛尔】在被击硬直中也能使用卡片。卡片生效期间火系伤害无效，受到冰系伤害时气绝。10次被击',
    '【拉克西恩】移动速度提高。卡片生效期间雷系伤害无效，特殊伤害增加。15次出卡',
    '【维克森】被打败后会回复一定量Hp继续战斗。卡片生效期间冰系伤害无效，受到火系伤害时眩晕。1E',
    '【马尔夏】无视储卡副作用，储卡技一次后立马重复一次。卡片生效期间火系、冰系、雷系、特殊伤害减少，物理伤害增加。3E',
    '【雷克萨斯】终结技命中前的瞬间有高概率是敌人消失，效果同【次元裂缝】。卡片生效期间冰系伤害无效，物理伤害减少，特殊伤害增加。50A',
    '【安塞姆】隐藏储卡。炎、冰、雷属性耐性增大。10次储卡技',
)


class Main(BaseGbaHack):

    def __init__(self):
        super().__init__()
        self._global = Global(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("hp")
            ModelInput("hpmax")
            ModelInput("cpmax")
            ModelInput("exp")
            ModelInput("mp")
            ModelInput("dark")
            ModelInput("atk")
            ModelInput("battle_hp")
            ModelInput("battle_hpmax")
            ModelCheckBox("riku_enable")

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.P, this.card_add),
        )

    def card_add(self):
        self._global.battle_cards[0] += 1
