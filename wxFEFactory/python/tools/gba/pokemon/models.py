from lib.hack.model import (
    Model, Field, ByteField, WordField, DWordField, BitsField, ArrayField, 
    ModelField, ModelPtrField, OffsetsField, FieldPrep, SignedField, ManagedModel
)
from lib.hack.localhandler import LocalHandler
from lib import utils
import ctypes


class ItemSlot(Model):
    SIZE = 4
    item = ByteField(0)
    count = ByteField(1)
    value = WordField(0)


class Pokemon(Model):
    SIZE = 0xA0

    hpmax = WordField(0x20069F8)


class StoreItem(Model):
    SIZE = 8
    item = WordField(0)


class PokemonStructHeader(Model):
    SIZE = 32
    dwChar = DWordField(0x00)                           # @00, 性格値
    dwID = DWordField(0x04)                             # @04, トレーナのＩＤ
    bNickName = Field(0x08, bytes, 10)                  # @08, ニックネーム
    bNickNameLanguage = ByteField(0x12)                 # @12, '01' = 6 bytes (jp), '02' = 10 bytes (en)
    bBadEgg = ByteField(0x13)                           # @12, '02' for daycare-center-enabled, '07' for ダメタマゴ
    bCatcherName = Field(0x14, bytes, 7)                # @14, トレーナの名前
    bMarkings = ByteField(0x1B)                         # @1B, only the lowest 4 bits are used
    wChecksum = WordField(0x1C)                         # @1C, Checksum
    # unk0 = ArrayField(0x1E, 2, ByteField(0))          # @1E, '00 00'


class PokemonStructBreedInfo(Model):
    SIZE = 12
    wBreed = WordField(0x00) # 种族ID
    wItem = WordField(0x02) # 持有物
    dwExp = DWordField(0x04) # 
    bPointUp0, bPointUp1, bPointUp2, bPointUp3 = \
        BitsField.create(0x08, 1, (2, 2, 2, 2))
    bIntimate = ByteField(0x09) # 亲密度
    # unk0 = WordField(0x10)


class PokemonStructSkillInfo(Model):
    SIZE = 12
    rgwSkillId = ArrayField(0x00, 4, WordField(0)) # ID of the Skill
    rgbPoints = ArrayField(0x08, 4, ByteField(0)) # Skill Points


class PokemonStructAcquiredInfo(Model):
    SIZE = 12
    rgbBattleBonuses = ArrayField(0x00, 6, ByteField(0)) # 努力值(ＨＰ, 攻击, 防御, 敏捷, 特攻, 特防)
    rgbApealPoints = ArrayField(0x06, 6, ByteField(0)) # 魅力值(帅气, 美丽, 可爱, 聪明, 坚强, 软弱)


class PokemonStructInnateInfo(Model):
    SIZE = 12
    (
        bPokeVirus,    # @0x00, if any bit is set, ポケルスがかかる
        bBlackPoint,   # @0x04, if any bit is set, 黒い点がつき
        bCatchPlace,   # @0x08, where the Pokemon was caught
        bCatchLevel,   # @0x10, the Pokemon's level when it was caught
        bGameVersion,  # @0x17, game version (sapphire=1, ruby=2, emerald=3, fire=4, leaf=5)
        bPokeBall,     # @0x1B, Poke-Ball type (Write twice, why?)
        unk1,          # @0x1F, 0
    ) = BitsField.create(0x00, 4, (4, 4, 8, 7, 4, 4, 1))
    (
        bHPIndv,       # @0x20, ＨＰ (个体值)
        bAtkIndv,      # @0x25, 攻撃 (个体值)
        bDefIndv,      # @0x2A, 防御 (个体值)
        bDexIndv,      # @0x2F, 敏捷 (个体值)
        bSAtkIndv,     # @0x34, 特攻 (个体值)
        bSDefIndv,     # @0x39, 特防 (个体值)
        bIsEgg,        # @0x3E, 是否是蛋
        bSpecialty,    # @0x3F, 特性 (0: the 1st, 1: the 2nd)
    ) = BitsField.create(0x00, 4, (5, 5, 5, 5, 5, 5, 1, 1))
    (
        bRibbon0,      # @0x40, # of リボン (0 - 4) かっこよさ：ノーマル、スーパー、ハイパー、マスター
        bRibbon1,      # @0x43, # of リボン (0 - 4) うつくしさ：ノーマル、スーパー、ハイパー、マスター
        bRibbon2,      # @0x46, # of リボン (0 - 4) かわいさ：ノーマル、スーパー、ハイパー、マスター
        bRibbon3,      # @0x49, # of リボン (0 - 4) かしこさ：ノーマル、スーパー、ハイパー、マスター
        bRibbon4,      # @0x4C, # of リボン (0 - 4) たくましさ：ノーマル、スーパー、ハイパー、マスター
        bRibbon5,      # @0x4F, # of リボン (0 - 1) x 12 (bit0-4: ok, bit5-11: reserved)
        unk2,          # @0x5B, 0
        bObedience,    # @0x5F, 幻のポケモンは命令を聞く
    ) = BitsField.create(0x00, 4, (3, 3, 3, 3, 3, 12, 4, 1))


