from ..base import BaseGbaHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelCoordWidget, ModelFlagWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
from . import models
import fefactory_api
ui = fefactory_api.ui


class BasePMHack(BaseGbaHack):

    def __init__(self):
        super().__init__()
        self._global = None
        self._pokemonins = models.Pokemon(0, self.handler)
        self.pokemon_index = 0

    def render_main(self):
        datasets = self.datasets
        pokemon = self.weak._pokemon
        with Group("global", "全局", self._global):
            ModelInput("money", "金钱")
            ModelSelect("store", "商店购物", choices=datasets.ITEMS)
            ModelSelect("area", "地点瞬移", choices=datasets.AREA_LABELS, values=datasets.AREA_VALUES)
            ModelSelect("wild_pokemon", "遇到精灵", choices=datasets.POKEMONS)
            ModelSelect("furniture_purchase", "家具购买", choices=datasets.FURNITURES)
            ModelSelect("appearance", "性别外形", choices=datasets.APPEARANCE)

        with Group("store", "商店购物", self._global):
            for i in range(8):
                ModelSelect("store.%d.item" % i, "商品%d" % (i + 1), choices=datasets.ITEMS)

    def onattach(self):
        rom_title = self.handler.getRomTitle()

        item = models.GAME_VERSON.get(rom_title, None)
        if item is None and rom_title == "YJencrypted":
            szGameVersion = self.handler.read(0x08000108, bytes, 32).decode()
            item = models.GAME_ENCRYPTED.get(szGameVersion, None)

        if item:
            self._global = item[0](0, self.handler)
            self.pm_version = item[1]
            self.lang = item[2]

    def on_pokemon_change(self, lb):
        self.pokemon_index = lb.index

    def _pokemon(self):
        pokemon_addr = self.PERSON_ADDR_START + self.pokemon_index * models.Pokemon.SIZE
        self._pokemonins.addr = pokemon_addr
        return self._pokemonins

    def _active_pokemons(self):
        pokemons = self._global.active_pokemon.to_local()
        for pokemon in pokemons.content:
            pokemon.pmStruct.attach()
            pokemon.pmStruct.Decode()
        return pokemons

    pokemon = property(_pokemon)
    active_pokemons = property(_active_pokemons)