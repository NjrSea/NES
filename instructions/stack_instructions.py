from addressing import ImplicitAddressing
from instructions.generic_instruction import Instruction
from instructions.base_instructions import StackPush, StackPull


# stack push instructions
class Php(ImplicitAddressing, StackPush):
    identifier_byte = bytes([0x08])

    @classmethod
    def data_to_push(cls, cpu):
        return cpu.status_reg.to_int()


class Pha(ImplicitAddressing, StackPush):
    identifier_byte = bytes([0x48])

    @classmethod
    def data_to_push(cls, cpu):
        return cpu.a_reg


class Txs(ImplicitAddressing, StackPush):
    identifier_byte = bytes([0x9A])

    @classmethod
    def data_to_push(cls, cpu):
        return cpu.x_reg


# stack pull instructions
class Plp(ImplicitAddressing, StackPull):
    identifier_byte = bytes([0x28])

    @classmethod
    def write_pulled_data(cls, cpu, pulled_data):
        cpu.status_reg.from_int(pulled_data)


class Pla(ImplicitAddressing, StackPull):
    identifier_byte = bytes([0x68])

    @classmethod
    def write_pulled_data(cls, cpu, pulled_data):
        cpu.a_reg = pulled_data


class Tsx(ImplicitAddressing, StackPull):
    identifier_byte = bytes([0xBA])

    @classmethod
    def write_pulled_data(cls, cpu, pulled_data):
        cpu.x_reg = pulled_data