class PokemonStructInfo(Model):
    SIZE = 12
    BreedInfo = ModelField(0, PokemonStructBreedInfo)
    SkillInfo = ModelField(0, PokemonStructSkillInfo)
    AcquiredInfo = ModelField(0, PokemonStructAcquiredInfo)
    InnateInfo = ModelField(0, PokemonStructInnateInfo)


class PokemonStruct(Model):
    SIZE = 80
    bEncoded = True

    Header = ModelField(0, PokemonStructHeader)
    rgInfo = ArrayField(32, 4, ModelField(0, PokemonStructInfo))
    # 加密解密的位置
    values = ArrayField(32, 12, DWordField(0))

    def attach(self):
        if (self.Header.bBadEgg & 0x05) != 0:
            self.Header.bBadEgg &= (~0x05) & 0xFF
        
        self.CalculatePokemonStructInfoPtr()

    def CalculatePokemonStructInfoPtr(self):
        rgInfo = self.rgInfo
        bOrder = self.DetermineWhichIsWhere()
        self.breedInfo = rgInfo[bOrder[0]].BreedInfo
        self.skillInfo = rgInfo[bOrder[1]].SkillInfo
        self.acquiredInfo = rgInfo[bOrder[2]].AcquiredInfo
        self.innateInfo = rgInfo[bOrder[3]].InnateInfo

    def DetermineWhereIsWhich(self):
        bOrder = [0, 1, 2, 3]

        bPosition = self.Header.dwChar % 24
        bCount = 6
        bTypeId = 0

        while bPosition > 0:
            bSubGroupIdAddTypeId = (bPosition // bCount) + bTypeId
            while bSubGroupIdAddTypeId > bTypeId:
                b = bOrder[bSubGroupIdAddTypeId]
                bOrder[bSubGroupIdAddTypeId] = bOrder[bSubGroupIdAddTypeId - 1]
                bOrder[bSubGroupIdAddTypeId - 1] = b
                bSubGroupIdAddTypeId -= 1

            bPosition %= bCount
            bCount //= (3 - bTypeId)
            bTypeId += 1

        return bOrder

    def DetermineWhichIsWhere(self):
        bTemp = self.DetermineWhereIsWhich()
        bOrder = [0, 0, 0, 0]
        for i in range(4):
            bOrder[bTemp[i]] = i
        return bOrder

    def Decode(self):
        """解密 此操作应在local对象上执行"""
        if self.bEncoded:
            pdwPokemon = self.values
            Header = self.Header

            dwXorMask = Header.dwChar ^ Header.dwID
            wChecksum = 0

            for n in range(len(pdwPokemon)):
                temp = pdwPokemon[n]
                temp ^= dwXorMask
                pdwPokemon[n] = temp
                wChecksum += utils.LOWORD(temp) + utils.HIWORD(temp)

            Header.wChecksum = utils.LOWORD(wChecksum)
            self.bEncoded = False

    def Encode(self):
        """加密 此操作应在local对象上执行"""
        if self.bEncoded:
            return

        pdwPokemon = self.values
        Header = self.Header

        # make sure this pokemon is daycare-center-enbled, and not a bag egg
        if self.breedInfo.wBreed != 0:
            Header.bBadEgg |= 0x02
            Header.bBadEgg &= (~0x05) & 0xFF

        dwXorMask = Header.dwChar ^ Header.dwID
        wChecksum = 0

        for n in range(len(pdwPokemon)):
            temp = pdwPokemon[n]
            wChecksum += utils.LOWORD(temp) + utils.HIWORD(temp)
            pdwPokemon[n] = temp ^ dwXorMask

        Header.wChecksum = wChecksum
        self.bEncoded = True


class PokemonStructRear(Model):
    SIZE = 20
    bStatus = ByteField(0x00)
    bLevel = ByteField(0x04)
    wHPcur = WordField(0x06)
    wHPcap = WordField(0x08)
    wAtk = WordField(0x0A)
    wDef = WordField(0x0C)
    wDex = WordField(0x0E)
    wSAtk = WordField(0x10)
    wSDef = WordField(0x12)


class PokemonStructActive(Model):
    SIZE = 100
    pmStruct = ModelField(0, PokemonStruct)
    pmRear = ModelField(80, PokemonStructRear)


class PokemonStructActives(Model):
    """local helper"""
    SIZE = PokemonStructActive.SIZE * 6
    content = ArrayField(0, 6, ModelField(0, PokemonStructActive), True)

    def to_local(self):
        p = ctypes.create_string_buffer(self.to_bytes())
        local_ins = __class__(ctypes.addressof(p), LocalHandler.get_instance())
        local_ins.buff = p
        return local_ins


class BaseGlobal(Model):
    def _empty(self):
        pass

    def mask(self, value, field):
        if not isinstance(value, int):
            value = int(value)
        value = self.xor_mask ^ value
        if field.size == 2:
            value &= 0xFFFF
        return value

    def managed_mask(self, value, field):
        if not isinstance(value, int):
            value = int(value)
        value = self.context.xor_mask ^ value
        if field.size == 2:
            value &= 0xFFFF
        return value

    battle_points_current = property(_empty)
    battle_points_trainer_card = battle_points_current

    
MaskedField = FieldPrep(BaseGlobal.mask)
ManagedMaskedField = FieldPrep(BaseGlobal.managed_mask)


class PokemonItem(ManagedModel):
    """背包物品"""
    SIZE = 4

    item = WordField(0)
    quantity = ManagedMaskedField(WordField(2))


class PokemonItemField(ModelField):
    def __init__(self, offset):
        super().__init__(offset, PokemonItem)

    def create_cache(self, instance):
        return self.modelClass(instance.addr + self.offset, instance)


class PointerGlobal(BaseGlobal):
    def __getattr__(self, name):
        if self.Inner.field(name):
            return getattr(self.inner, name)
        return super().__getattr__(name)

    def __setattr__(self, name, value):
        if self.Inner.field(name):
            setattr(self.inner, name, value)
        else:
            return super().__setattr__(name, value)


class RubySapphireJpGlobal(BaseGlobal):
    active_pokemon_count = Field(0x03004280)
    active_pokemon = ModelField(0x03004290, PokemonStructActives)
    stored_pokemon = Field(0x0202FDC0)
    _player_name = Field(0x02024C04, bytes, 10)
    _player_id = Field(0x02024C0E)
    xor_mask = 0
    money = MaskedField(Field(0x02025924))
    coin = MaskedField(WordField(0x02025928))
    dust = WordField(0x02026864)
    menu = Field(0x020267B4)
    decorate = Field(0x02027B34)
    badge = Field(0x020267B5)
    clock_adjustment = Field(0x02024C9C)
    per_day_random = Field(0x0202681C)
    spray_time = WordField(0x02026816)
    safari_balls = ByteField(0x02038504)
    safari_time = WordField(0x02038506)
    daycare_center_step_1 = ByteField(0x02028540)
    daycare_center_step_2 = ByteField(0x02028544)
    step_counter = ByteField(0x0202854A)
    exp_gain = SignedField(0x0202494C, size=2)

    _iemfield = PokemonItemField(0)
    item_normal = ArrayField(0x020259F4, 0x14, _iemfield)
    item_keyitem = ArrayField(0x02025A44, 0x14, _iemfield)
    item_pokeball = ArrayField(0x02025A94, 0x10, _iemfield)
    item_machine = ArrayField(0x02025AD4, 0x40, _iemfield)
    item_berry = ArrayField(0x02025BD4, 0x2E, _iemfield)
    item_pokeblock = ArrayField(0x02025C8C, 0x28, _iemfield)


class RubySapphireEnGlobal(BaseGlobal):
    active_pokemon_count = Field(0x03004350)
    active_pokemon = ModelField(0x03004360, PokemonStructActives)
    stored_pokemon = Field(0x020300A4)
    _player_name = Field(0x02024EA4, bytes, 10)
    _player_id = Field(0x02024EAE)
    xor_mask = 0
    money = MaskedField(Field(0x02025BC4))
    coin = MaskedField(WordField(0x02025BC8))
    dust = WordField(0x02026B04)
    menu = Field(0x02026A54)
    decorate = Field(0x02027DD4)
    badge = Field(0x02026A55)
    clock_adjustment = Field(0x02024F3C)
    per_day_random = Field(0x02026B0A)
    spray_time = WordField(0x02026AB6)
    safari_balls = ByteField(0x02038808)
    safari_time = WordField(0x0203880A)
    daycare_center_step_1 = ByteField(0x020287E0)
    daycare_center_step_2 = ByteField(0x020287E4)
    step_counter = ByteField(0x020287EA)
    exp_gain = SignedField(0x02024BEC, size=2)

    _iemfield = PokemonItemField(0)
    item_normal = ArrayField(0x02025C94, 0x14, _iemfield)
    item_keyitem = ArrayField(0x02025CE4, 0x14, _iemfield)
    item_pokeball = ArrayField(0x02025D34, 0x10, _iemfield)
    item_machine = ArrayField(0x02025D74, 0x40, _iemfield)
    item_berry = ArrayField(0x02025E74, 0x2E, _iemfield)
    item_pokeblock = ArrayField(0x02025F2C, 0x28, _iemfield)


class FireLeafJpGlobal(PointerGlobal):
    active_pokemon_count = 0
    active_pokemon = ModelField(0x020241E4, PokemonStructActives)
    stored_pokemon = OffsetsField((0x03005050, 4))
    dust = 0
    decorate = 0
    clock_adjustment = 0
    per_day_random = 0
    safari_balls = ByteField(0x0203990C)
    safari_time = WordField(0x0203990E)
    exp_gain = SignedField(0x02023CB0, size=2)

    class Inner(Model):
        _player_name = Field(0, bytes, 10)
        _player_id = Field(0x0A)
        xor_mask = Field(0x00000AF8)
        money = MaskedField(Field(0x00001234))
        coin = MaskedField(WordField(0x00001238))
        menu = Field(0x00001F89)
        badge = Field(0x00001F8A)
        spray_time = WordField(0x00001FE4)
        daycare_center_step_1 = ByteField(0x00003FAC)
        daycare_center_step_2 = ByteField(0x00004038)
        step_counter = ByteField(0x0000403E)

        _iemfield = PokemonItemField(0)
        item_normal = ArrayField(0x000012B4, 0x2A, _iemfield)
        item_keyitem = ArrayField(0x0000135C, 0x1E, _iemfield)
        item_pokeball = ArrayField(0x000013D4, 0x0D, _iemfield)
        item_machine = ArrayField(0x00001408, 0x3A, _iemfield)
        item_berry = ArrayField(0x000014F0, 0x2B, _iemfield)
        item_pokeblock = None


    inner = ModelPtrField(0x0300504C, Inner)


class FireLeafEnGlobal(PointerGlobal):
    active_pokemon_count = 0
    active_pokemon = ModelField(0x02024284, PokemonStructActives)
    stored_pokemon = OffsetsField((0x03005010, 4))
    dust = 0
    decorate = 0
    clock_adjustment = 0
    per_day_random = 0
    safari_balls = ByteField(0x02039994)
    safari_time = WordField(0x02039996)
    exp_gain = SignedField(0x02023D50, size=2)

    Inner = FireLeafJpGlobal.Inner
    inner = ModelPtrField(0x0300500C, Inner)


class EmeraldJpGlobal(PointerGlobal):
    active_pokemon_count = Field(0x0202418D)
    active_pokemon = ModelField(0x02024190, PokemonStructActives)
    stored_pokemon = OffsetsField((0x03005AF4, 4))
    safari_balls = ByteField(0x02039D18)
    safari_time = WordField(0x02039D1A)
    exp_gain = SignedField(0x02023E94, size=2)

    class Inner(Model):
        _player_name = Field(0, bytes, 10)
        _player_id = Field(0x0A)
        xor_mask = Field(0x000000AC)
        money = MaskedField(Field(0x0000143C))
        coin = MaskedField(WordField(0x00001440))
        dust = WordField(0x000023D8)
        menu = Field(0x00002328)
        decorate = Field(0x000036E0)
        badge = Field(0x00002329)
        clock_adjustment = Field(0x00000098)
        per_day_random = Field(0x00002390)
        spray_time = WordField(0x0000238A)
        daycare_center_step_1 = ByteField(0x00004064)
        daycare_center_step_2 = ByteField(0x000040F0)
        step_counter = ByteField(0x000040F8)
        battle_points_current = WordField(0x00000EB8)
        battle_points_trainer_card = WordField(0x00000EBA)

        _iemfield = PokemonItemField(0)
        item_normal = ArrayField(0x0000150C, 0x1E, _iemfield)
        item_keyitem = ArrayField(0x00001584, 0x1E, _iemfield)
        item_pokeball = ArrayField(0x000015FC, 0x10, _iemfield)
        item_machine = ArrayField(0x0000163C, 0x40, _iemfield)
        item_berry = ArrayField(0x0000173C, 0x46, _iemfield)
        item_pokeblock = ArrayField(0x000017F4, 0x28, _iemfield)
        

    inner = ModelPtrField(0x03005AF0, Inner)


class EmeraldEnGlobal(PointerGlobal):
    active_pokemon_count = Field(0x020244E9)
    active_pokemon = ModelField(0x020244EC, PokemonStructActives)
    stored_pokemon = OffsetsField((0x03005D94, 4))
    safari_balls = ByteField(0x0203A9FC)
    safari_time = WordField(0x0203A076)
    exp_gain = SignedField(0x020241F0, size=2)

    store = ArrayField(0x02005274, 8, ModelField(0, StoreItem))
    area = WordField(0x020322E4)
    wild_pokemon = WordField(0x03007E28)
    furniture_purchase = ByteField(0x03005E3A)
    appearance = ByteField(0x02024A5C)

    Inner = EmeraldJpGlobal.Inner
    inner = ModelPtrField(0x03005D90, Inner)


Globals = {
    'ruby_jp': RubySapphireJpGlobal,
    'ruby_en': RubySapphireEnGlobal,
    'sapphire_jp': RubySapphireJpGlobal,
    'sapphire_en': RubySapphireEnGlobal,
    'fire_jp': FireLeafJpGlobal,
    'fire_en': FireLeafEnGlobal,
    'leaf_jp': FireLeafJpGlobal,
    'leaf_en': FireLeafEnGlobal,
    'emerald_jp': EmeraldJpGlobal,
    'emerald_en': EmeraldJpGlobal,
}

PM_UNKNOWN = 0
PM_SAPPHIRE = 1
PM_RUBY = 2
PM_EMERALD = 3
PM_FIRE = 4
PM_LEAF = 5
LANG_JP = 0
LANG_EN = 1

GAME_VERSON = {
    "POKEMON RUBYAXVJ": (RubySapphireJpGlobal, PM_RUBY, LANG_JP),
    "POKEMON RUBYAXVE": (RubySapphireEnGlobal, PM_RUBY, LANG_EN),
    "POKEMON SAPPAXPJ": (RubySapphireJpGlobal, PM_SAPPHIRE, LANG_JP),
    "POKEMON SAPPAXPE": (RubySapphireEnGlobal, PM_SAPPHIRE, LANG_EN),
    "POKEMON FIREBPRJ": (FireLeafJpGlobal, PM_FIRE, LANG_JP),
    "POKEMON FIREBPRE": (FireLeafEnGlobal, PM_FIRE, LANG_EN),
    "POKEMON LEAFBPGJ": (FireLeafJpGlobal, PM_LEAF, LANG_JP),
    "POKEMON LEAFBPGE": (FireLeafEnGlobal, PM_LEAF, LANG_EN),
    "POKEMON EMERBPEJ": (EmeraldJpGlobal, PM_EMERALD, LANG_JP),
    "POKEMON EMERBPEE": (EmeraldEnGlobal, PM_EMERALD, LANG_EN),
}

GAME_ENCRYPTED = {
    "pokemon red version": (FireLeafJpGlobal, PM_FIRE, LANG_JP),
    "pokemon green version": (FireLeafJpGlobal, PM_LEAF, LANG_JP),
    "pokemon emerald version": (EmeraldJpGlobal, PM_EMERALD, LANG_JP),
}