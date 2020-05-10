import abc


class KEY(metaclass=abc.ABCMeta):
    MOD_ALT = 0x0001
    MOD_CTRL = 0x0002
    MOD_CONTROL = 0x0002
    MOD_SHIFT = 0x0004
    MOD_WIN = 0x0008
    MOD_LEFT = 0x8000
    MOD_RIGHT = 0x4000
    MOD_ON_KEYUP = 0x0800

    _0 = 48
    _1 = 49
    _2 = 50
    _3 = 51
    _4 = 52
    _5 = 53
    _6 = 54
    _7 = 55
    _8 = 56
    _9 = 57
    A = 65
    B = 66
    C = 67
    D = 68
    E = 69
    F = 70
    G = 71
    H = 72
    I = 73
    J = 74
    K = 75
    L = 76
    M = 77
    N = 78
    O = 79
    P = 80
    Q = 81
    R = 82
    S = 83
    T = 84
    U = 85
    V = 86
    W = 87
    X = 88
    Y = 89
    Z = 90

    @abc.abstractclassmethod
    def getcode(cls, name):
        pass

    def __new__(cls, name):
        return cls.getcode(name)


class VK(KEY):
    ASCII = {
        ' ': 32,
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
    }

    LBUTTON = 1    # 鼠标左键
    RBUTTON = 2    # 鼠标右键
    CANCEL = 3    # Ctrl + Break
    MBUTTON = 4    # 鼠标中键
    BACK = 8
    TAB = 9
    ENTER = 13
    RETURN = 13
    SHIFT = 16
    CONTROL = 17
    CAPSLOCK = 20
    ESCAPE = 27
    SPACE = 32
    PAGEUP = 33
    PAGEDOWN = 34
    END = 35
    HOME = 36
    LEFT = 37
    UP = 38
    RIGHT = 39
    DOWN = 40
    PRINT_SCREEN = 44
    INS = 45
    DELETE = 46
    LWIN = 91
    RWIN = 92
    NUMPAD0 = 96
    NUMPAD1 = 97
    NUMPAD2 = 98
    NUMPAD3 = 99
    NUMPAD4 = 100
    NUMPAD5 = 101
    NUMPAD6 = 102
    NUMPAD7 = 103
    NUMPAD8 = 104
    NUMPAD9 = 105
    MULTIPLY = 106
    ADD = 107
    SEPARATOR = 108
    SUBTRACT = 109
    DECIMAL = 110
    DIVIDE = 111
    F1 = 112
    F2 = 113
    F3 = 114
    F4 = 115
    F5 = 116
    F6 = 117
    F7 = 118
    F8 = 119
    F9 = 120
    F10 = 121
    F11 = 122
    F12 = 123
    NUMLOCK = 144

    @staticmethod
    def getcode(name):
        """根据名称获取windows的keyCode"""
        if len(name) == 1:
            code = ord(name)
            # 0~9, A~Z
            if 48 <= code <= 57 or 65 <= code <= 90:
                return code
            # a~z
            elif 97 <= code <= 122:
                return code - 32
        name = name.upper()
        return VK.ASCII.get(name, 0) or getattr(VK, name, 0)

    @staticmethod
    def getname(code, mod=None):
        """根据windows的keyCode和modifiers得到名称"""
        # 0~9, A~Z
        if 48 <= code <= 57 or 65 <= code <= 90:
            name = chr(code)
        else:
            for key in VK.__dict__:
                if VK.__dict__[key] == code:
                    name = key
            else:
                return ''
        if mod:
            if mod & KEY.MOD_ALT:
                name = 'alt+' + name
            if mod & KEY.MOD_SHIFT:
                name = 'shift+' + name
            if mod & KEY.MOD_CONTROL:
                name = 'ctrl+' + name
            if mod & KEY.MOD_WIN:
                name = 'win+' + name
        return name


