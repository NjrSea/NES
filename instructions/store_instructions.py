from addressing import ZeroPageAddressing, ZeroPageAddressingWithX, ZeroPageAddressingWithY,\
    AbsoluteAddressing, AbsoluteAddressingXOffset, IndirectAddressingWithX, IndirectAddressingWithY, \
    AbsoluteAddressingYOffset
from instructions.base_instructions import Stx, Sta


# Stx
class StxZeroPage(ZeroPageAddressing, Stx):
    identifier_byte = bytes([0x86])


class StxZeroPageY(ZeroPageAddressingWithY, Stx):
    identifier_byte = bytes([0x96])


class StxAbs(AbsoluteAddressing, Stx):
    identifier_byte = bytes([0x8E])


# Sta
class StaZeroPage(ZeroPageAddressing, Sta):
    identifier_byte = bytes([0x85])


class StaAbs(AbsoluteAddressing, Sta):
    identifier_byte = bytes([0x8D])


class StaAbsWithX(AbsoluteAddressingXOffset, Sta):
    identifier_byte = bytes([0x9D])


class StaAbsWithY(AbsoluteAddressingYOffset, Sta):
    identifier_byte = bytes([0x99])


class StaZeroPage(ZeroPageAddressing, Sta):
    identifier_byte = bytes([0x85])


class StaZeroPageX(ZeroPageAddressingWithX, Sta):
    identifier_byte = bytes([0x95])


class StaZeroPageIndirectWithY(IndirectAddressingWithY, Sta):
    identifier_byte = bytes([0x91])


class StaZeroIndirectWithX(IndirectAddressingWithX, Sta):
    identifier_byte = bytes([0x81])


