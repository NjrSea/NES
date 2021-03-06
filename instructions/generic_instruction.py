from typing import Optional
import helpers

import cpu


class Instruction:
    identifier_byte = None
    bit = None  # type: Status.StatusTypes
    sets_zero_bit = False
    sets_negative_bit = False
    sets_decimal_bit = False
    sets_overflow_bit_from_value = False
    sets_interrupt_bit = False
    sets_carry_bit = False

    data_length = 0

    @classmethod
    def apply_side_effects(cls, cpu: 'cpu.CPU'):
        pass

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        return None

    @classmethod
    def get_data(cls, cpu: 'cpu.CPU', memory_address: int, data_bytes) -> Optional[int]:
        if memory_address is not None:
            return cpu.get_memory(memory_address)
        return None

    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        pass

    @classmethod
    def execute(cls, cpu: 'cpu.CPU', data_bytes: bytes):
        memory_address = cls.get_address(cpu, data_bytes)

        value = cls.get_data(cpu, memory_address, data_bytes)

        updated_value = cls.write(cpu, memory_address, value)

        if updated_value is not None:
            value = updated_value

        cls.apply_side_effects(cpu)

        return value


class WritesToMemory:
    @classmethod
    def write(cls, cpu: 'cpu.CPU', memory_address, value):
        memory_owner = cpu._get_memory_owner(memory_address)
        memory_owner.set(position=memory_address, value=value)

