from instructions.generic_instruction import Instruction
from memory_owner import MemoryOwnerMixin
from ppu import PPU
from ram import RAM
from rom import ROM
from status import Status

import numpy as np

import instructions.instructions as i_file
import instructions.jump_instructions as j_file
import instructions.load_instructions as l_file
import instructions.branch_instructions as b_file
import instructions.store_instructions as s_file
import instructions.bit_instructions as bit_file
import instructions.stack_instructions as stack_file
import instructions.arithmetic_instructions as a_file


class CPU:
    def __init__(self, ram: RAM, ppu: PPU):
        # status registers: store a single byte
        self.status_reg = None  # type: Status

        # counter registers: store a single byte
        self.pc_reg = None  # program counter 2bytes
        self.sp_reg = None  # stack pointer

        # data registers: store a single byte
        self.x_reg = None  # x register
        self.y_reg = None  # y register
        self.a_reg = None  # a register

        # program counter stores current execution point
        self.running = False

        self.rom = None  # type: ROM
        self.ram = ram
        self.ppu = ppu

        self.memory_owners = [  # type: List[MemoryOwnerMixin]
            self.ram,
            self.ppu,
        ]

        self.instruction = None
        self.data_bytes = None

        # create the instructions that cpu can interpret
        instructions_list = self._find_instructions(Instruction)
        self.instructions = {}
        for instruction in instructions_list:
            if instruction in self.instructions:
                raise Exception('Duplicate instruction identifier bytes')
            self.instructions[instruction.identifier_byte] = instruction

        self.stack =[]

        # These instructions are implied mode, have a length of one byte and require machine cycles as indicated.
        # The "PuLl" operations are known as "POP" on most other microprocessors. With the 6502, the stack is always
        # on page one ($100-$1FF) and works top down.
        # http://www.6502.org/tutorials/6502opcodes.html
        self.stack_offset = 0x100

    def start_up(self):
        """
        set the initial values of cpu registers
        status: NVssDIZC
                00000100 (IRQ disabled)
        x, y, a regs: 0
        stack pointer: $FD
        $4017: 0 (sound chanel disabled)
        $4015: 0 (frame IRQ disabled)
        $4000-$400F: 0 (sound registers) """
        self.pc_reg = np.uint16(0)  # 2 bytes
        self.status_reg = Status()
        self.sp_reg = np.uint8(0xFD)

        self.x_reg = np.uint8(0)
        self.y_reg = np.uint8(0)
        self.a_reg = np.uint8(0)

        # TODO memory sets

    def stack_push(self, data_to_push: int, num_bytes: int = 1):
        self.set_memory(self.stack_offset + self.sp_reg, data_to_push, num_bytes)
        self.increase_stack_size(num_bytes)
        self.stack.append(hex(data_to_push))
        print('stack push: ', self.stack)

    def stack_pop(self, num_bytes: int = 1):
        self.decrease_stack_size(num_bytes)
        if self.stack.__len__() > 0:
            print('stack pop: ', self.stack.pop(), self.stack)
        return self.get_memory(self.stack_offset + self.sp_reg, num_bytes)

    def get_memory(self, location: int, num_bytes: int = 1) -> int:
        """
        return a byte from a given memory location
        """
        memory_owner = self._get_memory_owner(location)
        return memory_owner.get(location, num_bytes)

    def _get_memory_owner(self, location: int) -> MemoryOwnerMixin:
        """
        return the owner of a memory location
        """
        for memory_owner in self.memory_owners:
            if memory_owner.memory_start_location <= location <= memory_owner.memory_end_location:
                return memory_owner

        raise Exception('Cannot find memory owner')

    def set_memory(self, location: int, value: int, num_bytes: int = 1):
        """
        sets the memory at a location to a value
        """
        memory_owner = self._get_memory_owner(location)
        memory_owner.set(location, value, num_bytes)

    def _find_instructions(self, cls):
        """
        finds all available instructions
        """
        subclasses = [subc for subc in cls.__subclasses__() if subc.identifier_byte is not None]
        return subclasses + [g for s in cls.__subclasses__() for g in self._find_instructions(s)]

    def increase_stack_size(self, size: int):
        """
        increase stack size by decreasing the stack pointer
        """
        self.sp_reg -= np.uint8(size)

    def decrease_stack_size(self, size: int):
        """
        decrease stack size by decreasing the stack pointer
        """
        self.sp_reg += np.uint8(size)

    def load_rom(self, rom: ROM):
        # unload old rom
        if self.rom is not None:
            self.memory_owners.remove(self.rom)

        # load rom
        self.rom = rom
        self.pc_reg = np.uint16(0xC000)

        # load the rom program instructions into memory
        self.memory_owners.append(self.rom)

    def identify(self):
        identifier_byte = self._get_memory_owner(self.pc_reg).get(self.pc_reg)

        if isinstance(identifier_byte, np.uint8):
            identifier_byte = bytes([identifier_byte])

        self.instruction = self.instructions.get(identifier_byte, None)

        if self.instruction is None:
            raise Exception("Instruction not found: {}".format(identifier_byte.hex()))

        # get the data bytes
        if self.instruction.data_length > 0:
            next_to_pc_reg = self.pc_reg + np.uint16(1)
            self.data_bytes = self._get_memory_owner(next_to_pc_reg).get(next_to_pc_reg, self.instruction.data_length)

            # check type
            if isinstance(self.data_bytes, np.uint8):
                self.data_bytes = bytes([self.data_bytes])
        else:
            self.data_bytes = bytes()

        # print out diagnostic information
        # example: C000  4C F5 C5  JMP $C5F5                A:00 X:00 Y:00 P:24 SP:FD CYC:0
        print('{}, {}, {}, A:{}, X:{}, Y:{}, P:{}, SP:{}'.format(hex(self.pc_reg),
                                                                 (identifier_byte + self.data_bytes).hex(),
                                                                 self.instruction.__name__,
                                                                 hex(self.a_reg),
                                                                 hex(self.x_reg),
                                                                 hex(self.y_reg),
                                                                 hex(self.status_reg.to_int()),
                                                                 hex(self.sp_reg)))

    def execute(self):
        self.pc_reg += np.uint16(self.instruction.get_instruction_length())

        value = self.instruction.execute(self, self.data_bytes)

        self.status_reg.update(self.instruction, value)

