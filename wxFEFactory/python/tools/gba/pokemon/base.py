from ..base import BaseGbaHack
from lib.hack.forms import Group, StaticGroup, ModelInput, ModelSelect, ModelFlagWidget
from lib.win32.keys import VK
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
        self.active_pokemon_index = 0
        self.active_pokemon_ins = None

    def render_main(self):
        datasets = self.datasets
        this = self.weak
        # pokemon = self.weak._pokemon
        active_pokemon = this._active_pokemon
        with Group("global", "全局", self._global, horizontal=False):
            ModelInput("money", "金钱", spin=True)
            ModelInput("coin", "游戏币", spin=True)
            ModelInput("dust", "宝石版火山灰", spin=True)
            ModelInput("spray_time", "喷雾剂剩余步数", spin=True)
            ModelInput("safari_time", "狩猎区剩余步数", spin=True)
            ModelInput("battle_points_current", "战斗点数（仅绿宝石）", spin=True)
            ModelInput("battle_points_trainer_card", "训练员卡上的战斗点数（仅绿宝石）", spin=True)

            ModelSelect("area", "地点瞬移", choices=datasets.AREA_LABELS, values=datasets.AREA_VALUES)
            ModelSelect("furniture_purchase", "家具购买", choices=datasets.FURNITURES)
            ModelSelect("appearance", "性别外形", choices=datasets.APPEARANCE)
            # ModelSelect("wild_pokemon", "遇到精灵", choices=datasets.POKEMONS)

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
                self.backpack_pageview = Pagination(this.on_backpack_page, self.BACKPACK_PAGE_LENGTH)
            self.backpack_group = backpack_group

        with StaticGroup("宝可梦") as pokemon_group:
            ui.RadioBox("带着的宝可梦", className="expand", choices=tuple(str(i) for i in range(1, 7)), onselect=self.on_active_pokemo_swith)

            with ui.Notebook(className="fill") as book:
                with Group("basic", "基本", active_pokemon):
                    ModelInput("breedInfo.bIntimate", "亲密度", spin=True, max=255)
                    ModelSelect("breedInfo.wBreed", "种族", choices=datasets.POKEMONS)
                    ModelInput("Header.dwChar", "性格值", hex=True)
                    ModelInput("Header.dwID", "ID", hex=True)
                    ModelSelect("personality", "性格", choices=datasets.PERSONALITYS, onselect=this.on_personality_select)
                    ui.Text("性格描述")
                    self.personality_desc = ui.Text("")
                with Group("basic", "能力", active_pokemon):
                    pass
                with Group("basic", "技能", active_pokemon):
                    pass
                with Group("basic", "缎带", active_pokemon):
                    pass
                with Group("basic", "其它", active_pokemon):
                    pass

            with ui.Horizontal(className="expand"):
                ui.Button("读入", className="btn_sm", onclick=this.read_active_pokemon)
                ui.Button("写回", className="btn_sm", onclick=this.write_active_pokemon)
            self.pokemon_group = pokemon_group

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

    def read_active_pokemons(self):
        pokemons = self._globalins.active_pokemon.tolocal()
        for pokemon in pokemons.content:
            pokemon.pmStruct.attach()
            pokemon.pmStruct.Decode()
        return pokemons

    def read_active_pokemon(self, _=None):
        active_pokemon = self._globalins.active_pokemon.content[self.active_pokemon_index]
        self.active_pokemon_ins = pokemon = active_pokemon.pmStruct.tolocal()
        pokemon.attach()
        pokemon.Decode()
        return pokemon

    def write_active_pokemon(self, _=None):
        pokemon = self.active_pokemon_ins
        if pokemon:
            temp = pokemon.tolocal()
            temp.bEncoded = False
            temp.Encode()
            self._globalins.active_pokemon.content[self.active_pokemon_index].pmStruct = temp


    def _active_pokemon(self):
        return self.active_pokemon_ins or self.read_active_pokemon()

    # pokemon = property(_pokemon)
    # active_pokemons = property(_active_pokemons)

    def on_backpack_page(self, page):
        """背包物品切换页"""
        self._globalins.backpack_offset = (page - 1) * self.BACKPACK_PAGE_LENGTH
        self.backpack_group.read()

    def on_backpack_swith(self, view):
        self._globalins.backpack_type = self.datasets.BACKPACK_KEYS[view.index]
        self.backpack_pageview.asset_total(self._globalins.backpack_items.length, self.BACKPACK_PAGE_LENGTH)
        self.backpack_group.read()

    def on_active_pokemo_swith(self, view):
        self.active_pokemon_index = view.index
        self.read_active_pokemon()
        self.pokemon_group.read()

    def on_personality_select(self, view):
        personality = view.index
        b = [1, 1, 1, 1, 1]
        b[personality // 5] += 1
        b[personality % 5] -= 1
        sz = ("－", "　", "＋")
        desc = "攻击:{}防御:{}敏捷:{}特攻:{}特防:{}".format(*(sz[i] for i in b))
        self.personality_desc.label = desc