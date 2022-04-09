from modules.destiny2_api import Destiny2API, EntityType



if __name__ == '__main__':
    client = Destiny2API()
    result = client.get_entity_definition(EntityType.InventoryItem, "2782847179")
    print(result)