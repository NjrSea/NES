from typing import List

from memory_owner import MemoryOwnerMixin


class PPU(MemoryOwnerMixin, object):
    def __init__(self):
        zero_byte = bytes.fromhex('00')
        self.memory = [zero_byte] * 8  # type: List[bytes]

    def get_memory(self) -> List[bytes]:
        return self.memory

    @property
    def memory_start_location(self):
        return 0x2000

    @property
    def memory_end_location(self):
        return 0x2007
