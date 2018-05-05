from typing import List

from memory_owner import MemoryOwnerMixin

KB_SIZE = 1024


class ROM(MemoryOwnerMixin, object):
    def __init__(self, rom_bytes: bytes):
        self.header_size = 16

        # TODO unhardcode
        self.num_prg_blocks = 2

        # program data starts after header
        # and lasts for a set number of 16KB blocks
        self.rom_bytes = rom_bytes
        self.prg_bytes = rom_bytes[self.header_size:
                                   self.header_size + 16 * KB_SIZE * self.num_prg_blocks]

    def get_memory(self) -> List[bytes]:
        return self.rom_bytes

    def set_byte(self, position: int, value: bytes):
        """
        read only memory
        """
        raise Exception('Trying to write to Read only Memory')

    @property
    def memory_start_location(self):
        return 0x4020

    @property
    def memory_end_location(self):
        return 0xFFFF

