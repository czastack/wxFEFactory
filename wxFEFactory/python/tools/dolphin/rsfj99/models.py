from lib.hack.model import Model, Field


class Ram(Model):
    hp = Field(0x00E464D8)
    max_hp = Field(0x00E464DC)