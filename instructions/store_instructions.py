from addressing import ZeroPageAddressing, ZeroPageAddressingWithY, AbsoluteAddressing
from instructions.base_instructions import Stx, Sta


class StxZeroPage(ZeroPageAddressing, Stx):
    identifier_byte = bytes([0x86])


class StxZeroPageY(ZeroPageAddressingWithY, Stx):
    identifier_byte = bytes([0x96])


class StxAbs(AbsoluteAddressing, Stx):
    identifier_byte = bytes([0x8E])


class StaAbs(AbsoluteAddressing, Sta):
    identifier_byte = bytes([0x8D])