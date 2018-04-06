from ..main import BaseGSTool


class Tool(BaseGSTool):
    from . import models, datasets, coords
    PERSON_ADDR_START = 0x02000520
