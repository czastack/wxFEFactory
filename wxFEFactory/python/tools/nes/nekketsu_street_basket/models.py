from lib.hack.models import Model, Field, ByteField, WordField, BitsField, ArrayField, ToggleField, ToggleFields


class Global(Model):
    turn = ByteField(0x058C, label='前/后半场')
    minutes = ByteField(0x06C2, label='剩余分钟')
    seconds_1 = ByteField(0x06C3, label='秒十位数')
    seconds_0 = ByteField(0x06C4, label='秒个位数')

    our_points = ByteField(0x0166, label='我方进球')
    enemy_points = ByteField(0x0167, label='敌方进球')

    basketry = Field(0x057E, size=6, label='球筐耐久')
    basketry_left_bottom = ByteField(0x057E, label='左下球框耐久')  # 08 左下球框不掉
    basketry_right_bottom = ByteField(0x057F, label='右下球框耐久')  # 08 右下球框不掉
    basketry_left_middle = ByteField(0x0580, label='左中球框耐久')  # 06 左中球框不掉
    basketry_right_middle = ByteField(0x0581, label='右中球框耐久')  # 06 右中球框不掉
    basketry_left_top = ByteField(0x0582, label='左上球框耐久')  # 05 左上球框不掉
    basketry_right_top = ByteField(0x0583, label='右上球框耐久')  # 05 右上球框不掉

    ball_owner = ByteField(0x053F, label='球所在')  # 球在人手里(0~3),地上或空中(6)
    ball_form = ByteField(0x0518, label='球形态')

    # 原数据-->修改后
    # 横坐标清除必杀释放限制静态地址：
    # 0x18cfc-10-->00
    # 0x18d00-60-->80
    # 0x18d91-10-->00
    # 0x18d95-60-->80

    # 纵坐标清除必杀释放限制静态地址：
    # 0x18d06-05-->06
    # 0x18d9b-05-->06
    skill_anywhere = ToggleFields()


class Character(Model):
    jump = ByteField(0x0576, label='无限跳')  # 0: 未二段跳, 0x80: 已二段跳
    power = ByteField(0x0572, label='无限威力')
    character = ByteField(0x03E3, label='角色(0~3)')


class EquipHolder(Model):
    SIZE = 3
    equip_1 = ByteField(0x06E4, label='衬衫')
    equip_2 = ByteField(0x06E5, label='短裤')
    equip_3 = ByteField(0x06E6, label='鞋子')
