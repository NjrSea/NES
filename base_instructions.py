from typing import Optional

from addressing import ImplicitAddressing
from generic_instruction import Instruction


class Lda(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Ldx(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value


class Ldy(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = value


class Sta(Instruction):
    @classmethod
    def get_data(cls, cpu: 'cpu.CPU', memory_address, data_bytes) -> Optional[int]:
        return cpu.a_reg


class SetBit(ImplicitAddressing, Instruction):
    """
    set a bit to be Ture
    """
    @classmethod
    def apply_side_effects(cls, cpu: 'cpu.CPU'):
        # TODO:
        cpu.status_reg.bits[0] = True


class ClearBit(ImplicitAddressing, Instruction):
    """
    set a bit to be Ture
    """
    @classmethod
    def apply_side_effects(cls, cpu: 'cpu.CPU'):
        cpu.status_reg.interrupt = True
