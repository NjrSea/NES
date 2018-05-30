from addressing import ZeroPageAddressing, AbsoluteAddressing, ImmediateReadAddressing, ZeroPageAddressingWithX,\
    AbsoluteAddressingXOffset, AbsoluteAddressingYOffset, IndirectAddressingWithX, IndirectAddressingWithY
from instructions.base_instructions import Bit, And


class BitZeroPage(ZeroPageAddressing, Bit):
    identifier_byte = bytes([0x24])


class BitAbs(AbsoluteAddressing, Bit):
    identifier_byte = bytes([0x2C])


# and instructions
class AndImm(ImmediateReadAddressing, And):
    identifier_byte = bytes([0x29])


class AndZpg(ZeroPageAddressing, And):
    identifier_byte = bytes([0x25])


class AndZpgX(ZeroPageAddressingWithX, And):
    identifier_byte = bytes([0x35])


class AndAbs(AbsoluteAddressing, And):
    identifier_byte = bytes([0x2D])


class AndAbsX(AbsoluteAddressingXOffset, And):
    identifier_byte = bytes([0x3D])


class AndAbsY(AbsoluteAddressingYOffset, And):
    identifier_byte = bytes([0x39])


class AndIndX(IndirectAddressingWithX, And):
    identifier_byte = bytes([0x21])


class AndIndY(IndirectAddressingWithY, And):
    identifier_byte = bytes([0x31])