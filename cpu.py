import  instructions as instructions_file
from generic_instruction import Instruction
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

        self.rom = None  # type: ROM
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
        for memory_owner in self.memory_owners:
            if memory_owner.memory_start_location <= location <= memory_owner.memory_end_location:
                return memory_owner

        raise Exception('Cannot find memory owner')

    def find_instructions(self, cls):
        """
        finds all available instructions
        """
        subclasses = [subc for subc in cls.__subclasses__() if subc.identifier_byte is not None]
        return subclasses + [g for s in cls.__subclasses__() for g in self.find_instructions(s)]

    def run_rom(self, rom: ROM):
        # unload old rom
        if self.rom is not None:
            self.memory_owners.remove(self.rom)

        # load rom
        self.rom = rom
        self.pc_reg = 0xC000

        # load the rom program instructions into memory
        self.memory_owners.append(self.rom)

        instructions_list = self.find_instructions(Instruction)
        instructions = {}
        for instruction in instructions_list:
            instructions[instruction.identifier_byte] = instruction

        # run program
        self.running = True
        while self.running:
            identifier_byte = self.get_memory_owner(self.pc_reg).get(self.pc_reg)
            instruction = instructions.get(identifier_byte, None)

            if instruction is None:
                raise Exception("Instruction not found: {}".format(identifier_byte.hex()))

            # get the data bytes
            data_bytes = self.rom.get(self.pc_reg + 1, instruction.data_length)

            # print out diagnostic information
            # example: C000  4C F5 C5  JMP $C5F5                A:00 X:00 Y:00 P:24 SP:FD CYC:0
            print('{}, {}, {}, A:{}, X:{}, Y:{}, P:{}, SP:{}'.format(hex(self.pc_reg),
                                                                     (identifier_byte+data_bytes).hex(),
                                                                     instruction.__name__,
                                                                     self.a_reg,
                                                                     self.x_reg,
                                                                     self.y_reg,
                                                                     hex(self.status_reg.to_int()),
                                                                     hex(self.sp_reg)))

            self.pc_reg += instruction.get_instruction_length()

            # we have a valid instruction
            instruction.execute(self, data_bytes)



