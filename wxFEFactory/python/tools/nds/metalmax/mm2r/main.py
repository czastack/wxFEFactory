from ..main import MetalMaxHack


class Tool(MetalMaxHack):
    from . import models, datasets

    @property
    def chariot_equips(self):
        from . import chariot_equips
        return chariot_equips
    
