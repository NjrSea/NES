from addressing import ZeroPageAddressing, AbsoluteAddressing
from instructions.base_instructions import Bit


class BitZeroPage(ZeroPageAddressing, Bit):
    identifier_byte = bytes([0x24])


class BitAbs(AbsoluteAddressing, Bit):
    identifier_byte = bytes([0x2C])