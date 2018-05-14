from typing import List
from abc import abstractmethod, ABC, abstractproperty


class MemoryOwnerMixin(ABC):
    @abstractproperty
    @property
    def memory_start_location(self) -> int:
        """
        inclusive
        """
        pass

    @abstractproperty
    @property
    def memory_end_location(self) -> int:
        """
        inclusive
        """
        pass

    @abstractmethod
    def get_memory(self) -> List[int]:
        pass

    def get(self, position: int):
        """
        get bytes at given position and size, could be multiple bytes
        """
        return self.get_memory()[position - self.memory_start_location]

    def set(self, position: int, value: int, size: int = 1):
        """
        gets int at given position
        """
        for i in range(size):
            self.get_memory()[position - self.memory_start_location - i] = value

