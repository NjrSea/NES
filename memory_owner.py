from typing import List
from abc import abstractmethod, ABC, abstractproperty

from helpers import short_to_byte, bytes_to_short


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

    def get(self, position: int, size: int=1):
        """
        get bytes at given position and size, could be multiple bytes
        """
        if size == 1:
            return self.get_memory()[position - self.memory_start_location]
        elif size == 2:
            upper = self.get_memory()[position - self.memory_start_location]
            lower = self.get_memory()[position - self.memory_start_location - 1]
            return bytes_to_short(lower=lower, upper=upper)
        else:
            raise Exception('Unknown number size')

    def set(self, position: int, value: int, size: int = 1):
        """
        gets int at given position
        """
        if size == 1:
            self.get_memory()[position - self.memory_start_location] = value
        if size == 2:
            upper, lower = short_to_byte(value)
            self.get_memory()[position - self.memory_start_location] = upper
            self.get_memory()[position - self.memory_start_location - 1] = lower
        else:
            raise Exception('Unknown number size')

