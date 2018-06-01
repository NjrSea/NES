from addressing import ImmediateReadAddressing
from instructions.base_instructions import Cmp


class CmpImm(ImmediateReadAddressing, Cmp):
    identifier_byte = bytes([0xC9])
