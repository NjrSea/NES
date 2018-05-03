from instruction import Instruction, LDAInstruction, SEIInstruction, CLDInstruction
from rom import ROM
from status import Status


class CPU:
    def __init__(self):
        # status registers: store a single byte
        self.status_reg = None   # status register

        # counter registers: store a single byte
        self.pc_reg = None  # program counter
        self.sp_reg = None  # stack pointer

        # data registers: store a single byte
        self.x_reg = None  # x register
        self.y_reg = None  # y register
        self.a_reg = None  # a register

        # program counter stores current execution point
        self.running = False

        self.instruction_classes = [
            SEIInstruction,
            CLDInstruction,
            LDAInstruction,
        ]

        self.instruction_class_mapping = dict()

        for instruction_class in self.instruction_classes:
            self.instruction_class_mapping[instruction_class.identifier_byte] = instruction_class

        self.rom = None

    def start_up(self):
        """
        set the initial values of cpu registers
        status: NVssDIZC
                00000100 (IRQ disabled)
        x, y, a regs: 0
        stack pointer: $FD
        $4017: 0 (sound chanel disabled)
        $4015: 0 (frame IRQ disabled)
        $4000-$400F: 0 (sound registers)
        """
        self.pc_reg = 0
        self.status_reg = Status(bytes.fromhex('34'))
        self.sp_reg = bytes.fromhex('FD')

        # TODO change to int?
        self.x_reg = 0
        self.y_reg = 0
        self.a_reg = 0

        # TODO memory sets

    def run_rom(self, rom: ROM):
        # load rom
        self.rom = rom
        self.pc_reg = self.rom.header_size

        # run program
        self.running = True
        while self.running:
            # get the current byte at pc
            identifier_byte = self.rom.get_byte(self.pc_reg)

            # turn the byte into an Instruction
            # mapping[identifier_byte] will crash if identifier_byte is not valid
            # get method with default value of None can get value safely
            instruction_class = self.instruction_class_mapping.get(identifier_byte, None)
            if instruction_class is None:
                raise Exception("Instruction not found")

            # we have a valid instruction
            instruction = instruction_class()
            instruction.execute()

            self.pc_reg += instruction.instruction_length

    def process_instruction(self, instruction: Instruction):
        instruction.execute()

