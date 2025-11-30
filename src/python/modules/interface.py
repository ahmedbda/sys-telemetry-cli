from abc import ABC, abstractmethod

# abstract class and it's abstract method to make the different getters for different information
# abstract as we cannot just "get" information, a type (network, system, ...) is needed
class Probe(ABC):
    @abstractmethod
    def run(self):
        pass