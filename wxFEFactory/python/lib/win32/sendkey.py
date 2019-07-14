from .keys import VK
from pyapi import auto


def TextVK(text):
    ret = []
    for s in text:
        keycode = VK(s)
        if keycode:
            ret.append(auto.VKey(keycode))
            ret.append(auto.VKey(keycode, True))
    return ret
