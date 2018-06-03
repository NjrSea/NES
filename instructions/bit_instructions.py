from addressing import ZeroPageAddressing, AbsoluteAddressing, ImmediateReadAddressing, ZeroPageAddressingWithX,\
    AbsoluteAddressingXOffset, AbsoluteAddressingYOffset, IndirectAddressingWithX, IndirectAddressingWithY, \
    ImplicitAddressing
from instructions.base_instructions import Bit, And, RegisterModifier
import numpy as np


class BitZeroPage(ZeroPageAddressing, Bit):
    identifier_byte = bytes([0x24])


class BitAbs(AbsoluteAddressing, Bit):
    identifier_byte = bytes([0x2C])


# register instructions
class Iny(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0xC8])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg += np.uint8(1)
        return cpu.y_reg


class Dey(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0x88])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg -= np.uint8(1)
        return cpu.y_reg


class Inx(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0xE8])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg += np.uint8(1)
        return cpu.x_reg


class Dex(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0xCA])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg -= np.uint8(1)
        return cpu.x_reg


class Tax(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0xAA])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = cpu.a_reg
        return cpu.x_reg


class Txa(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0x8A])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = cpu.x_reg
        return cpu.a_reg


class Tay(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0xA8])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = cpu.a_reg
        return cpu.y_reg


class Tya(ImplicitAddressing, RegisterModifier):
    identifier_byte = bytes([0x98])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = cpu.y_reg
        return cpu.a_reg
