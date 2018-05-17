from typing import Optional

from addressing import ImplicitAddressing
from generic_instruction import Instruction, WritesToMemory


class Jmp(Instruction):
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        cpu.pc_reg = memory_address


class Jsr(Jmp):
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        # store the pc reg on the stack
        cpu.set_memory(cpu.sp_reg, cpu.pc_reg, num_bytes=2)

        # increases the size of the stack
        cpu.increase_stack_size(2)

        super().write(cpu, memory_address, value)


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


class Sta(WritesToMemory, Instruction):
    @classmethod
    def get_data(cls, cpu: 'cpu.CPU', memory_address, data_bytes) -> Optional[int]:
        return cpu.a_reg


class Stx(WritesToMemory, Instruction):
    @classmethod
    def get_data(cls, cpu: 'cpu.CPU', memory_address, data_bytes) -> Optional[int]:
        return cpu.x_reg


class Sty(WritesToMemory, Instruction):
    @classmethod
    def get_data(cls, cpu: 'cpu.CPU', memory_address, data_bytes) -> Optional[int]:
        return cpu.y_reg


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
