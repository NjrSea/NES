from instruction import Instruction, instructions
from memory_owner import MemoryOwnerMixin
from ram import RAM
from ppu import PPU
from rom import ROM
from status import Status


class CPU:
    def __init__(self, ram: RAM, ppu: PPU):
        # status registers: store a single byte
        self.status_reg = None   # type: Status

        # counter registers: store a single byte
        self.pc_reg = None  # program counter
        self.sp_reg = None  # stack pointer

        # data registers: store a single byte
        self.x_reg = None  # x register
        self.y_reg = None  # y register
        self.a_reg = None  # a register

        # program counter stores current execution point
        self.running = False

        self.rom = None
        self.ram = ram
        self.ppu = ppu

        self.memory_owners = [  # type: List[MemoryOwnerMixin]
            self.ram,
            self.ppu,
        ]

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
        self.pc_reg = 0
        self.status_reg = Status()
        self.sp_reg = 0xFD

        # TODO change to int?
        self.x_reg = 0
        self.y_reg = 0
        self.a_reg = 0

        # TODO memory sets

    def get_memory(self, location: int) -> int:
        """
        return a byte from a given memory location
        """
        memory_owner = self.get_memory_owner(location)
        return memory_owner.get(location)

    def get_memory_owner(self, location: int) -> MemoryOwnerMixin:
        """
        return the owner of a memory location
        """
        if location is None:
            raise Exception('invalid location')

        if self.rom.memory_start_location <= location <= self.rom.memory_end_location:
            return self.rom

        for memory_owner in self.memory_owners:
            if memory_owner.memory_start_location <= location <= memory_owner.memory_end_location:
                return memory_owner

        raise Exception('Cannot find memory owner')

    def run_rom(self, rom: ROM):
        # load rom
        self.rom = rom
        self.pc_reg = self.rom.header_size

        # run program
        self.running = True
        while self.running:
            # get the current byte at pc
            identifier_byte = self.rom.get(self.pc_reg)

            # turn the byte into an Instruction
            # mapping[identifier_byte] will crash if identifier_byte is not valid
            # get method with default value of None can get value safely
            instruction: Instruction = instructions.get(identifier_byte, None)
            if instruction is None:
                raise Exception("Instruction not found")

            # get the data bytes
            data_bytes = self.rom.get(self.pc_reg + 1, instruction.data_length)

            # we have a valid instruction
            instruction.execute(self, data_bytes)

            self.pc_reg += instruction.get_instruction_length()


