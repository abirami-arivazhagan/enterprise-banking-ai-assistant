from abc import ABC, abstractmethod


class BaseChain(ABC):

    @abstractmethod
    def invoke(self, state: dict):
        pass