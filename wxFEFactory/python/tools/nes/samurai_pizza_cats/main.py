from ..base import SimpleNesHack


class Main(SimpleNesHack):
    fields = (
        (0x003F, "血量", 1, 10),
        (0x0040, "能量", 1, 0xFF),
        (0x0044, "生命"),
        (0x0041, "援助", 1, 0xC0),
        (0x003d, "忍术(1-3)"),
        (0x005d, "关卡"),
    )

    def pull_through(self, _=None):
        self.set_max("血量")
        self.set_max("能量")
        self.set_max("援助")