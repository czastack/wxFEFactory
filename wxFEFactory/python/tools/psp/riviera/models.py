from lib.hack.models import Model, Field, ByteField, WordField, ArrayField, ModelField


class Global(Model):
    tp = ByteField(0x0126C341)
