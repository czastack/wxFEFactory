from ..base import BaseGbaHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelCoordWidget, ModelFlagWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
from . import models, datasets
import fefactory_api
ui = fefactory_api.ui


class BasePMHack(BaseGbaHack):
    BACKPACK_PAGE_LENGTH = 10

    def __init__(self):
        super().__init__()
        self._globalins = None
        self._pokemonins = models.Pokemon(0, self.handler)
        self.pokemon_index = 0

    def render_main(self):
        datasets = self.datasets
        pokemon = self.weak._pokemon
        with Group("global", "全局", self._global, horizontal=False):
            ModelInput("money", "金钱", spin=True)
            ModelInput("coin", "游戏币", spin=True)
            ModelInput("dust", "宝石版火山灰", spin=True)
            ModelInput("spray_time", "喷雾剂剩余步数", spin=True)
            ModelInput("safari_time", "狩猎区剩余步数", spin=True)
            ModelInput("battle_points_current", "战斗点数（仅绿宝石）", spin=True)
            ModelInput("battle_points_trainer_card", "训练员卡上的战斗点数（仅绿宝石）", spin=True)

            ModelSelect("area", "地点瞬移", choices=datasets.AREA_LABELS, values=datasets.AREA_VALUES)
            ModelSelect("wild_pokemon", "遇到精灵", choices=datasets.POKEMONS)
            ModelSelect("furniture_purchase", "家具购买", choices=datasets.FURNITURES)
            ModelSelect("appearance", "性别外形", choices=datasets.APPEARANCE)

        with Group("store", "商店购物", self._global):
            for i in range(8):
                ModelSelect("store.%d.item" % i, "商品%d" % (i + 1), choices=datasets.ITEMS)

        with Group("store", "背包", self._global, hasheader=True, cols=4) as backpack_group:
            with backpack_group.header:
                ui.RadioBox("类型", className="fill", choices=datasets.BACKPACK_LABELS, onselect=self.on_backpack_swith)
            for i in range(self.BACKPACK_PAGE_LENGTH):
                ModelSelect("backpack_items.%d+backpack_offset.item" % i, "", choices=datasets.ITEMS)
                ModelInput("backpack_items.%d+backpack_offset.quantity" % i, "数量")
            with backpack_group.footer:
                self.backpack_pageview = Pagination(self.weak.on_backpack_page, self.BACKPACK_PAGE_LENGTH)
            self.backpack_group = backpack_group


    def onattach(self):
        rom_title = self.handler.getRomTitle()

        item = models.GAME_VERSON.get(rom_title, None)
        if item is None and rom_title == "YJencrypted":
            szGameVersion = self.handler.read(0x08000108, bytes, 32).decode()
            item = models.GAME_ENCRYPTED.get(szGameVersion, None)

        if item:
            self._globalins = item[0](0, self.handler)
            self.pm_version = item[1]
            self.lang = item[2]
            # 初始化一些背包参数
            self._globalins.backpack_offset = 0

    def _global(self):
        return self._globalins

    def on_pokemon_change(self, lb):
        self.pokemon_index = lb.index

    def _pokemon(self):
        pokemon_addr = self.PERSON_ADDR_START + self.pokemon_index * models.Pokemon.SIZE
        self._pokemonins.addr = pokemon_addr
        return self._pokemonins

    def _active_pokemons(self):
        pokemons = self._globalins.active_pokemon.to_local()
        for pokemon in pokemons.content:
            pokemon.pmStruct.attach()
            pokemon.pmStruct.Decode()
        return pokemons

    pokemon = property(_pokemon)
    active_pokemons = property(_active_pokemons)

    def on_backpack_page(self, page):
        """背包物品切换页"""
        self._globalins.backpack_offset = (page - 1) * self.BACKPACK_PAGE_LENGTH
        self.backpack_group.read()

    def on_backpack_swith(self, view):
        self._globalins.backpack_type = self.datasets.BACKPACK_KEYS[view.index]
        self.backpack_pageview.asset_total(self._globalins.backpack_items.length, self.BACKPACK_PAGE_LENGTH)
        self.backpack_group.read()