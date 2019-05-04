from lib.hack.forms import ModelCheckBox, ModelInput, ModelSelect
from ..main import MetalMaxHack


class Main(MetalMaxHack):
    from . import models, datasets

    @property
    def chariot_equips(self):
        from . import chariot_equips
        return chariot_equips

    def render_global_ext(self):
        datasets = self.datasets
        ModelInput("game_turn")
        ModelInput("game_time")
        ModelInput("after_money")
        ModelInput("after_exp")
        ModelInput("posx")
        ModelInput("posy")
        ModelSelect("difficulty", choices=datasets.DIFFICULTY)
        ModelSelect("after_money_rate", choices=datasets.RATE, values=datasets.RATE_VALUES)
        ModelSelect("after_exp_rate", choices=datasets.RATE, values=datasets.RATE_VALUES)
        for name in ("quick_switch", "quick_move", "through_wall", "no_battle", "must_winning", "tool_count_keep",
                "ammo_keep", "level_up_max", "weight_zero", "equip_limit_remove", "without_material", "twin_engines",
                "drop_item_three_star", "must_drop_item", "must_first", "allfax", "allmap", "enemy_flash",
                "can_use_other_skill", "must_critical_hit"):
            ModelCheckBox(name)
