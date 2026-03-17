from abc import ABC, abstractmethod

class RateProvider(ABC):
    @abstractmethod
    def fetch_rates(self) -> dict:
        pass

class RateCache(ABC):
    @abstractmethod
    def load_rates(self):
        pass

    @abstractmethod
    def save_rates(self, rates):
        pass

class RateSource(ABC):
    @abstractmethod
    def get_rates(self) -> dict:
        pass