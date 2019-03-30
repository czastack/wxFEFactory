from lib.hack.models import Model, Field, ByteField, WordField, ArrayField, ModelField


class Robot(Model):
    SIZE = 0x34
    START = 0x0202A358
    # 我方 start: 0x0202A358, step: 0x34, length: 0x46
    # 敌方 start: 0x0202B190, step: 0x34, length: 0x28

    hp = Field(0, label="HP")
    en = WordField(4, label="EN")
    body = WordField(6, label="机种")
    pilot = WordField(8, label="人物")
    # 机体改造
    body_remould = ArrayField(26, 4, ByteField(0),
        label=('机体改造:HP', '机体改造:EN', '机体改造:运动性', '机体改造:装甲'))
    weapon_remould = ByteField(31, label="武器改造")
    # 弹药 63636363
    ammo = ArrayField(32, 4, ByteField(0), label="弹药")


class Pilot(Model):
    SIZE = 0x20
    START = 0x020285F4

    # 我方 start: 0x020285F4, step: 0x20, length: 0x63
    pilot = WordField(0, label="人物")
    exp = WordField(2, label="经验")  # 决定等级 max:0xC000
    sp = WordField(4, label="精神点数")  # 03E7
    killed = WordField(6, label="击坠")  # 03E7
    help_atk = ByteField(13, label="援攻")  # 09
    help_def = ByteField(14, label="援防")  # 09
    energy = ByteField(15, label="气力")  # 96
    points = ByteField(17, label="奖励点数")  # FF
    # 养成能力
    develop = ArrayField(18, 6, ByteField(0),
        label=('养成:格斗', '养成:射击', '养成:防御', '养成:技量', '养成:回避', '养成:命中',))
    skill_chip = ArrayField(24, 4, ByteField(0), label="技能芯片")


class Global(Model):
    money = Field(0x02029750, label="金钱")
    turn = Field(0x02029760, label="回合")
    after_money = Field(0x020361D0, label="战后金钱")
    after_exp = Field(0x020361D4, label="战后经验")
    chapter = ByteField(0x02029776, label="关卡")
    intensified_parts = ArrayField(0x020297B0, 67, ByteField(0))  # 强化部件
    mini_games = ArrayField(0x020297F4, 51, ByteField(0))  # 小游戏
    skill_chip = ArrayField(0x02029786, 42, ByteField(0))  # 技能芯片


# 全员无限移动
# 4203424E 0103
# 0000003C 0084

# 全机体已探查
# 4203423E 1001
# 0000003C 0084
