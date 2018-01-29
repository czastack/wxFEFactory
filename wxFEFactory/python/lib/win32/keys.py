MOD_ALT      = 0x0001
MOD_CONTROL  = 0x0002
MOD_SHIFT    = 0x0004
MOD_WIN      = 0x0008
MOD_LEFT     = 0x8000
MOD_RIGHT    = 0x4000
MOD_ON_KEYUP = 0x0800

VK_CODE = {
    'BACK': 8,
    'TAB': 9,
    'ENTER': 13,
    'RETURN': 13,
    'CAPSLOCK': 20,
    'ESCAPE': 27,
    'SPACE': 32,
    ' ': 32,
    'PAGEUP': 33,
    'PAGEDOWN': 34,
    'END': 35,
    'HOME': 36,
    'LEFT': 37,
    'UP': 38,
    'RIGHT': 39,
    'DOWN': 40,
    'PRINT_SCREEN': 44,
    'INS': 45,
    'DEL': 46,
    'LWIN': 91,
    'RWIN': 92,
    'NUMPAD0': 96,
    'NUMPAD1': 97,
    'NUMPAD2': 98,
    'NUMPAD3': 99,
    'NUMPAD4': 100,
    'NUMPAD5': 101,
    'NUMPAD6': 102,
    'NUMPAD7': 103,
    'NUMPAD8': 104,
    'NUMPAD9': 105,
    'MULTIPLY': 106,
    'ADD': 107,
    'SEPARATOR': 108,
    'SUBTRACT': 109,
    'DECIMAL': 110,
    'DIVIDE': 111,
    'F1': 112,
    'F2': 113,
    'F3': 114,
    'F4': 115,
    'F5': 116,
    'F6': 117,
    'F7': 118,
    'F8': 119,
    'F9': 120,
    'F10': 121,
    'F11': 122,
    'F12': 123,
    'NUMLOCK': 144,
    '+': 187,
    ',': 188,
    '-': 189,
    '.': 190,
    '/': 191,
    '`': 192,
    ';': 186,
    '[': 219,
    '\\': 220,
     ']': 221,
    "'": 222,
    '`': 192 
}


WXK_CODE = {
    'BACK': 8,
    'TAB': 9,
    'SPACE': 32,
    'DELETE': 127,
    'ENTER': 13,
    'RETUEN': 13,
    'ESCAPE': 27,
    'LBUTTON': 301,
    'RBUTTON': 302,
    'CANCEL': 303,
    'MBUTTON': 304,
    'CLEAR': 305,
    'SHIFT': 306,
    'ALT': 307,
    'CONTROL': 308,
    'MENU': 309,
    'PAUSE': 310,
    'CAPITAL': 311,
    'END': 312,
    'HOME': 313,
    'LEFT': 314,
    'UP': 315,
    'RIGHT': 316,
    'DOWN': 317,
    'SELECT': 318,
    'PRINT': 319,
    'EXECUTE': 320,
    'SNAPSHOT': 321,
    'INSERT': 322,
    'HELP': 323,
    'NUMPAD0': 324,
    'NUMPAD1': 325,
    'NUMPAD2': 326,
    'NUMPAD3': 327,
    'NUMPAD4': 328,
    'NUMPAD5': 329,
    'NUMPAD6': 330,
    'NUMPAD7': 331,
    'NUMPAD8': 332,
    'NUMPAD9': 333,
    'MULTIPLY': 334,
    'ADD': 335,
    'SEPARATOR': 336,
    'SUBTRACT': 337,
    'DECIMAL': 338,
    'DIVIDE': 339,
    'F1': 340,
    'F2': 341,
    'F3': 342,
    'F4': 343,
    'F5': 344,
    'F6': 345,
    'F7': 346,
    'F8': 347,
    'F9': 348,
    'F10': 349,
    'F11': 350,
    'F12': 351,
    'NUMLOCK': 364,
    'SCROLL': 365,
    'PAGEUP': 366,
    'PAGEDOWN': 367,
    'NUMPAD_SPACE': 368,
    'NUMPAD_TAB': 369,
    'NUMPAD_ENTER': 370,
    'NUMPAD_F1': 371,
    'NUMPAD_F2': 372,
    'NUMPAD_F3': 373,
    'NUMPAD_F4': 374,
    'NUMPAD_HOME': 375,
    'NUMPAD_LEFT': 376,
    'NUMPAD_UP': 377,
    'NUMPAD_RIGHT': 378,
    'NUMPAD_DOWN': 379,
    'NUMPAD_PAGEUP': 380,
    'NUMPAD_PAGEDOWN': 381,
    'NUMPAD_END': 382,
    'NUMPAD_BEGIN': 383,
    'NUMPAD_INSERT': 384,
    'NUMPAD_DELETE': 385,
    'NUMPAD_EQUAL': 386,
    'NUMPAD_MULTIPLY': 387,
    'NUMPAD_ADD': 388,
    'NUMPAD_SEPARATOR': 389,
    'NUMPAD_SUBTRACT': 390,
    'NUMPAD_DECIMAL': 391,
    'NUMPAD_DIVIDE': 392,
    'WINDOWS_LEFT': 393,
    'WINDOWS_RIGHT': 394,
    'WINDOWS_MENU' : 395,
}


def getVK(name):
    """根据名称获取windows的keyCode"""
    if len(name) == 1:
        code = ord(name)
        # 0~9, A~Z
        if 48 <= code <= 57 or 65 <= code <= 90:
            return code
        # a~z
        elif 97 <= code <= 122:
            return code - 32
    return VK_CODE.get(name.upper(), 0)


def getVKName(code, mod=None):
    """根据windows的keyCode和modifiers得到名称"""
    # 0~9, A~Z
    if 48 <= code <= 57 or 65 <= code <= 90:
        name = chr(code)
    else:
        for key in VK_CODE:
            if VK_CODE[key] == code:
                name = key
        else:
            return ''
    if mod:
        if mod & MOD_ALT:
            name = 'alt+' + name
        if mod & MOD_SHIFT:
            name = 'shift+' + name
        if mod & MOD_CONTROL:
            name = 'ctrl+' + name
        if mod & MOD_WIN:
            name = 'win+' + name
    return name


def isWXKMod(code):
    """判断一个keyCode是否是ctrl, shift, alt"""
    return code == WXK_CODE['SHIFT'] or code == WXK_CODE['ALT'] or code == WXK_CODE['CONTROL']


def getWXK(name):
    """根据名称获取onKeyDown时wxWidgets的的keyCode"""
    if len(name) == 1:
        code = ord(name)
        # 0~9, A~Z
        if 33 <= code <= 126:
            return code
        # a~z
        elif 97 <= code <= 122:
            return code - 32
    return WXK_CODE.get(name.upper(), 0)


def getWXKName(code, mod=None):
    """根据wxWidgets的keyCode和modifiers得到名称"""
    if 33 <= code <= 126:
        name = chr(code)
    else:
        for key in WXK_CODE:
            if WXK_CODE[key] == code:
                name = key
                break
        else:
            return ''
    if mod and not isWXKMod(code):
        if mod & MOD_ALT:
            name = 'alt+' + name
        if mod & MOD_SHIFT:
            name = 'shift+' + name
        if mod & MOD_CONTROL:
            name = 'ctrl+' + name
        if mod & MOD_WIN:
            name = 'win+' + name
    return name