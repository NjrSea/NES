import numpy as np

from addressing import ImpliedAddressing
from instructions.generic_instruction import Instruction
from instructions.base_instructions import StackPush, StackPull


# stack push instructions
class Php(ImpliedAddressing, StackPush):
    identifier_byte = bytes([0x08])

    @classmethod
    def data_to_push(cls, cpu):
        return cpu.status_reg.to_int() | 0b110000


class Pha(ImpliedAddressing, StackPush):
    """
    N Z C I D V
    - - - - - -
    """
    identifier_byte = bytes([0x48])

    @classmethod
    def data_to_push(cls, cpu):
        return cpu.a_reg


class Txs(ImpliedAddressing, Instruction):
    # TODO:
    # sets_negative_bit = True
    sets_zero_bit = True

    identifier_byte = bytes([0x9A])

    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        cpu.sp_reg = cpu.x_reg
        return cpu.sp_reg


# stack pull instructions
class Plp(ImpliedAddressing, StackPull):
    """
    sets the stack
    ignores bits 4 and 5
    """
    identifier_byte = bytes([0x28])

    @classmethod
    def write_pulled_data(cls, cpu, pulled_data):
        cpu.status_reg.from_int(pulled_data, [4, 5])


class Pla(ImpliedAddressing, StackPull):
    sets_negative_bit = True
    sets_zero_bit = True

    identifier_byte = bytes([0x68])

    @classmethod
    def write_pulled_data(cls, cpu, pulled_data):
        cpu.a_reg = np.uint8(pulled_data)
        return cpu.a_reg


class Tsx(ImpliedAddressing, Instruction):
    sets_negative_bit = True
    sets_zero_bit = True

    identifier_byte = bytes([0xBA])

    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        cpu.x_reg = cpu.sp_reg
        return cpu.x_reg
