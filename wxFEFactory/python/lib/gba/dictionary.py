from .utils import checkbytes
import re


class Dictionary:
    def __init__(self, code_table, low_range=None, ctrl_table=None, ctrl_low_range=None, end_code=0):
        """
        :param code_table: 码表文件路径或字典
        :param low_range: 双字节码的低字节判定范围: 长度为2的元组
        :param ctrl_table: 控制码表: 字典{code: fn(bytes, i) -> (word, i)}
        :param end_code: 结束符 
        """
        self._code_char = code_char = {}
        self._char_code = char_code = {}
        self.low_range = low_range

        if hasattr(ctrl_table, '__len__') and isinstance(ctrl_table[0], CtrlCode):
            ctrl_table = {ctrlcode.code: ctrlcode for ctrlcode in ctrl_table}

        self.ctrl_table = ctrl_table
        self.ctrl_low_range = ctrl_low_range
        self.end_code = end_code

        if isinstance(code_table, str):
            with open(code_table, 'r', encoding='utf8') as f:
                for line in f.readlines():
                    k, v = line.rstrip('\n').split('=', 1)
                    k = int(k, 16)
                    code_char[k] = v
                    if len(v) == 1:
                        char_code[ord(v)] = k

    def getCode(self, ch):
        return self._char_code.get(ord(ch), 0x00)

    def getChar(self, code):
        return self._code_char.get(code, None)

    def decode(self, data, one=False):
        """
        :param one: 读到一句就返回
        """
        if checkbytes(data):
            char = 0
            words = [] # 一句话
            result = []
            i = offset = -1
            length = len(data) - 1

            while i < length:
                i += 1
                byte = data[i]

                if char == 0:
                    if (
                        (not self.low_range) or (self.low_range[0] <= byte < self.low_range[1]) or
                        (self.ctrl_low_range and self.ctrl_low_range[0] <= byte < self.ctrl_low_range[1])
                    ):
                        # 读取到双字节码的低字节
                        char = byte
                        # 记录这句话的偏移位置
                        if not words:
                            offset = i
                        continue
                    elif byte == self.end_code:
                        # 读到结束符，把当前文本缓冲区内容存入result，并清空缓冲区
                        if words:
                            result.append((offset, ''.join(words)))
                            words.clear()
                        else:
                            continue
                    else:
                        if not words:
                            offset = i
                        word = self._code_char.get(byte, None)
                        if word:
                            # 读到单字节字码
                            pass
                        elif self.ctrl_table and byte in self.ctrl_table:
                            # 读到单字节控制码
                            word, i = self.ctrl_table[byte].decode(data, i)
                        else:
                            # 无法解析
                            word = '[?%X]' % byte
                        words.append(word)
                else:
                    char = char << 8 | byte # 低字节在左边
                    try:
                        words.append(self._code_char[char])
                    except:
                        # 尝试双字节控制码
                        if self.ctrl_table and char in self.ctrl_table:
                            word, i = self.ctrl_table[char].decode(data, i)
                            words.append(word)
                        else:
                            raise
                    char = 0
            if words:
                if one:
                    return ''.join(words)
                result.append((offset, ''.join(words)))

            if len(result) is 0 and one:
                result = ''
            elif one:
                return result[0][1]
            return result
        else:
            print("data must be integer iterable")

    def encode(self, text, buf=None, sep=None):
        """
        :param sep: 分隔符，便于显示
        """
        result = bytearray() if buf is None else buf
        length = len(text) - 1
        i = -1

        if sep and isinstance(sep, (str, bytes)):
            sep = ord(sep)

        while i < length:
            i += 1
            ch = text[i]
            code = self.getCode(ch)
            if code == 0:
                if self.ctrl_table and CtrlCode.FMT_START.startswith(ch):
                    con = False
                    for ctrlcode in self.ctrl_table.values():
                        m = ctrlcode.encode(text, i)
                        if m:
                            bs, i = m
                            i -= 1
                            result.extend(bs)
                            con = True
                            break
                    if con:
                        continue
                print("warning: %s不在码表中" % ch)
                
            if code > 0xFF:
                result.append(code >> 8)
                result.append(code & 0xFF)
            else:
                result.append(code)
            if sep:
                result.append(sep)
        if self.end_code:
            result.append(self.end_code)
        return result

    def encodeToArray(self, text):
        """不支持控制码"""
        def getCode(ch):
            code = self._char_code.get(ord(ch), 0x00)
            if code is 0:
                print("warning: %s不在码表中" % ch)
            return code

        return [getCode(ch) for ch in text]


    def decode_it(self, data, codebuff=None, ignore_zero=False):
        """ 读到一句就返回
        :param ignore_zero: 不把00当作结束符
        """
        char = 0
        words = [] # 一句话
        i = offset = -1
        it = iter(data)

        while True:
            i += 1

            try:
                byte = next(it)
            except StopIteration:
                break

            if codebuff is not None:
                codebuff.append(byte)

            if char == 0:
                if (
                    (not self.low_range) or (self.low_range[0] <= byte < self.low_range[1]) or
                    (self.ctrl_low_range and self.ctrl_low_range[0] <= byte < self.ctrl_low_range[1])
                ):
                    # 读取到双字节码的低字节
                    char = byte
                    # 记录这句话的偏移位置
                    if not words:
                        offset = i
                    continue
                elif not ignore_zero and byte == self.end_code:
                    # 读到结束符，把当前文本缓冲区内容存入result，并清空缓冲区
                    if words:
                        break
                    else:
                        continue
                else:
                    if not words:
                        offset = i
                    word = self._code_char.get(byte, None)
                    if word:
                        # 读到单字节字码
                        pass
                    elif self.ctrl_table and byte in self.ctrl_table:
                        # 读到单字节控制码
                        try:
                            word = self.ctrl_table[byte].decode_it(it)
                        except:
                            print(data)
                            word = '[??]'
                            # raise
                    else:
                        # 无法解析
                        word = '[?%X]' % byte
                    words.append(word)
            else:
                char = char << 8 | byte # 低字节在左边
                try:
                    words.append(self._code_char[char])
                except:
                    # 尝试双字节控制码
                    if self.ctrl_table and char in self.ctrl_table:
                        word = self.ctrl_table[char].decode_it(it)
                        words.append(word)
                    else:
                        print("can't decode %04X" % char)
                char = 0
        return ''.join(words)



