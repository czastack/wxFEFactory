
def r1(n):
    return ((n & 0xFF00) >> 8) | ((n & 0xFF) << 8)