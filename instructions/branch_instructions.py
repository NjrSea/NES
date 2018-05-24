from instructions.base_instructions import BranchSet, BranchClear
from status import Status
from addressing import AbsoluteAddressing


class Bcs(BranchSet):
    """
    Branch on Carry Set
    """
    identifier_byte = bytes([0xB0])
    bit = Status.StatusTypes.carry


class Beq(BranchSet):
    """
    Branch on Result Zero
    """
    identifier_byte = bytes([0xF0])
    bit = Status.StatusTypes.zero


class Bmi(BranchSet):
    """
    Branch on Result Minus
    branch on N = 1
    """
    identifier_byte = bytes([0x30])
    bit = Status.StatusTypes.negative


class Bvs(BranchSet):
    """
    Branch on Overflow Set
    branch on V = 1
    """
    identifier_byte = bytes([0x70])
    bit = Status.StatusTypes.overflow


class Bvc(BranchClear):
    """
    Branch on Overflow Clear
    branch on V = 0
    """
    identifier_byte = bytes([0x50])
    bit = Status.StatusTypes.overflow


class Bcc(BranchClear):
    """
    Branch on Carry Clear
    """
    identifier_byte = bytes([0x90])
    bit = Status.StatusTypes.carry


class Bne(BranchClear):
    """
    Branch on Result not Zero
    """
    identifier_byte = bytes([0xD0])
    bit = Status.StatusTypes.zero


class Bpl(BranchClear):
    """
    Branch on Result Plus
    branch on N = 0
    """
    identifier_byte = bytes([0x10])
    bit = Status.StatusTypes.negative
