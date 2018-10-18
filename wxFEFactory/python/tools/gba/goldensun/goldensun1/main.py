from ..main import GSHack


class Main(GSHack):
    from . import models, datasets, coords
    PERSON_ADDR_START = 0x02000500
