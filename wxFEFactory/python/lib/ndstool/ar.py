import re

INDENT = '    '
H = '[\\dA-F]'
FMT = {
    'i': H,
    'i7': H + '{7}',
    'hw': H + '{4}',
    'w': H + '{8}',
    'b': H + '{2}',
}


def _F(s):
    return re.compile(REPEAT_REG.sub(r'{\1}', s).format(**FMT), re.IGNORECASE)


REPEAT_REG = re.compile(r'(\{\d\})')
CODE_REG = re.compile(_F('{w} {w}'))


NDS_AR_HANDLERS = {
    "0": (
        _F("0({i7}) ({w})"),
        "write32(0x{0}+offset, 0x{1})",
    ),
    "1": (
        _F("1({i7}) {i}{4}({hw})"),
        "write16(0x{0}+offset, 0x{1})",
    ),
    "2": (
        _F("2({i7}) {i}{6}({b})"),
        "write8(0x{0}+offset, 0x{1})",
    ),
    "3": (
        _F("3({i7}) ({w})"),
        "if 0x{1} > read32(0x{0}):",
    ),
    "4": (
        _F("4({i7}) ({w})"),
        "if 0x{1} < read32(0x{0}):",
    ),
    "5": (
        _F("5({i7}) ({w})"),
        "if 0x{1} == read32(0x{0}):",
    ),
    "6": (
        _F("6({i7}) ({w})"),
        "if 0x{1} != read32(0x{0}):",
    ),

    "7": (
        _F("7({i7}) ({hw})({hw})"),
        "if 0x{2} > ~0x{1} & read16(0x{0}):",
    ),
    "8": (
        _F("8({i7}) ({hw})({hw})"),
        "if 0x{2} < ~0x{1} & read16(0x{0}):",
    ),
    "9": (
        _F("9({i7}) ({hw})({hw})"),
        "if 0x{2} == ~0x{1} & read16(0x{0}):",
    ),
    "A": (
        _F("A({i7}) ({hw})({hw})"),
        "if 0x{2} != ~0x{1} & read16(0x{0}):",
    ),

    "B": (
        _F("B({i7}) 0{8}"),
        "offset = read32(0x{0})",
    ),
    "D3": (
        _F("D30{6} ({w})"),
        "offset = 0x{0}",
    ),
    "DC": (
        _F("DC0{6} ({w})"),
        "offset += 0x{0}",
    ),

    "C": (
        _F("C0{7} ({w})"),
        "n = 0x{0}",
    ),

    "D0": (
        _F("D0{7} 0{8}"),
        "Loads the previous execution status",
    ),

    "D1": (
        _F("D10{6} 0{8}"),
        "for i in range(n):",
    ),
    "D2": (
        _F("D20{6} 0{8}"),
        "clear(Dx); for i in range(n):",
    ),

    "D4": (
        _F("D40{6} ({w})"),
        "data += 0x{0}",
    ),
    "D5": (
        _F("D50{6} ({w})"),
        "data = 0x{0}",
    ),

    "D6": (
        _F("D60{6} ({w})"),
        "write32(0x{0} + offset, data); offset += 4",
    ),
    "D7": (
        _F("D70{6} ({w})"),
        "write16(0x{0} + offset, data); offset += 2",
    ),
    "D8": (
        _F("D80{6} ({w})"),
        "write8(0x{0} + offset, data); offset += 1",
    ),

    "D9": (
        _F("D90{6} ({w})"),
        "data = read32(0x{0} + offset)",
    ),
    "DA": (
        _F("DA0{6} ({w})"),
        "data = read16(0x{0} + offset)",
    ),
    "DB": (
        _F("DB0{6} ({w})"),
        "data = read8(0x{0} + offset)",
    ),
    "E": (
        _F("E({i7}) ({w})"),
        "Copies 0x{1} bytes from (current code location + 8) to [0x{0} + offset].",
    ),
    "F": (
        _F("F({i7}) ({w})"),
        "Use the code type D3, DC or B before to set the offset."
        "D2 should be needed to clear the offset after the code.\n"
        "D3000000 XXXXXXXX\n"
        "FYYYYYYY ZZZZZZZZ\n"
        "This should copy ZZZZZZZZ bytes from offset (=0x{0} in this case) to 0x{1}."
        "(YYYYYYYY if fixed, no offsets are added to it).",
    ),
}


def iter_code_simple(lines):
    return lines.split('\n')


def iter_code_strict(lines):
    return map(lambda x: x.group(0), CODE_REG.finditer(lines))


def analyse(lines, strict=False):
    # 从字符串中获取一条代码
    iter_code = iter_code_strict if strict else iter_code_simple
    indent = 0
    preloop = False
    result = []

    for code in iter_code(lines.upper()):
        id_ = code[:2]
        if id_ not in NDS_AR_HANDLERS:
            id_ = code[0]
        if id_ not in NDS_AR_HANDLERS:
            raise ValueError(code + ' is not a valid AR code')
        fmt, value = NDS_AR_HANDLERS[id_]
        matcher = fmt.match(code)
        if matcher:
            if preloop and (id_ == 'D1' or id_ == 'D2'):
                preloop = False
            elif id_ == 'D2':
                value = 'end'
                indent -= 1

            if indent:
                result.append(INDENT * indent)
            result.append(value.format(*matcher.groups()))
            result.append('\n')

            if value[-1] == ':':
                indent += 1
                if id_ == 'C':
                    preloop = True

    return ''.join(result)
