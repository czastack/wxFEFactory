from lib.hack.model import Model, Field, Fields, ByteField, WordField, ArrayField


class Global(Model):
    x_invincible = Fields(Field(0x04857CE0), Field(0x04857CE4))
    zero_invincible = Fields(Field(0x0485A6E8), Field(0x0485A6EC))
    axl_invincible = Fields(Field(0x0485DA90), Field(0x0485DA94))

    hp_axl = Field(0x0428F388)
    hp_x = Field(0x0428F574)
    hp_zero = Field(0x0428F760)
    hpmax_axl = Field(0x0428F38C)
    hpmax_x = Field(0x0428F578)
    hpmax_zero = Field(0x0428F764)

    metal = Fields(Field(0x0428D320), Field(0x0428D31C))
    all_weapon = ByteField(0x0428D32D)

    super_x = ByteField(0x0428D32E)
    back_zero_white_axl = ByteField(0x0428D328)
    ultimate_x = ByteField(0x0428D330)

    zero_jump = ByteField(0x0485A6FC) # 锁住2
    resurgence = ByteField(0x0428D772)
    joint_attack = ByteField(0x04882D98)