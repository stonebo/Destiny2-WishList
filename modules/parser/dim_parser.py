import re


class DimParser:
    def __init__(self, wish_item: str):
        """

        Args:
            wish_item (str): DIM format wishlist string

        Examples:
            dimwishlist:item=3886416794&perks=839105230,2420895100,509074078,3078487919
        """
        if self._check(wish_item) is False:
            raise ValueError(f"Wish Item Format Invalid: {wish_item}")
        self.wish_item = wish_item

    def _check(self, wish_item: str) -> bool:
        compile = re.compile("dimwishlist:item=[0-9]+&perks=[0-9,]+")
        if compile.match(wish_item) is None:
            return False
        else:
            return True

    def fetch_item_id(self) -> str:
        wish_item_detal = self.wish_item.split(":")[-1]
        item = wish_item_detal.split("&")[0]
        item_id = item.split("=")[-1]
        return item_id

    def fetch_perk_list(self) -> list:
        wish_item_detal = self.wish_item.split(":")[-1]
        perk = wish_item_detal.split("&")[-1]
        perk_ids = perk.split("=")[-1]
        return perk_ids.split(",")