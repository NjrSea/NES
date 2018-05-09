from abc import ABC, abstractmethod, abstractproperty
from typing import Optional, List

import cpu
from adressing import NoAddressingMixin, ImmediateReadAddressingMixin, AbsoluteAddressingMixin

"""
Finished Instructions

LDA #

SEI
CLD
"""


class Instruction(ABC):
    def __init__(self):
        pass

    def __str__(self):
        return '{}, Identifier byte: {}'.format(self.__class__.__name__,
                                                self.identifier_byte.hex())

    @property
    def writes_to_memory(self) -> bool:
        return False

    @abstractproperty
    @property
    def identifier_byte(self) -> bytes:
        return None

    def apply_side_effects(self, cpu: 'cpu.CPU'):
        pass

    def get_address(self, data_bytes) -> Optional[int]:
        return None

    def get_data(self, cpu: 'cpu.CPU', memory_address: int, data_bytes) -> Optional[int]:
        return None

    def write(self, cpu: 'cpu.CPU', memory_address, value):
        if self.writes_to_memory:
            memory_owner = cpu.get_memory_owner(memory_address)
            memory_owner.set(memory_address, value)

    def execute(self, cpu: 'cpu.CPU', data_bytes: bytes):
        memory_address = self.get_address(data_bytes)

        value = self.get_data(cpu, memory_address, data_bytes)

        self.write(cpu, memory_address, value)

        self.apply_side_effects(cpu)


# data instructions
class LDAImmInstruction(ImmediateReadAddressingMixin, Instruction):
    """
    Load Accumulator with Memory
    """
    identifier_byte = bytes([0xA9])

    def write(self, cpu: 'cpu.CPU', memory_address, value):
        cpu.a_reg = value


class STAAbsInstruction(AbsoluteAddressingMixin, Instruction):
    identifier_byte = bytes([0x8D])
    writes_to_memory = True

    def get_data(self, cpu: 'cpu.CPU', memory_address, data_bytes) -> Optional[int]:
        return cpu.a_reg


# status instructions
class SEIInstruction(NoAddressingMixin, Instruction):
    """
    Set Interrupt Disable Status
    """
    identifier_byte = bytes([0x78])

    def apply_side_effects(self, cpu: 'cpu.CPU'):
        # set the instruction flag to 1
        cpu.status_reg.interrupt = True


class CLDInstruction(NoAddressingMixin, Instruction):
    """
    Clear Decimal Mode
    """
    identifier_byte = bytes([0xD8])

    def apply_side_effects(self, cpu: 'cpu.CPU'):
        cpu.status_reg.decimal = False

