from ..gtaiv_hack.main import Tool as GTAIVBaseTool

class Tool(GTAIVBaseTool):
    WINDOW_NAME = 'EFLC'
    from .datasets import WEAPON_LIST, SLOT_NO_AMMO