from instruction import Instruction, LDAInstruction, SEIInstruction, CLDInstruction
from rom import ROM


class CPU:
    def __init__(self):
        self.registers = []

        # program counter stores current execution point
        self.running = False
        self.pc = None

        self.instruction_classes = [
            SEIInstruction,
            CLDInstruction,
            LDAInstruction,
        ]

        self.instruction_class_mapping = dict()

        for instruction_class in self.instruction_classes:
            self.instruction_class_mapping[instruction_class.identifier_byte] = instruction_class

        self.rom = None

    def load_rom(self, rom: ROM):
        self.rom = rom

    def run_rom(self, rom: ROM):
        # load rom
        self.rom = rom
        self.pc = self.rom.header_size

        # run program
        self.running = True
        while self.running:
            # get the current byte at pc
            identifier_byte = self.rom.get_byte(self.pc)

            # turn the byte into an Instruction
            # mapping[identifier_byte] will crash if identifier_byte is not valid
            # get method with default value of None can get value safely
            instruction_class = self.instruction_class_mapping.get(identifier_byte, None)
            if instruction_class is None:
                raise Exception("Instruction not found")

            # we have a valid instruction
            instruction = instruction_class()
            instruction.execute()

            self.pc += instruction.instruction_length


    def process_instruction(self, instruction: Instruction):
        instruction.execute()

