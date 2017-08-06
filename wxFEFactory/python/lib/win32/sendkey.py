from .keys import getVK
from fefactory_api import auto


def TextVK(text):
    ret = []
    for s in text:
        keycode = getVK(s)
        if keycode:
            ret.append(auto.VKey(keycode))
            ret.append(auto.VKey(keycode, True))
    return ret