def fmt2reg(fmt):
    return re.compile(re.escape(fmt).replace('\\%d', '(\w+)'))

class CtrlCode:
    # usage:
    # cc = CtrlCode(0xFC, 'no.%d name[%d]')
    # print(cc.encode('多亏了{no.1 name[1]}的帮助', 3))

    FMT_START = '{'
    FMT_END   = '}'
    FMT_START_LEN = len(FMT_START)
    FMT_END_LEN   = len(FMT_END)

    __slots__ = ('code', 'fmt', 'argc', 'reg')

    def __init__(self, code, fmt):
        self.code = code
        self.fmt = self.FMT_START + fmt + self.FMT_END
        self.argc = fmt.count('%d')
        self.reg = fmt2reg(fmt)

    def decode(self, data, i):
        if self.argc is 0:
            return self.fmt, i
        if self.argc is 1:
            i += 1
            return self.fmt % data[i], i
        else:
            return self.fmt % tuple(data[i] for i in range(self.argc)), i + self.argc

    def decode_it(self, it):
        """
        :param it: 类byte迭代器
        """
        if self.argc is 0:
            return self.fmt
        if self.argc is 1:
            return self.fmt % next(it)
        else:
            return self.fmt % tuple(next(it) for i in range(self.argc))

    def encode(self, text, i):
        result = self.encode_args(text, i)
        if result:
            code, args, end = result

            if not args:
                return (code,), end
            else:
                code_bytes = (code,) if code < 0x100 else (code & 0xFF, code >> 8)
                return bytes(code_bytes + args), end

    def encode_args(self, text, i):
        """手动encode时，获取所需参数"""
        code = self.code
        if self.argc is 0:
            fmt_len = len(self.fmt)
            if text.find(self.fmt, i, i + fmt_len) == i:
                return code, None, i + fmt_len
        elif text.find(self.FMT_START, i, i + self.FMT_START_LEN) == i:
            i += self.FMT_START_LEN
            end = text.find(self.FMT_END, i, i + 32)
            if end != -1:
                match = self.reg.match(text[i:end])
                if match:
                    code_bytes = (code,) if code < 0x100 else (code & 0xFF, code >> 8)
                    return code, tuple(int(i) for i in match.groups()), end + self.FMT_END_LEN