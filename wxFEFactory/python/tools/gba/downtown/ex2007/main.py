from ..main import ExTool


class Main(ExTool):
    from . import models, datasets
    PERSON_ADDR_START = 0x02000594