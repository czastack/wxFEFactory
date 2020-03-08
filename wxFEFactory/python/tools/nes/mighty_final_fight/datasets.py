from lib import utils


PLAYERS = ("卡迪", "向一", "杰克")


ENEMYS = (
    (0x2020, "女流氓"),
    (0x2121, "小兵甲"),
    (0x2222, "小兵乙"),
    (0x2323, "拳击手"),
    (0x2424, "刀手"),
    (0x2525, "壮汉"),
    (0x8080, "BOSS1"),
    (0x8181, "BOSS2"),
    (0x9090, "BOSS3"),
    (0x8383, "BOSS4"),
    (0x7474, "BOSS5"),
)


ENEMY_LABELS, ENEMY_VALUES = utils.split_tuple_reverse(ENEMYS)
