import math
from collections import OrderedDict
from enum import IntEnum
from typing import List

from instructions.generic_instruction import Instruction
import numpy as np


class Status:
    """
    7  bit  0
    ---- ----
    NVss DIZC
    |||| ||||
    |||| |||+- Carry: 1 if last addition or shift resulted in a carry, or if
    |||| |||     last subtraction resulted in no borrow
    |||| ||+-- Zero: 1 if last operation resulted in a 0 value
    |||| |+--- Interrupt: Interrupt inhibit
    |||| |       (0: /IRQ and /NMI get through; 1: only /NMI gets through)
    |||| +---- Decimal: 1 to make ADC and SBC use binary-coded decimal arithmetic
    ||||         (ignored on second-source 6502 like that in the NES)
    ||++------ s: No effect, used by the stack copy, see note below
    |+-------- Overflow: 1 if last ADC or SBC resulted in signed overflow,
    |            or D6 from last BIT
    +--------- Negative: Set to bit 7 of the last operation
    """

    class StatusTypes(IntEnum):
        carry = 0
        zero = 1
        interrupt = 2
        decimal = 3
        unused1 = 4
        unused2 = 5
        overflow = 6
        negative = 7

    def __init__(self):
        self.bits = OrderedDict([
            (Status.StatusTypes.carry, False),
            (Status.StatusTypes.zero, False),
            (Status.StatusTypes.interrupt, True),
            (Status.StatusTypes.decimal, False),
            (Status.StatusTypes.unused1, False),
            (Status.StatusTypes.unused2, True),
            (Status.StatusTypes.overflow, False),
            (Status.StatusTypes.negative, False),
        ])

    def update(self, instruction: Instruction, value: int):
        if instruction.sets_zero_bit:
            self.bits[Status.StatusTypes.zero] = not bool(np.uint8(value))
        if instruction.sets_negative_bit:
            self.bits[Status.StatusTypes.negative] = bool(np.uint8(value) & 0b10000000)
        if instruction.sets_overflow_bit_from_value:
            self.bits[Status.StatusTypes.overflow] = bool(np.uint8(value) & 0b01000000)

    def to_int(self):
        value = 0
        for i, bit in enumerate(self.bits.values()):
            value += int(bit) * math.pow(2, i)
        return int(value)

    def from_int(self, value: int, bits_to_ignore: List[int] = []):
        for i, key in enumerate(self.bits.keys()):
            if i in bits_to_ignore:
                continue
            self.bits[key] = bool(np.uint8(value) & (1 << i))

    def status_of_flag(self, flag: StatusTypes) -> bool:
        return self.bits[flag]

    def set_status_of_flag(self, flag: StatusTypes, value: bool):
        self.bits[flag] = value
