from cpu import CPU
from ppu import PPU
from ram import RAM
from instructions.instructions import LDAImmInstruction, STAAbsInstruction, SEIInstruction, CLDInstruction
from mock import MagicMock
import pytest


# @pytest.fixture()
# def ram():
#     return MagicMock()
#
#
# @pytest.fixture()
# def ppu():
#     return MagicMock()


@pytest.fixture()
def cpu():
    ram = RAM()
    ppu = PPU()
    c: CPU = CPU(ram, ppu)
    c.rom = MagicMock()
    c.rom.memory_start_location = 0
    c.rom.memory_end_location = 0x1FFF
    c.start_up()
    return c


def check_instruction_bytes(instruction, instruction_bytes):
    assert instruction.identifier_byte == instruction_bytes[0:1]


def get_data_bytes(instruction_bytes):
    return instruction_bytes[1:]


def test_lda_imm(cpu):
    instruction_bytes = bytes([0xA9, 0x10])

    lda_imm = LDAImmInstruction()
    check_instruction_bytes(lda_imm, instruction_bytes)
    # check that value has been loaded into a register
    assert cpu.a_reg == 0
    lda_imm.execute(cpu, get_data_bytes(instruction_bytes))
    assert cpu.a_reg == get_data_bytes(instruction_bytes)[0]


def test_sta_abs(cpu):
    instruction_bytes = bytes([0x8D, 0x00, 0x20])

    instruction = STAAbsInstruction()
    check_instruction_bytes(instruction, instruction_bytes)
    # check that value has been loaded into a register
    value_to_store = 8
    cpu.a_reg = value_to_store
    instruction.execute(cpu, get_data_bytes(instruction_bytes))
    # 0x00 0x20 -> $2000 -> 8192
    memory_location = 8192
    owner = cpu._get_memory_owner(memory_location)
    value_at_memory_location = owner.get(memory_location)
    assert value_at_memory_location == value_to_store


def test_sei(cpu):
    instruction_bytes = bytes([0x78])

    instruction = SEIInstruction()
    check_instruction_bytes(instruction, instruction_bytes)
    cpu.status_reg.interrupt = False
    instruction.execute(cpu, get_data_bytes(instruction_bytes))
    assert cpu.status_reg.interrupt is True


def test_cld(cpu):
    instruction_bytes = bytes([0xD8])

    instruction = CLDInstruction()
    check_instruction_bytes(instruction, instruction_bytes)
    cpu.status_reg.decimal = True
    instruction.execute(cpu, get_data_bytes(instruction_bytes))
    assert cpu.status_reg.decimal is False
