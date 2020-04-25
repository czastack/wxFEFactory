VERSIONS = ('steam', 'codex')


# (name, label)
INVENTORYS = {
    # Ammo
    'MagnumBullet': '44麦林枪弹药',
    'BurnerBullet': '燃烧器燃料',
    'HandgunBulletL': '增强的手枪弹药',
    'FlameBulletS': '火焰弹',
    'HandgunBullet': '手枪弹药',
    'UnlimitedAmmo': '无限子弹',
    'MachineGunBullet': '机枪子弹',
    'AcidBulletS': '神经毒素弹',
    'ShotgunBullet': '猎枪子弹',

    # Body Parts
    'HandCutOff': '伊森的手',
    'EthanLeg': '伊森的脚',

    # Coins
    'Coin': '古钱币',
    'PowerUpCoin01A': 'Assault Coin',
    'GoodLuckCoinA': 'Defense Coin',
    'PowerUpCoin01B': 'Iron Defense Coin',

    # Crafting
    'ChemicalS': '化学液体',
    'Gunpowder': '火药',
    'RepairKit': '修理包',
    'ChemicalL': 'Seperating Agent',
    'Alcohol': '固体燃料',
    'ChemicalM': '强烈化学液体',
    'Flower': '补养品',

    # Documents/Books
    'MailMia': '米娅发送的电子邮件',
    'MiaDriversLicense': '驾照',
    'ProposalBookFf': '节目企划书',

    # Keys
    'CabinKey': 'Captains Cabin Locker Key',
    'EthanCarKey': 'Car Key',
    'SpareKey': '腐蚀剂',
    'TalismanKey': '乌鸦钥匙',
    'WorkroomKey': '解剖室钥匙',
    '3CrestKeyA': '蓝色狗头',
    '3CrestKeyC': '红色狗头',
    '3CrestKeyB': '白色狗头',
    'FloorDoorKey': 'Hatch Key',
    'LucasCardKey': '蓝色钥匙卡',
    'LucasCardKey2': '红色钥匙卡',
    'CylinderKey': '开锁器',
    'EntranceHallKey': '牛的雕像',
    'MorgueKey': '蝎子钥匙',
    'MasterKey': '蛇钥匙',

    # Maps (Treasure Maps)
    'TreasureMap03': '宝藏照片 (Master Bedroom)',
    'TreasureMap01': '宝藏照片 (Morgue)',
    'TreasureMap02': '宝藏照片 (老房子)',

    # Medicine
    'RemedyM': '急救药',
    'RemedyL': '药性强的急救药',
    'Herb': '药草',
    'EyeDrops': '兴奋剂',

    # Mission Items
    'Battery': 'Battery',
    'ChainCutter': 'Bolt Cutters',
    'BrokenHandgun_M19': 'Broken Handgun',
    'BrokenShotgun_DB': 'Broken Shotgun',
    'BurnerPartsA': 'Burner Grip',
    'BurnerPartsB': 'Burner Nozzle',
    'PendulumClock': 'Clock Pendulum',
    'Crank': 'Crank',
    'SerumMaterialA': 'D系列手臂',
    'SerumMaterialB': 'D系列头部',
    'SerumTypeE': 'E-Necrotoxin',
    'EvelynRadar1': '奇怪的瓶子',
    'EvelynRadar2': '伊芙琳组织样本 (1)',
    'EvelynRadar3': '伊芙琳组织样本 (2)',
    'EvelynRadar4': '伊芙琳组织样本 (3)',
    'Fuse': 'Fuse',
    'FuseCh4': '通用保险丝',
    'Lantern': 'Lantern',
    'EvOpener': '扳手',
    'ToyShotgun': 'Model Shotgun',
    'EvCable': 'Power Cable',
    'SerumComplete': 'SerumComplete',
    'SilhouettePazzlePieceOldHouse': '石雕像',
    'Timebomb': '定时炸弹',
    'DummyAxe': '玩具斧',
    'SilhouettePazzlePiece': '木雕像',

    # Mission Items (HappyBirthday)
    'Balloonbomb': '气球',
    'Candle': '蜡烛',
    'Glasses': '望远镜',
    'ScrewFinger': '假手指',
    'Quill': '羽毛笔',
    'Valve': '阀门手柄',
    'SpringCoil': '上发条钥匙',

    # Other
    'SupplyBoxA': 'Box from Mia (Closed)',
    'SupplyBoxOpenedA': 'Box from Mia (Opened)',
    'SaveTape': 'Cassette Tape (Save)',

    # Player Upgrades
    'Depressant': '松弛剂 (提高上弹速度)',
    'Stimulant': '类固醇 (提高血值上限)',
    'BookDefence01': 'The Secrets Of Defence',
    'AlphaGrass': 'X-ray Glasses',

    # Videotapes
    'FoundFootage000': '"废弃房子录像"',
    'FoundFootage020': 'Derelict House Footage (2)',
    'FoundFootage010': 'FoundFootage010',
    'FoundFootage040': '“生日快乐”录像带',
    'FoundFootage030': '“米娅”录像带',
    'FoundFootage050': '旧的录像带',

    # Weapons - Firearms
    'Magnum': '44麦林枪',
    'Handgun_Albert': '埃尔伯特01',
    'Handgun_Albert_Reward': '埃尔伯特01R',
    'Burner': '燃烧器',
    'Handgun_G17': 'G17手枪',
    'GrenadeLauncher': '榴弹发射器',
    'Handgun_M19': 'M19手枪',
    'Shotgun_DB': 'M21猎枪',
    'Shotgun_M37': 'M37猎枪',
    'Handgun_MPM': 'MPM手枪',
    'MachineGun': 'P19机枪',

    # Weapons - Melee
    'HandAxe': '斧头',
    'ChainSaw': '电锯',
    'CircularSaw': '圆锯',
    'Bar': '撬棍',
    'Knife': '刀子',
    'MiaKnife': '露营刀',

    # Weapons - Thrown
    'LiquidBomb': '遥控炸弹',

    # 佐伊的结局
    'NumaItem000': '拳击手人偶',
    'NumaItem001': '冠军人偶',
    'NumaItem003': '乔的求生指南',
    'NumaItem004': '化学液体',
    'NumaItem009': '废金属',
    'NumaItem010': '树枝',
    'NumaItem013': '急救药',
    'NumaItem022': '小生物',
    'NumaItem030': 'E型感染治疗药',
    'NumaItem031': 'E型感染治疗药(满)',
    'NumaItem071': '赤手空拳',
    'NumaItem072': '投掷用小刀',
    'CH9_WP000': 'AMG-78a',
    'CH9_WP001': 'AMG-78',
    'CH9_WP003': 'M21猎枪',
    'CH9_WP004': '投掷用长矛',
    'CH9_WP005': '定点炸弹',
}

INVENTORY_LABELS = tuple(INVENTORYS.values())
INVENTORY_VALUES = tuple(INVENTORYS.keys())
