from addressing import ImmediateReadAddressing, IndirectAddressingWithX, ZeroPageAddressing, ZeroPageAddressingWithX, \
    ZeroPageAddressingWithY, AbsoluteAddressing, AbsoluteAddressingYOffset, AbsoluteAddressingXOffset, IndirectAddressingWithY
from instructions.base_instructions import Lda, Ldx, Ldy


# Lda
class LdaImm(ImmediateReadAddressing, Lda):
    identifier_byte = bytes([0xA9])


class LdaIndirectWithX(IndirectAddressingWithX, Lda):
    identifier_byte = bytes([0xA1])


class LdaZeroPage(ZeroPageAddressing, Lda):
    identifier_byte = bytes([0xA5])


class LdaZeroPageX(ZeroPageAddressingWithX, Lda):
    identifier_byte = bytes([0xB5])


class LdaAbs(AbsoluteAddressing, Lda):
    identifier_byte = bytes([0xAD])


class LdaAbsY(AbsoluteAddressingYOffset, Lda):
    identifier_byte = bytes([0xB9])


class LdaAbsX(AbsoluteAddressingXOffset, Lda):
    identifier_byte = bytes([0xBD])


class LdaIndirectWithY(IndirectAddressingWithY, Lda):
    identifier_byte = bytes([0xB1])


# Ldx
class LdxImm(ImmediateReadAddressing, Ldx):
    identifier_byte = bytes([0xA2])


class LdxZeroPage(ZeroPageAddressing, Ldx):
    identifier_byte = bytes([0xA6])


class LdxZeroPageWithY(ZeroPageAddressingWithY, Ldx):
    identifier_byte = bytes([0xB6])


class LdxZeroAbs(AbsoluteAddressing, Ldx):
    identifier_byte = bytes([0xAE])


class LdxZeroAbsWithY(AbsoluteAddressingYOffset, Ldx):
    identifier_byte = bytes([0xBE])


# Ldy
class LdyImm(ImmediateReadAddressing, Ldy):
    identifier_byte = bytes([0xA0])


class LdyZeroPageX(ZeroPageAddressingWithY, Ldy):
    identifier_byte = bytes([0xB4])


class LdyZeroPage(ZeroPageAddressing, Ldy):
    identifier_byte = bytes([0xA4])


class LdyZeroAbs(AbsoluteAddressing, Ldy):
    identifier_byte = bytes([0xAC])


class LdyZeroAbsWithX(AbsoluteAddressingXOffset, Ldy):
    identifier_byte = bytes([0xBE])
