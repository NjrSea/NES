from addressing import AbsoluteAddressing, IndirectAddressing, ImplicitAddressing
from instructions.base_instructions import Jmp, Jsr, Rts, Rti


class JmpAbs(AbsoluteAddressing, Jmp):
    identifier_byte = bytes([0x4C])


class JmpInd(IndirectAddressing, Jmp):
    identifier_byte = bytes([0x6C])


class JsrAbs(AbsoluteAddressing, Jsr):
    identifier_byte = bytes([0x20])


class RtsImp(ImplicitAddressing, Rts):
    identifier_byte = bytes([0x60])


class RtiImp(ImplicitAddressing, Rti):
    identifier_byte = bytes([0x40])


class BrkImp(ImplicitAddressing, Jmp):
    identifier_byte = bytes([0x00])
