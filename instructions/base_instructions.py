from typing import Optional

from addressing import ImplicitAddressing, RelativeAddressing
from instructions.generic_instruction import Instruction, WritesToMemory


class Jmp(Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        cpu.pc_reg = memory_address


class Jsr(Jmp):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        # store the pc reg on the stack
        cpu.set_memory(cpu.sp_reg, cpu.pc_reg, num_bytes=2)

        # increases the size of the stack
        cpu.increase_stack_size(2)

        super().write(cpu, memory_address, value)


class Nop(Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    pass


class Ld(Instruction):
    """
    N Z C I D V
    + + - - - -
    """
    sets_zero_bit = True
    sets_negative_bit = True


class Lda(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Ldx(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value


class Ldy(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = value


class Sta(WritesToMemory, Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def get_data(cls, cpu: 'cpu.CPU', memory_address, data_bytes) -> Optional[int]:
        return cpu.a_reg


class Stx(WritesToMemory, Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def get_data(cls, cpu: 'cpu.CPU', memory_address, data_bytes) -> Optional[int]:
        return cpu.x_reg


class Sty(WritesToMemory, Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def get_data(cls, cpu: 'cpu.CPU', memory_address, data_bytes) -> Optional[int]:
        return cpu.y_reg


class SetBit(ImplicitAddressing, Instruction):
    """
    set a bit to be True
    """
    @classmethod
    def apply_side_effects(cls, cpu: 'cpu.CPU'):
        if cls.bit is not None:
            cpu.status_reg.set_status_of_flag(cls.bit, True)


class ClearBit(ImplicitAddressing, Instruction):
    """
    set a bit to be False
    """
    @classmethod
    def apply_side_effects(cls, cpu: 'cpu.CPU'):
        if cls.bit is not None:
            cpu.status_reg.set_status_of_flag(cls.bit, False)


class BranchSet(RelativeAddressing, Jmp):
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        if cpu.status_reg.status_of_flag(cls.bit):
            super().write(cpu, memory_address, value)


class BranchClear(RelativeAddressing, Jmp):
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        if not cpu.status_reg.status_of_flag(cls.bit):
            super().write(cpu, memory_address, value)


class Bit(Instruction):
    """
    bits 7 and 6 of operand are transfered to bit 7 and 6 of SR (N,V);
    the zeroflag is set to the result of operand AND accumulator.
    """
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        # TODO:
        super().write(cpu, memory_address, value)
