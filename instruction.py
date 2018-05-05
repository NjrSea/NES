from abc import ABC, abstractmethod, abstractproperty

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

    @abstractproperty
    def identifier_byte(self) -> bytes:
        return None

    @abstractproperty
    def instruction_length(self) -> int:
        return 1

    @abstractmethod
    def execute(self, *args):
        print(self.__str__())


# data instructions
class LDAImmInstruction(Instruction):
    identifier_byte = bytes.fromhex('A9')
    instruction_length = 2

    def execute(self, cpu, data_bytes):
        # load value into accumulator register
        cpu.a_reg = data_bytes


# status instructions
class SEIInstruction(Instruction):
    identifier_byte = bytes.fromhex('78')
    instruction_length = 1

    def execute(self, cpu, data_bytes):
        # set the instruction flag to 1
        cpu.status_reg.interrupt = True


class CLDInstruction(Instruction):
    identifier_byte = bytes.fromhex('D8')
    instruction_length = 1

    def execute(self, cpu, data_bytes):
        cpu.status_reg.decimal_bit = False


class STAAbsInstruction(Instruction):
    identifier_byte = bytes.fromhex('8D')
    instruction_length = 3

    def execute(self, cpu, data_bytes):
        # take value from A register and put it in memory
        memory_address = int.from_bytes(data_bytes, byteorder='little')
        val_to_store = cpu.a_reg
        memory_owner = cpu.get_memory_owner(memory_address)
        memory_owner.set_byte(memory_address, val_to_store)



