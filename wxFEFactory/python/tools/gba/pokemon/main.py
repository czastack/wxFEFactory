from ..base import BaseGbaHack
from lib.hack.forms import Group, Groups, StaticGroup, ModelInput, ModelSelect, ModelFlagWidget
from lib.win32.keys import VK
from lib.exui.components import Pagination
from fefactory_api import ui
from . import models, datasets


class PMHack(BaseGbaHack):
    BACKPACK_PAGE_LENGTH = 10

    def __init__(self):
        super().__init__()
        self._globalins = None
        self._pokemonins = models.Pokemon(0, self.handler)
        self.active_pokemon_index = 0
        self.active_pokemon_ins = None

    def render_main(self):
        with Group("global", "全局", self._global, horizontal=False):
            self.render_global()

        self.lazy_group(Group("shop", "商店购物", self._global), self.render_shop)
        self.backpack_group = Group("store", "背包", self._global, hasheader=True, cols=4)
        self.lazy_group(self.backpack_group, self.render_backpack)
        self.pokemon_group = StaticGroup("宝可梦")
        self.lazy_group(self.pokemon_group, self.render_pokemon)

    def render_global(self):
        datasets = self.datasets

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

    def render_shop(self):
        datasets = self.datasets
        with ModelSelect.choices_cache:
            for i in range(8):
                ModelSelect("store.%d.item" % i, "商品%d" % (i + 1), choices=datasets.ITEMS)

    def render_backpack(self):
        datasets = self.datasets
        with self.backpack_group.header:
            ui.RadioBox("类型", className="fill", choices=datasets.BACKPACK_LABELS, onselect=self.on_backpack_swith)
        for i in range(self.BACKPACK_PAGE_LENGTH):
            ModelSelect("backpack_items.%d+backpack_offset.item" % i, "", choices=datasets.ITEMS)
            ModelInput("backpack_items.%d+backpack_offset.quantity" % i, "数量")
        with self.backpack_group.footer:
            self.backpack_pageview = Pagination(self.on_backpack_page, self.BACKPACK_PAGE_LENGTH)

    def render_pokemon(self):
        # pokemon = self.weak._pokemon
        active_pokemon = self._active_pokemon

        ui.RadioBox("带着的宝可梦", className="expand", choices=tuple(str(i) for i in range(1, 7)),
            onselect=self.on_active_pokemo_swith)

        with Groups(None, self.weak.onNotePageChange):
            with Group("basic", "基本", active_pokemon, cols=4):
                ModelInput("breedInfo.bIntimate", "亲密度", spin=True, max=255)
                ModelSelect("breedInfo.wBreed", "种族", choices=self.datasets.POKEMONS)
                ModelInput("Header.dwChar", "性格值", hex=True)
                ModelInput("Header.dwID", "ID", hex=True)
                ModelSelect("personality", "性格", choices=self.datasets.PERSONALITYS,
                    onselect=self.on_personality_select)
                ui.Text("性格描述", className="vcenter")
                self.personality_desc = ui.Text("", className="vcenter")
            with Group("basic", "能力", active_pokemon):
                pass
            with Group("basic", "技能", active_pokemon):
                pass
            with Group("basic", "缎带", active_pokemon):
                pass
            with Group("basic", "其它", active_pokemon):
                pass

        with ui.Horizontal(className="expand"):
            ui.Button("读入", className="btn_sm", onclick=self.read_active_pokemon)
            ui.Button("写回", className="btn_sm", onclick=self.write_active_pokemon)

    def onattach(self):
        super().onattach()
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
