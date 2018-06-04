from ..base import SimpleNesHack


class Tool(SimpleNesHack):
    fields = (
        (0x041E, "1P体力", 1, 0x7F),
        (0x041F, "2P体力", 1, 0x7F),
        (0x0420, "敌A体力"),
        (0x0421, "敌B体力"),
        (0x0432, "1P人数", 1, 9),
        (0x0433, "2P人数", 1, 9),
        (0x03CC, "1P闪光无敌(1)"),
        (0x03CD, "2P闪光无敌(1)"),
    )

    def pull_through(self, _=None):
        self.set_max("1P体力")
        self.set_max("2P体力")