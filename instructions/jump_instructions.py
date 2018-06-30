from addressing import AbsoluteAddressing, IndirectAddressing, ImpliedAddressing
from instructions.base_instructions import Jmp, Jsr, Rts, Rti


class JmpAbs(AbsoluteAddressing, Jmp):
    identifier_byte = bytes([0x4C])


class JmpInd(IndirectAddressing, Jmp):
    identifier_byte = bytes([0x6C])


class JsrAbs(AbsoluteAddressing, Jsr):
    identifier_byte = bytes([0x20])


class RtsImp(ImpliedAddressing, Rts):
    identifier_byte = bytes([0x60])


class RtiImp(ImpliedAddressing, Rti):
    identifier_byte = bytes([0x40])


class BrkImp(ImpliedAddressing, Jmp):
    identifier_byte = bytes([0x00])
