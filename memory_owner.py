from typing import List
from abc import abstractmethod, ABC, abstractproperty


class MemoryOwnerMixin(ABC):
    @abstractproperty
    def memory_start_location(self):
        """
        inclusive
        """
        pass

    @abstractproperty
    def memory_end_location(self):
        """
        inclusive
        """
        pass

    @abstractmethod
    def get_memory(self) -> List[bytes]:
        pass

    def get_bytes(self, position: int, size: int = 1) -> bytes:
        """
        get byte at given position and size
        """
        return self.get_memory()[position : position + size]

    def set_byte(self, position: int, value: bytes):
        """
        gets bytes at given position
        """
        if len(value) > 1:
            raise Exception("Trying to store multiple bytes")
        self.get_memory()[position] = value

