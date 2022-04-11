import logging
from typing import List, Dict
from ..parser import DimParser, WishListParser
from ..destiny2_api import Destiny2API
from .weapon import Destiny2Weapon

logger = logging.getLogger()


class WishList:
    def __init__(self):
        """
        self.wish_list = {
            "<item id>": [
                parser
                ...
            ]
        }
        """
        self.destiny2_api_client = Destiny2API()
        self.wish_list: Dict[List[WishListParser]] = {}

    def import_dim_file(self, file_path: str):
        with open(file_path, "r") as fp:
            wishlist = fp.readlines()
        self.import_dim_list(wishlist)

    def import_dim_list(self, wish_list: list):
        for wish_item in wish_list:
            logger.info(f"Import wish list: {wish_item}")
            self.import_dim_wish_item(wish_item)

    def import_dim_wish_item(self, wish_item: str):
        _parse = DimParser(wish_item)
        self._import2wishlist(_parse)

    def _import2wishlist(self, parser: WishListParser):
        if parser.id in self.wish_list.keys():
            self.wish_list[parser.id].append(parser)
        else:
            self.wish_list[parser.id] = [parser]

    def append_wish_list(self):
        failed_list = []
        for item_id in self.wish_list.keys():
            logger.info(f"Processing Item ID {item_id}")
            try:
                item = Destiny2Weapon(item_id)
            except Exception as e:
                logger.warning(f"Get Destiny2 Definition Detail failed by Item ID {item_id}\n"
                               f"error: {e}")
                failed_list.append(item_id)
                continue
            else:
                logger.info(f"Processing {item_id}'s Perks")
                parser_list: list = self.wish_list[item_id]
                for index, parser in enumerate(parser_list):
                    logger.info(f"Add #{index} perk to item id {item_id}")
                    item.add_perks(parser.perk_list)
                item.save()