class WXK(KEY):
    BACK = 8
    TAB = 9
    SPACE = 32
    DELETE = 127
    ENTER = 13
    RETURN = 13
    ESCAPE = 27
    LBUTTON = 301
    RBUTTON = 302
    CANCEL = 303
    MBUTTON = 304
    CLEAR = 305
    SHIFT = 306
    ALT = 307
    CONTROL = 308
    MENU = 309
    PAUSE = 310
    CAPITAL = 311
    END = 312
    HOME = 313
    LEFT = 314
    UP = 315
    RIGHT = 316
    DOWN = 317
    SELECT = 318
    PRINT = 319
    EXECUTE = 320
    SNAPSHOT = 321
    INSERT = 322
    HELP = 323
    NUMPAD0 = 324
    NUMPAD1 = 325
    NUMPAD2 = 326
    NUMPAD3 = 327
    NUMPAD4 = 328
    NUMPAD5 = 329
    NUMPAD6 = 330
    NUMPAD7 = 331
    NUMPAD8 = 332
    NUMPAD9 = 333
    MULTIPLY = 334
    ADD = 335
    SEPARATOR = 336
    SUBTRACT = 337
    DECIMAL = 338
    DIVIDE = 339
    F1 = 340
    F2 = 341
    F3 = 342
    F4 = 343
    F5 = 344
    F6 = 345
    F7 = 346
    F8 = 347
    F9 = 348
    F10 = 349
    F11 = 350
    F12 = 351
    NUMLOCK = 364
    SCROLL = 365
    PAGEUP = 366
    PAGEDOWN = 367
    NUMPAD_SPACE = 368
    NUMPAD_TAB = 369
    NUMPAD_ENTER = 370
    NUMPAD_F1 = 371
    NUMPAD_F2 = 372
    NUMPAD_F3 = 373
    NUMPAD_F4 = 374
    NUMPAD_HOME = 375
    NUMPAD_LEFT = 376
    NUMPAD_UP = 377
    NUMPAD_RIGHT = 378
    NUMPAD_DOWN = 379
    NUMPAD_PAGEUP = 380
    NUMPAD_PAGEDOWN = 381
    NUMPAD_END = 382
    NUMPAD_BEGIN = 383
    NUMPAD_INSERT = 384
    NUMPAD_DELETE = 385
    NUMPAD_EQUAL = 386
    NUMPAD_MULTIPLY = 387
    NUMPAD_ADD = 388
    NUMPAD_SEPARATOR = 389
    NUMPAD_SUBTRACT = 390
    NUMPAD_DECIMAL = 391
    NUMPAD_DIVIDE = 392
    WINDOWS_LEFT = 393
    WINDOWS_RIGHT = 394
    WINDOWS_MENU = 395

    @staticmethod
    def ismod(code):
        """判断一个keyCode是否是ctrl, shift, alt"""
        return code == WXK.SHIFT or code == WXK.ALT or code == WXK.CONTROL

    @staticmethod
    def getcode(name):
        """根据名称获取onKeyDown时wxWidgets的keyCode"""
        if len(name) == 1:
            code = ord(name)
            # 0~9, A~Z
            if 33 <= code <= 126:
                return code
            # a~z
            elif 97 <= code <= 122:
                return code - 32
        return getattr(WXK, name.upper(), 0)

    @staticmethod
    def getname(code, mod=None):
        """根据wxWidgets的keyCode和modifiers得到名称"""
        if 33 <= code <= 126:
            name = chr(code)
        else:
            for key in WXK.__dict__:
                if WXK.__dict__[key] == code:
                    name = key
                    break
            else:
                return ''
        if mod and not WXK.ismod(code):
            if mod & KEY.MOD_ALT:
                name = 'alt+' + name
            if mod & KEY.MOD_SHIFT:
                name = 'shift+' + name
            if mod & KEY.MOD_CONTROL:
                name = 'ctrl+' + name
            if mod & KEY.MOD_WIN:
                name = 'win+' + name
        return name
