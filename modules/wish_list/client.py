from ..parser import DimParser
from ..destiny2_api import Destiny2API
from .weapon_wish_list import Destiny2Weapon


class WishList:
    def __init__(self):
        self.destiny2_api_client = Destiny2API()
        self.wish_list = []

    def import_dim_list(self, wish_list: list):
        return [self.import_dim_wish_item(wish_item) for wish_item in wish_list]

    def import_dim_wish_item(self, wish_item: str):
        _parse = DimParser(wish_item)


