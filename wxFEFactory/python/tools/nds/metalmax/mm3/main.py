from lib.hack.forms import Group, ModelCheckBox, ModelInput, ModelSelect
from ..main import MetalMaxHack


class Main(MetalMaxHack):
    from . import models, datasets

    @property
    def chariot_equips(self):
        from . import chariot_equips
        return chariot_equips

    def render_character_ext(self):
        datasets = self.datasets
        for i in range(self.character.skills.length):
            ModelInput("skills.%d.item" % i, "技能%d种类" % (i + 1))
            ModelInput("skills.%d.count" % i, "次数")

    def render_global_ext(self):
        datasets = self.datasets
        ModelInput("game_time")
        ModelInput("reward")
        ModelInput("fame")
        ModelInput("move_speed")
        ModelSelect("after_money_rate", choices=datasets.RATE, values=datasets.RATE_VALUES)
        for name in ("quick_move", "through_wall", "no_battle", "must_winning", "tool_count_keep", "ammo_keep",
                "weight_zero", "equip_limit_remove", "without_material", "drop_item_three_star", "enemy_flash",
                "skill_count_keep", "can_go_here", "use_humen_weapon_1", "use_humen_weapon_2",
                "buy_chariot_item_three_star", "can_buy_not_for_sale", "can_change_even_overweight",
                "can_always_special_bullet", "skill_count_keep"):
            ModelCheckBox(name)

    def render_ext(self):
        self.lazy_group(Group("favorability", "好感度", self._global), self.render_favorability)
        self.lazy_group(Group("wanted", "赏金首", self._global, cols=4), self.render_wanted)

    def render_favorability(self):
        datasets = self.datasets
        for i, name in enumerate(datasets.ORGANIZATION):
            ModelInput("favorability.%d" % i, name)

    def render_wanted(self):
        datasets = self.datasets
        with ModelSelect.choices_cache:
            for i, name in enumerate(datasets.WANTED_LIST):
                ModelSelect("wanted_status.%d" % i, name, choices=datasets.WANTED_STATUS)
