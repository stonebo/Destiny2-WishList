from modules.destiny2_api import Destiny2API, EntityType
from modules.parser import DimParser
from modules.wish_list.weapon_wish_list import Destiny2Weapon



if __name__ == '__main__':
    dim_wishlist = "dimwishlist:item=3886416794&perks=839105230,2420895100,509074078,3078487919"
    dim_parser = DimParser(dim_wishlist)
    client = Destiny2API()
    result = client.get_entity_definition(EntityType.InventoryItem, dim_parser.fetch_item_id())
    weapon = Destiny2Weapon(result)