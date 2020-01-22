from ..gtaiv_hack.main import Main as GTAIVBaseTool


class Main(GTAIVBaseTool):
    WINDOW_NAME = 'EFLC'
    from .datasets import WEAPON_LIST, SLOT_NO_AMMO
