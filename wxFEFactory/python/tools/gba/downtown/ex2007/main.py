from ..main import ExTool


class Tool(ExTool):
    from . import models, datasets
    PERSON_ADDR_START = 0x02000594