

class LOROM:
    @classmethod
    def from_str(self, str):
        (b, o) = str.split(":")
        return (int(b, 16), int(o, 16))

    @classmethod
    def from_int(self, int):
        bank = int // 0x8000
        offset = int & 0x00FFFF
        if not (bank & 0x01):
            offset = offset + 0x8000
        return (bank, offset)

    # Takes 4 possible forms:
    # 1 argument, string of bank:offset, hex
    # 1 argument, integer 3 bytes, "packed LOROM"
    # 1 argument, integer 3 bytes, flat=True
    # 2 arguments, bank, offset
    def __init__(self, *args,  flat=True):
        if len(args) == 1:
            if isinstance(args[0], str):
                (self.bank, self.offset) = LOROM.from_str(args[0])
            elif isinstance(args[0], int):
                if flat:
                    (self.bank, self.offset) = LOROM.from_int(args[0])
                else:
                    self.bank = (args[0] & 0xFF0000) >> 16
                    self.offset = (args[0] & 0x00FFFF)
            else:
                raise ValueError("Conversion arg must be str or int")
        elif len(args) == 2:
            self.bank = args[0]
            self.offset = args[1]
        else:
            raise ValueError("Unexpected number of args")

    def __repr__(self):
        return "{0:02X}:{1:04X}".format(self.bank, self.offset)

    def __int__(self):
        return self.bank * 0x8000 + (self.offset - 0x8000)

    def __radd__(self, val):
        if isinstance(val, int):
            return LOROM(val + int(self))
        elif isinstance(val, LOROM):
            return LOROM(int(val) + int(self))

    def __add__(self, val):
        if isinstance(val, int):
            return LOROM(int(self) + val)
        elif isinstance(val, LOROM):
            return LOROM(int(self) + int(val))

    def __rsub__(self, val):
        if isinstance(val, int):
            return LOROM(val - int(self))
        elif isinstance(val, LOROM):
            return LOROM(int(val) - int(self))

    def __sub__(self, val):
        if isinstance(val, int):
            return LOROM(int(self) - val)
        elif isinstance(val, LOROM):
            return LOROM(int(self) - int(val))

    def __le__(self, val):
        (cmp, other) = self.check_args(val)
        return cmp <= other

    def __lt__(self, val):
        (cmp, other) = self.check_args(val)
        return cmp < other

    def __ge__(self, val):
        (cmp, other) = self.check_args(val)
        return cmp >= other

    def __gt__(self, val):
        (cmp, other) = self.check_args(val)
        return cmp > other

    def __eq__(self, val):
        (cmp, other) = self.check_args(val)
        return cmp == other

    def check_args(self, val):
        cmp = int(self)
        if isinstance(val, int):
            other = val
        elif isinstance(val, LOROM):
            other = int(val)
        else:
            raise ValueError("Comparison must be between int or LOROM.")
        return (cmp, other)

    def __hash__(self):
        return hash(int(self))

    def from_offset(self, offset):
        return LOROM(self.bank, self.offset)
