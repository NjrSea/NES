from typing import Optional

import numpy as np

from addressing import ImpliedAddressing, RelativeAddressing
from instructions.generic_instruction import Instruction, WritesToMemory
from status import Status
from helpers import Numbers


class Jmp(Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        cpu.pc_reg = np.uint16(memory_address)


class Jsr(Jmp):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        # store the pc reg on the stack
        cpu.stack_push(cpu.pc_reg - np.uint16(1), 2)

        super().write(cpu, memory_address, value)


class Rts(Jmp):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        # grab the pc reg on the stack
        old_pc_reg = cpu.stack_pop(2) + np.uint16(1)

        # jump to the memory location
        super().write(cpu, old_pc_reg, value)


class Brk(Instruction):
    """
    push PC+2, push SR
    N Z C I D V
    - - - 1 - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # increment pc reg
        cpu.pc_reg += np.uint16(1)

        # store the pc reg onto the stack
        cpu.set_stack_value(cpu.pc_reg, Numbers.SHORT.value)

        # store the status on the stack
        status = cpu.status_reg.to_int()
        cpu.set_stack_value(status)

        # set interrupt bit to be true
        cpu.status_reg.bits[Status.StatusTypes.interrupt] = True


class Rti(Jmp):
    """
    N Z C I D V
    from stack
    """
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        # get the stored status from stack, and then set the status reg
        status = cpu.stack_pop(1)
        cpu.status_reg.from_int(status, [4, 5])

        # grab the stored pc reg from the stack (note: is exact pc_reg not pc_reg+1)
        old_pc_reg = cpu.stack_pop(2)

        # jump to the memory location
        super().write(cpu, old_pc_reg, value)


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
        cpu.a_reg = np.uint8(value)

class Lax(Ld):
    """
    Lda then Tax
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        Lda.write(cpu, memory_address, value)
        return Tax.write(cpu, memory_address, value)


class Ldx(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = np.uint8(value)


class Ldy(Ld):
    """
    N Z C I D V
    + + - - - -
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = np.uint8(value)


class Sta(WritesToMemory, Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def get_data(cls, cpu: 'cpu.CPU', memory_address, data_bytes) -> Optional[int]:
        return cpu.a_reg


class Sax(WritesToMemory, Instruction):
    """
    N Z C I D V
    - - - - - -
    """
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg & cpu.x_reg


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
        cpu.stack_push(data_to_push, 1)

        return data_to_push


class StackPull(Instruction):
    """
    pull data reg onto stack
    N Z C I D V
    - - - - - -
    """

    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        # get the data from the stack
        pulled_data = cpu.stack_pop()

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
        cpu.a_reg &= np.uint8(value)
        return cpu.a_reg


class Ora(Instruction):
    """
    bitwise or with accumulator and store result
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg |= np.uint8(value)
        return cpu.a_reg


class Eor(Instruction):
    """
    bitwise exclusive or with accumulator and store result
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg ^= np.uint8(value)
        return cpu.a_reg


class Adc(Instruction):
    """
    A + M + C -> A, C
    N Z C I D V
    + + + - - +
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        result = cpu.a_reg + int(value) + int(cpu.status_reg.bits[Status.StatusTypes.carry])
        # if value and a_reg have different signs than result, set overflow
        overflow = bool((np.uint8(cpu.a_reg) ^ np.uint8(result)) & (np.uint8(value) ^ np.uint8(result)) & 0x80)
        cpu.status_reg.bits[Status.StatusTypes.overflow] = overflow

        # if greater than 255, carry
        cpu.status_reg.bits[Status.StatusTypes.carry] = bool(result & 256)

        cpu.a_reg = np.uint8(result)
        return cpu.a_reg


class Sbc(Adc):
    """
    A - M - C -> A
    N Z C I D V
    + + + - - +
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        return super().write(cpu, memory_address, value ^ 0xFF)


class Shift(Instruction):
    """
    Shifts bits
    N Z C I D V
    + + + - - -
    """
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # shift bits
        if memory_address is None:
            cpu.a_reg = value
        else:
            cpu.set_memory(memory_address, value, Numbers.BYTE.value)

        return value


class Lsr(Shift):
    """
    Shifts bits right
    N Z C I D V
    + + + - - -
    LSR shifts all bits right one position. 0 is shifted into bit 7 and the original bit 0 is shifted into the Carry.
    """
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # shift bits
        updated_value = np.uint8(value >> 1)
        # set the carry reg
        cpu.status_reg.bits[Status.StatusTypes.carry] = bool(value & 0b1)

        return super().write(cpu, memory_address, updated_value)


class Asl(Shift):
    """
    Shifts bits left
    ASL shifts all bits left one position. 0 is shifted into bit 0 and the original bit 7 is shifted into the Carry.
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # shift bits
        value_without_7 = value & 0b01111111
        updated_value = np.uint8(value_without_7 << 1)
        # set the carry reg
        original_bit_7 = (value & 0b10000000) >> 7
        cpu.status_reg.bits[Status.StatusTypes.carry] = bool(original_bit_7)
        return super().write(cpu, memory_address, updated_value)


class Ror(Shift):
    """
    Shifts bits right
    ROR shifts all bits right one position. The Carry is shifted into bit 7 and the original bit 0 is shifted into the Carry.
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        # shift bits
        shifted_bits_without_7 = np.uint8(value >> 1)
        shifted_carry = int(cpu.status_reg.bits[Status.StatusTypes.carry]) << 7
        updated_value = np.uint8(shifted_bits_without_7 | shifted_carry)
        # set the carry reg
        cpu.status_reg.bits[Status.StatusTypes.carry] = bool(value & 0b1)
        return super().write(cpu, memory_address, updated_value)


class Rol(Shift):
    """
    Shifts bits left
    ROL shifts all bits left one position. The Carry is shifted into bit 0 and the original bit 7 is shifted into the Carry.
    N Z C I D V
    + + + - - -
    """
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # shift bits
        value_reg_without_7 = value & 0b01111111
        shifted_bits_without_0 = value_reg_without_7 << 1
        shifted_carry = int(cpu.status_reg.bits[Status.StatusTypes.carry])
        updated_value = np.uint8(shifted_bits_without_0 | shifted_carry)
        # set the carry reg
        original_bit_7 = (value & 0b10000000) >> 7
        cpu.status_reg.bits[Status.StatusTypes.carry] = bool(original_bit_7)
        return super().write(cpu, memory_address, updated_value)


class Inc(Instruction):
    """
    increment memory by 1
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        original_value = np.uint8(cpu.get_memory(memory_address))
        updated_value = original_value + np.uint8(1)
        cpu.set_memory(memory_address, updated_value)
        return updated_value


class Dec(Instruction):
    """
    increment memory by 1
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        original_value = np.uint8(cpu.get_memory(memory_address))
        updated_value = original_value - np.uint8(1)
        cpu.set_memory(memory_address, updated_value)
        return updated_value


class Compare(Instruction):
    """
    compare given value with a given reg
    N Z C I D V
    + + + - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        # TODO: remove np.int()
        cpu.status_reg.bits[Status.StatusTypes.carry] = not bool(np.int(value) & 256)
        return value


class Cmp(Compare):
    """
    compare given value with the a reg
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        result = int(cpu.a_reg) - value
        return super().write(cpu, memory_address, result)


class Cpx(Compare):
    """
    compare given value with the x reg
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        result = int(cpu.x_reg) - value
        return super().write(cpu, memory_address, result)


class Cpy(Compare):
    """
    compare given value with the y reg
    """
    @classmethod
    def write(cls, cpu, memory_address, value):
        result = int(cpu.y_reg) - value
        return super().write(cpu, memory_address, result)


class SetBit(ImpliedAddressing, Instruction):
    """
    set a bit to be True
    """
    @classmethod
    def apply_side_effects(cls, cpu: 'cpu.CPU'):
        if cls.bit is not None:
            cpu.status_reg.set_status_of_flag(cls.bit, True)


class ClearBit(ImpliedAddressing, Instruction):
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

    N Z C I D V
    x + - - - x
    """
    sets_negative_bit = True
    sets_overflow_bit_from_value = True

    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        cpu.status_reg.set_status_of_flag(Status.StatusTypes.zero, not bool(value & cpu.a_reg))


class RegisterModifier(Instruction):
    """
    updates register
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True


class Dcp(Instruction):
    """
    dec then cmp
    N Z C I D V
    + + - - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        updated_value = Dec.write(cpu, memory_address, value)

        return Cmp.write(cpu, memory_address, updated_value)


class Isb(Instruction):
    """
    inc then sbc
    A - M - C -> A
    N Z C I D V
    + + + - - +
    """
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        updated_value = Dec.write(cpu, memory_address, value)

        return Cmp.write(cpu, memory_address, updated_value)


class Isb(Instruction):
    """
    inc then sbc
    A - M - C -> A
    N Z C I D V
    + + + - - +
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        updated_value = Inc.write(cpu, memory_address, value)

        return Sbc.write(cpu, memory_address, updated_value)

class Slo(Instruction):
    """
    asl then ora
    N Z C I D V
    + + + - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        updated_value = Asl.write(cpu, memory_address, value)
        return Ora.write(cpu, memory_address, updated_value)


class Rla(Instruction):
    """
    Rol then and
    N Z C I D V
    + + + - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        updated_value = Rol.write(cpu, memory_address, value)
        return And.write(cpu, memory_address, updated_value)


class Rra(Instruction):
    """
    Ror then adc
    N Z C I D V
    + + + - - +
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        updated_value = Ror.write(cpu, memory_address, value)
        return Adc.write(cpu, memory_address, updated_value)


class Tax(ImpliedAddressing, RegisterModifier):
    identifier_byte = bytes([0xAA])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = cpu.a_reg
        return cpu.x_reg


class Slo(Instruction):
    """
    asl then ora
    N Z C I D V
    + + + - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        updated_value = Asl.write(cpu, memory_address, value)
        return Ora.write(cpu, memory_address, updated_value)


class Rla(Instruction):
    """
    Rol then and
    N Z C I D V
    + + + - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        updated_value = Rol.write(cpu, memory_address, value)
        return And.write(cpu, memory_address, updated_value)


class Rra(Instruction):
    """
    Ror then adc
    N Z C I D V
    + + + - - +
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        updated_value = Ror.write(cpu, memory_address, value)
        return Adc.write(cpu, memory_address, updated_value)


class Sre(Instruction):
    """
    lsr then eor
    N Z C I D V
    + + + - - -
    """
    sets_negative_bit = True
    sets_zero_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        updated_value = Lsr.write(cpu, memory_address, value)
        return Eor.write(cpu, memory_address, updated_value)


