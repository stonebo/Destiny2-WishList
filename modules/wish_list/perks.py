import os
from .inventory_item import Destiny2Inventory
from ..utils import workspace


class Perks(Destiny2Inventory):
    
    def json_data_path(self):
        file_name = f"{self.hash_id}.json"
        return os.path.join(workspace(),
                            "data",
                            "perks",
                            file_name)
