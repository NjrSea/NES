from typing import Optional
import numpy as np


"""
  http://nesdev.com/6502.txt

  ADDRESSING MODES

   Instructions need operands to work on. There are various ways of
  indicating where the processor is to get these operands. The different
  methods used to do this are called addressing modes. The 6502 offers 11
  modes, as described below.

  1) Immediate
  In this mode the operand's value is given in the instructions itself. In
  assembly language this is indicated by "#" before the operand.
  eg.  LDA #$0A - means "load the accumulator with the hex value 0A"
  In machine code different modes are indicated by different codes. So LDA
  would be translated into different codes depending on the addressing mode.
  In this mode, it is: $A9 $0A

  2 & 3) Absolute and Zero-page Absolute
  In these modes the operands address is given.
  eg.  LDA $31F6 - (assembler)
       $AD $31F6 - (machine code)
  If the address is on zero page - i.e. any address where the high byte is
  00 - only 1 byte is needed for the address. The processor automatically
  fills the 00 high byte.
  eg.  LDA $F4
       $A5 $F4
  Note the different instructions codes for the different modes.
  Note also that for 2 byte addresses, the low byte is store first, eg.
  LDA $31F6 is stored as three bytes in memory, $AD $F6 $31.
  Zero-page absolute is usually just called zero-page.

  4) Implied
  No operand addresses are required for this mode. They are implied by the
  instructions.
  eg.  TAX - (transfer accumulator contents to X-register)
       $AA

  5) Accumulator
  In this mode the instructions operates on data in the accumulator, so no
  operands are needed.
  eg.  LSR - logical bit shift right
       $4A

  6 & 7) Indexed and Zero-page Indexed
  In these modes the address given is added to the value in either the X or
  Y index register to give the actual address of the operand.
  eg.  LDA $31F6, Y
       $D9 $31F6
       LDA $31F6, X
       $DD $31F6
  Note that the different operation codes determine the index register used.
  In the zero-page version, you should note that the X and Y registers are
  not interchangeable. Most instructions which can be used with zero-page
  indexing do so with X only.
  eg.  LDA $20, X
       $B5 $20

  8) Indirect
  This mode applies only to the JMP instructions - JuMP to new location. It is
  indicated by parenthesis around the operand. The operand is the address of
  the bytes whose value is the new location.
  eg.  JMP ($215F)
  Assume the following -        byte      value
                                $215F     $76
                                $2160     $30
  This instructions takes the value of bytes $215F, $2160 and uses that as the
  address to jump to - i.e. $3076 (remember that addresses are stored with
  low byte first).

  9) Pre-indexed indirect
  In this mode a zer0-page address is added to the contents of the X-register
  to give the address of the bytes holding the address of the operand. The
  indirection is indicated by parenthesis in assembly language.
  eg.  LDA ($3E, X)
       $A1 $3E
  Assume the following -        byte      value
                                X-reg.    $05
                                $0043     $15
                                $0044     $24
                                $2415     $6E

  Then the instructions is executed by:
  (i)   adding $3E and $05 = $0043
  (ii)  getting address contained in bytes $0043, $0044 = $2415
  (iii) loading contents of $2415 - i.e. $6E - into accumulator

  Note a) When adding the 1-byte address and the X-register, wrap around
          addition is used - i.e. the sum is always a zero-page address.
          eg. FF + 2 = 0001 not 0101 as you might expect.
          DON'T FORGET THIS WHEN EMULATING THIS MODE.
       b) Only the X register is used in this mode.

  10) Post-indexed indirect
  In this mode the contents of a zero-page address (and the following byte)
  give the indirect addressm which is added to the contents of the Y-register
  to yield the actual address of the operand. Again, inassembly language,
  the instructions is indicated by parenthesis.
  eg.  LDA ($4C), Y
  Note that the parenthesis are only around the 2nd byte of the instructions
  since it is the part that does the indirection.
  Assume the following -        byte       value
                                $004C      $00
                                $004D      $21
                                Y-reg.     $05
                                $2105      $6D
  Then the instructions above executes by:
  (i)   getting the address in bytes $4C, $4D = $2100
  (ii)  adding the contents of the Y-register = $2105
  (111) loading the contents of the byte $2105 - i.e. $6D into the
        accumulator.
  Note: only the Y-register is used in this mode.

  11) Relative
  This mode is used with Branch-on-Condition instructions. It is probably
  the mode you will use most often. A 1 byte value is added to the program
  counter, and the program continues execution from that address. The 1
  byte number is treated as a signed number - i.e. if bit 7 is 1, the number
  given byt bits 0-6 is negative; if bit 7 is 0, the number is positive. This
  enables a branch displacement of up to 127 bytes in either direction.
  eg  bit no.  7 6 5 4 3 2 1 0    signed value          unsigned value
      value    1 0 1 0 0 1 1 1    -39                   $A7
      value    0 0 1 0 0 1 1 1    +39                   $27
  Instruction example:
    BEQ $A7
    $F0 $A7
  This instructions will check the zero status bit. If it is set, 39 decimal
  will be subtracted from the program counter and execution continues from
  that address. If the zero status bit is not set, execution continues from
  the following instructions.
  Notes:  a) The program counter points to the start of the instructions
  after the branch instructions before the branch displacement is added.
  Remember to take this into account when calculating displacements.
          b) Branch-on-condition instructions work by checking the relevant
  status bits in the status register. Make sure that they have been set or
  unset as you want them. This is often done using a CMP instructions.
          c) If you find you need to branch further than 127 bytes, use the
  opposite branch-on-condition and a JMP.
"""


