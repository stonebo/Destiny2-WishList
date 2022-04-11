from abc import ABC, abstractmethod


class WishListParser(ABC):
    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def perk_list(self):
        pass
