from ctypes.wintypes import LONG, DWORD, WORD
from .keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT, MOD_WIN
import ctypes
import time

ULONG_PTR = ctypes.POINTER(DWORD)

KEYUP    = 0x0002
UNICODE  = 0x0004
SCANCODE = 0x0008


class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ('wVk', WORD),
        ('wScan', WORD),
        ('dwFlags', DWORD),
        ('time', DWORD),
        ('dwExtraInfo', ULONG_PTR)
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", DWORD),
        ("wParamL", WORD),
        ("wParamH", WORD)
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", LONG),
        ("dy", LONG),
        ("mouseData", DWORD),
        ("dwFlags", DWORD),
        ("time",DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]


class InputUnion(ctypes.Union):
    _fields_ = [
        ("mi", MouseInput),
        ("ki", KeyBdInput),
        ("hi", HardwareInput)
    ]


class Input(ctypes.Structure):
    _fields_ = [
        ("type", DWORD),
        ("union", InputUnion)
    ]


def sendKey(vk, scan, codeType, keyUp=False):
    if keyUp:
        codeType |= KEYUP
    if codeType is UNICODE:
        vk = 0
    extra = ctypes.pointer(ctypes.c_ulong(0))
    union = InputUnion()
    union.ki = KeyBdInput(vk, scan, codeType, 0, extra)
    inp = Input(ctypes.c_ulong(1), union)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))


def sendVKey(keyCode, keyUp=False):
    sendKey(keyCode, 0, 0, keyUp)


def sendScan(keyCode, codeType=UNICODE, keyUp=False):
    sendKey(0, keyCode, codeType, keyUp)


def sendComb(mod, keyCode):
    """
    usage: sendComb(MOD_CONTROL, getVK('v'))
    """
    
    if mod & MOD_SHIFT:
        sendVKey(0x10)
    if mod & MOD_CONTROL:
        sendVKey(0x11)
    if mod & MOD_ALT:
        sendVKey(0x12)

    sendVKey(keyCode)
    sendVKey(keyCode, keyUp=True)

    if mod & MOD_SHIFT:
        sendVKey(0x10, keyUp=True)
    if mod & MOD_CONTROL:
        sendVKey(0x11, keyUp=True)
    if mod & MOD_ALT:
        sendVKey(0x12, keyUp=True)


# def sendVKey(keyCode, keyUp=False):
#     keyCode = ctypes.windll.user32.MapVirtualKeyA(keyCode, 0)
#     sendScan(keyCode, SCANCODE, keyUp)


if __name__ == '__main__':
    time.sleep(1)
    sendVKey(0x30)
    sendVKey(0x30, keyUp=True)
    sendScan(0x30)
    sendScan(0x30, keyUp=True)
    sendScan(0x30, SCANCODE)
    sendScan(0x30, SCANCODE, keyUp=True)