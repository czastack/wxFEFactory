
STATUS_CHOICES = ('普通', '不减')
STATUS_VALUES = (5, 6)

# 100% = 464, 200% = 1169, Max = 8388607
BADASS_BONUSES = (
    "最大生命值",
    "护盾容量",
    "护盾充能速度",
    "护盾充能延迟",
    "近战伤害",
    "手雷伤害",
    "武器精准率",
    "枪械伤害",
    "射速",
    "后坐力减免",
    "元素效果几率",
    "装填速度",
    "元素效果伤害",
    "暴击伤害",
)


SKILL_NAMES = (
    ('突击手', '军刀枪塔', (
        ('游击系', ('岗哨布控', '有备无患', '激光瞄准', '斗志昂扬', '勇猛进军', '焦土战略', '一展长才', '掷弹能手', '危机管理', '双管齐下')),
        ('火药系', (
            '激烈交锋', '职业军人', '战术嵌装', '金属风暴', '稳操胜券', '枪塔远布', '前沿阵地', '使命召唤', '决一死战', '别动队员', '核爆打击',
        )),
        ('游击系', (
            '身强体壮', '常备不懈', '最后手段', '力挽狂澜', '百炼成钢', '方阵护盾', '快速充能', '资源回收', '枪塔嵌锁', '视死如归', '双子枪塔'
        )),
    )),
    ('暗杀者', '幻影·零', (
        ('狙击系', ('一击爆头', '光学运用', '杀手天成', '追求精准', '弹无虚发', '穿身破甲', '让子弹飞', '伺机待发', '人枪合一', '暴击天国')),
        ('诡诈系', ('手疾眼快', '反戈一击', '英勇无畏', '暗中突袭', '后劲十足', '死亡印记', '出其不意', '活化细胞', '双弹齐发', '死亡绽放')),
        ('血屠系', ('致死打击', '钢筋铁手', '冷酷无情', '善变如水', '有始有终', '就地处决', '狠辣背刺', '血脉复苏', '穿行如风', '杀戮盛宴')),
    )),
    ('魔女', '相位锁定', (
        ('操控系', ('防护强化', '弹速强化', '悬停专精', '动量反转', '身轻如燕', '相位收束', '惯性作用', '相位鼓动', '目标转移', '思维锁定')),
        ('调和系', ('灵犀之眼', '甜蜜解脱', '恢复专精', '火上浇油', '隔岸观火', '转世重生', '以牙还牙', '回复强化', '生命之源', '嘲弄之球')),
        ('灾厄系', ('闪变效应', '先见之明', '火焰祭献', '阳焱爆裂', '相位连锁', '致命酸雾', '引燃体质', '生命收割', '病毒凤凰', '相位毁灭')),
    )),
    ('狂枪手', '双枪狂虐', (
        ('嗜枪系', (
            '装填摇滚', '瞬间拔枪', '救命稻草', '系于一发', '异中有同', '自动装填',
            '压轴一弹', '天性暴虐', '虚而不屈', '血仍未冷', '以杀止杀'
        )),
        ('狂暴系', (
            '如有天助', '满打满算', '反应直觉', '坚持到底', '早有准备', '稳扎稳打',
            '五发六中', '乐在其中', '乐趣倍增', '来者不拒', '密集弹幕'
        )),
        ('肌肉系', (
            '百折不挠', '激发潜能', '皮糙肉厚', '气贯长虹', '浴血奋战', '暴虐之拳',
            '毫无阻隔', '马不停蹄', '愈挫愈勇', '暴龙血性', '向我开炮'
        )),
    )),
    ('机械术士', '死神吵闹', (
        ('友爱系', (
            '近在咫尺', '编派问题', '奇妙数学', '振奋人心', '事半功倍', '壮硕小马',
            '机关算尽', '势不可挡', '吵闹爆破', '坚甲利兵', '冷静两成', '不分彼此'
        )),
        ('妨碍系', (
            '精力充沛', '神经绝缘', '电击风暴', '灼热视线', '金刚之力', '电光石火',
            '如雷贯耳', '邪恶女巫', '轰天裂地', '导体催化', '耀斑爆发', '闪耀时刻'
        )),
        ('扰乱系', (
            '短小精悍', '无法无天', '微缩叛客', '机械暴乱', '血染之盾', '安卓狂躁',
            '不和谐音', '定时破除', '理性动乱', '死从天降', '多重分级', '数码钩爪'
        )),
    )),
    ('疯子', '飞斧狂暴', (
        ('嗜血系', (
            '浸血透枪', '恐血痉挛', '腥香血膻', '血红甦生', '血液超涌', '浴血屠杀',
            '投弹飞斧', '鲜血供养', '血光恍惚', '血液沸腾', '充血神经', '血色爆裂'
        )),
        ('狂躁系', (
            '怒火释放', '火线引爆', '茹毛饮血', '享受痛苦', '怒不可遏', '杀戮振奋',
            '点燃引线', '血肉纷飞', '移魂换命', '伤上撒盐', '沉默羔羊', '兽性大发'
        )),
        ('狱炎系', (
            '烧吧宝贝', '抱薪救火', '神经麻木', '痛苦力量', '元素激奋', '被害妄想',
            '火炎恶魔', '火焰耀斑', '地火臭息', '元素入神', '怒号惩戒'
        )),
    ))
)
