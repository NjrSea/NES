from typing import Optional

from addressing import ImplicitAddressing, RelativeAddressing
from instructions.generic_instruction import Instruction, WritesToMemory, ReadsFromMemory
from status import Status


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


class Rts(Jmp):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        # decrease the size of the stack
        cpu.decrease_stack_size(2)

        # grab the pc reg on the stack
        old_pc_reg = cpu.get_memory(cpu.sp_reg, num_bytes=2)

        # jump to the memory location
        super().write(cpu, old_pc_reg, value)


class Nop(Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    pass


class Ld(ReadsFromMemory, Instruction):
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


class StackPush(Instruction):
    """
    push data reg onto stack
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        data_to_push = cls.data_to_push(cpu)

        # write the status to the stack
        cpu.set_memory(cpu.sp_reg, data_to_push, 1)

        cpu.increase_stack_size(1)

        return data_to_push


class StackPull(Instruction):
    """
    pull data reg onto stack
    N Z C I D V
    - - - - - -
    """

    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        cpu.decrease_stack_size(1)

        # get the data from the stack
        pulled_data = cpu.get_memory(cpu.sp_reg)

        # write the pulled data
        return cls.write_pulled_data(cpu, pulled_data)


class And(Instruction):
    """
    bitwise and with accumulator and store result
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        cpu.a_reg &= value
        return cpu.a_reg


class Cmp(Instruction):
    """
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True
    sets_carry_bit = True

    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        return value - cpu.a_reg


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


class Bit(ReadsFromMemory, Instruction):
    """
    bits 7 and 6 of operand are transfered to bit 7 and 6 of SR (N,V);
    the zeroflag is set to the result of operand AND accumulator.

    N Z C I D V
    x + - - - x
    """
    sets_negative_bit = True
    sets_overflow_bit = True

    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        cpu.status_reg.set_status_of_flag(Status.StatusTypes.zero, not bool(value & cpu.a_reg))

