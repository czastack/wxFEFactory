ORIGIN_TIMER_DOWN = 0xCD2B  # this is original code (sub ecx, ebp)
ORIGIN_TIMER_UP = 0xCD03    # this is original code (add ecx, ebp)

NOP = 0x9090

SPAWN_VEHICLE_ID_BASE = 0x1301000

version_config = {
    'V1.0': {
        # 计时器地址
        'CodeInjectNOP_FreezeTimerDownAddr': 0x44CB56,
        'CodeInjectNOP_FreezeTimerUpAddr': 0x44CBAB,

        # 一击必杀
        'CodeInjectJump_OneHitKillAddr': 0x4B331F,
        'CodeInjectCode_OneHitKillAddr': 0x856F68,
        'bNotInjectedJump_OneHitKill': b"\x89\x96\x40\x05\x00",
        'bInjectedJump_OneHitKill':  b"\xE9\x4A\x3C\x3A\x00",
        'bInjectedCode_OneHitKill':  (
            b"\xA8\x27\x48\x0E\x00\x00\x60\xA1\x68\x6F\x85\x00\x8D\x8E\x40\x05\x00\x00\x3B\xC8\x75\x09\x61\x89\x96\x40\x05\x00\x00\xEB\x0B"
            b"\x61\xC7\x86\x40\x05\x00\x00\x00\x00\x00\x00\xE9\x8E\xC3\xC5\xFF"
        ),
        'CHEATS_ADDR': [
            0x969171, # Never Wanted
            0x969174, # Never Get Hungry
            0x96916D, # Infinite Health
            0x96916E, # Infinite Oxygen
            0x969178, # Infinite Ammo
            0x969164, # Tank Mode
            0x969173, # Mega Punch
            0x96916C, # Mega Jump
            0x96917F, # Max Respect
            0x969180, # Max Sex Appeal
            0x96915F, # Fast Cars
            0x96915E, # Cheap Cars
            0xB7CEE4, # Infinite Run
            0xB7CEE6, # Fireproof
            0x96914C, # Perfect Handling
            0x96917A, # Decreased Traffic
            0x969161, # Huge Bunny Hop
            0x969165, # All cars have Nitro
            0x969153, # Boats can Fly
            0x969160, # Cars can Fly
        ],

        # 武器熟练度
        'WEAPON_PROF_ADDR': [
            0xB79494,
            0xB79498,
            0xB7949C,
            0xB794A0,
            0xB794A4,
            0xB794A8,
            0xB794AC,
            0xB794B0,
            0xB794B4,
            0xB794B8,
        ],

        # 和女友的进度
        'GIRL_FRIEND_PROGRESS_ADDR': [
            0xA49EFC, # Denise
            0xA49F00, # Michelle
            0xA49F04, # Helena
            0xA49F0C, # Katie
            0xA49F08, # Barbara
            0xA49F10, # Millie
        ]
    },
    'V1.1': {
        'CodeInjectNOP_FreezeTimerDownAddr': 0x44CBD6,
        'CodeInjectNOP_FreezeTimerUpAddr': 0x44CC2B,

        'CodeInjectJump_OneHitKillAddr': 0x4B339F,
        'CodeInjectCode_OneHitKillAddr': 0x857F68,
        'bNotInjectedJump_OneHitKill': b"\x89\x96\x40\x05\x00\x00",
        'bInjectedJump_OneHitKill':  b"\xE9\xCA\x4B\x3A\x00\x90",
        'bInjectedCode_OneHitKill':  (
            b"\xA8\x27\x48\x0E\x00\x00\x60\xA1\x68\x7F\x85\x00\x8D\x8E\x40\x05\x00\x00\x3B\xC8\x75\x09\x61\x89\x96\x40\x05\x00\x00\xEB\x0B"
            b"\x61\xC7\x86\x40\x05\x00\x00\x00\x00\x00\x00\xE9\x0E\xB4\xC5\xFF"
        ),
    },
}


