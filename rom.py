from typing import List

from memory_owner import MemoryOwnerMixin

KB_SIZE = 1024


class ROM(MemoryOwnerMixin, object):
    memory_start_location = 0x4020
    memory_end_location = 0xFFFF

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

    def get(self, position: int, size: int=1) -> bytes:
        return self.get_memory()[position:position+size]

    def set(self, position: int, value: bytes):
        """
        read only memory
        """
        raise Exception('Trying to write to Read only Memory')

