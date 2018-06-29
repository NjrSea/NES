from enum import Enum
from typing import List

import re

from addressing import ImmediateReadAddressing, Addressing, ZeroPageAddressing, ZeroPageAddressingWithX, \
    AbsoluteAddressing, AbsoluteAddressingXOffset, AbsoluteAddressingYOffset, IndirectAddressingWithX, \
    IndirectAddressingWithY, ZeroPageAddressingWithY, AccumulatorAdressing

class_pattern = r'(\S*)\s*(\w*).{11}(\w*).*'
compiled_class_pattern = re.compile(class_pattern)

instruction_classes = []


class Numbers(Enum):
    BYTE = 1
    SHORT = 2


def int_to_byte(value: int) -> int:
    """
    cast a single int to a byte
    """
    # TODO: signed values? hahahah
    return value % 256


def short_to_bytes(value: int) -> List[int]:
    """
    cast a short to 2 ints
    """
    upper = int_to_byte(value >> 8)
    lower = int_to_byte(value)
    return [upper, lower]


def bytes_to_short(*, upper: int, lower: int) -> int:
    """
    cast 2 ints to a short
    """
    return (upper << 8) | lower


def num_of_bytes_from_bytes(value: bytes) -> int:
    value = int.from_bytes(value, byteorder='little')
    return num_of_bytes_from_int(value)


def num_of_bytes_from_int(value: int) -> int:
    if value is None:
        raise Exception('invalid value type of None')
    if value <= 0xFF:
        return 1
    return 2


def description_to_addressing(description: str) -> Addressing:
    """
    turns a string description into a addressing type
    based on format from http://e-tradition.net/bytes/6502/6502_instruction_set.html
    """
    return {
        'immidiate': ImmediateReadAddressing,
        'zeropage': ZeroPageAddressing,
        'zeropage,X': ZeroPageAddressingWithX,
        'zeropage,Y': ZeroPageAddressingWithY,
        'absolute': AbsoluteAddressing,
        'absolute,X': AbsoluteAddressingXOffset,
        'absolute,Y': AbsoluteAddressingYOffset,
        '(indirect,X)': IndirectAddressingWithX,
        '(indirect),Y': IndirectAddressingWithY,
        'accumulator': AccumulatorAdressing,
    }[description]


def generate_classes_from_string(class_type, class_string: str):
    """
    creates a list of classes from descriptor
    based on format from http://e-tradition.net/bytes/6502/6502_instruction_set.html
    """
    for class_entry in [line.strip() for line in class_string.split('\n') if line != '']:
        matches = compiled_class_pattern.match(class_entry)
        addressing = description_to_addressing(matches.group(1))
        class_name = matches.group(2) + matches.group(1)
        class_name = re.sub('[(),]', '', class_name)
        yield type(class_name, (addressing, class_type,), {'identifier_byte': bytes([int(matches.group(3), 16)])})