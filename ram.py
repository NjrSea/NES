from typing import List

from memory_owner import MemoryOwnerMixin

KB = 1024


class RAM(MemoryOwnerMixin, object):
    def __init__(self):
        # TODO byte vs int?
        zero_byte = bytes.fromhex('00')
        self.memory = [zero_byte] * KB * 2  # type: List[int]

    def get_memory(self) -> List[bytes]:
        return self.memory

    @property
    def memory_start_location(self):
        return 0x0

    @property
    def memory_end_location(self):
        return 0x1FFF