class Addressing(object):
    data_length = 0

    @classmethod
    def get_instruction_length(cls):
        return cls.data_length + 1

    @classmethod
    def get_offset(cls, cpu):
        return 0


class ImplicitAddressing(Addressing):
    """
    instructions that have data passed
    example: CLD
    """
    data_length = 0


class ImmediateReadAddressing(Addressing):
    """
    takes a value from the instructions data
    example: STA #7
    example: 8D  07
    """
    data_length = 1

    @classmethod
    def get_data(cls, cpu: 'cpu.CPU', memory_address: int, data_bytes) -> Optional[int]:
        return data_bytes[0]


class AccumulatorAdressing(Addressing):
    """
    get value from accumulator
    """
    data_length = 0

    @classmethod
    def get_data(cls, cpu: 'cpu.CPU', memory_address: int, data_bytes) -> Optional[int]:
        return cpu.a_reg


class AbsoluteAddressing(Addressing):
    """
    looks up an absolute memory address and returns the value
    example: STA 12 34
    example: 8D  34 12
    """
    data_length = 2

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        return np.uint16(int.from_bytes(data_bytes, byteorder='little') + cls.get_offset(cpu))


class XRegOffset(object):
    @classmethod
    def get_offset(cls, cpu):
        return np.uint16(cpu.x_reg)


class YRegOffset(object):
    @classmethod
    def get_offset(cls, cpu):
        return np.uint16(cpu.y_reg)


class AbsoluteAddressingXOffset(XRegOffset, AbsoluteAddressing):
    """
    looks up an absolute memory address including adding the x reg to tht address returns the value
    at that address
    example: STA $12 34
    example: 8D  ($3412+X)
    """


class AbsoluteAddressingYOffset(YRegOffset, AbsoluteAddressing):
    """
    looks up an absolute memory address including adding the x reg to tht address returns the value
    at that address
    example: STA $12 34
    example: 8D  ($3412+X)
    """


class ZeroPageAddressing(Addressing):
    """
    look up an absolute memory address in the first 256 bytes including adding the x reg to
    that address returns the value at that address
    example: STA $12
    memory_address: ($12 + #X)
    Note: can overflow
    """
    data_length = 1

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        address = np.uint8(int.from_bytes(data_bytes, byteorder='little') + cls.get_offset(cpu))
        # check for overflow
        return address


class ZeroPageAddressingWithX(XRegOffset, ZeroPageAddressing):
    """
    adds the x reg offset to an absolute memory address in the first 256 bytes
    """


class ZeroPageAddressingWithY(YRegOffset, ZeroPageAddressing):
    """
    adds the y reg offset to an absolute memory address in the first 256 bytes
    """


class RelativeAddressing(Addressing):
    """
    offset from current PC
    """
    data_length = 1

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        # get the program counter
        current_address = cpu.pc_reg

        # offset by value in instructions
        return current_address + np.uint16(int.from_bytes(data_bytes, byteorder='little'))


class IndirectBase(Addressing):
    @classmethod
    def get_address(cls, cpu, data_bytes: bytes):
        # look up the bytes at [original_address, original_address + 1]
        lsb_location = np.uint16(super().get_address(cpu, data_bytes))
        msb_location = np.uint16(lsb_location + 1)

        # wrap around on page boundaries
        if msb_location % 0x100 == 0:
            msb_location = np.uint16(lsb_location - 0xFF)

        lsb = cpu.get_memory(lsb_location)
        msb = cpu.get_memory(msb_location)

        return np.uint16(int.from_bytes(bytes([lsb, msb]), byteorder='little'))


class IndirectAddressing(IndirectBase, AbsoluteAddressing):
    """
    indirect addressing
    """


class IndirectAddressingWithX(IndirectBase, ZeroPageAddressingWithX):
    """
    adds the x reg before indirection
    """


class IndirectAddressingWithY(IndirectBase, ZeroPageAddressing):
    """
    adds the y reg after indirection
    """
    @classmethod
    def get_address(cls, cpu, data_bytes: bytes):
        return super().get_address(cpu, data_bytes) + cpu.y_reg

