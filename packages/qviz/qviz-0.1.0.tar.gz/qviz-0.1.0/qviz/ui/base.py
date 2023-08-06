from abc import ABC, abstractmethod

from typing import Callable

class UI(ABC):

    @abstractmethod
    def display(self, on_finished: Callable = None):
        pass
