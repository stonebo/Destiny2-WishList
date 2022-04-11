import os
from typing import List
from .inventory_item import Destiny2Inventory
from ..utils import workspace


class Perks(Destiny2Inventory):
    @property
    def json_data_path(self):
        file_name = f"{self.hash_id}.json"
        return os.path.join(workspace(),
                            "data",
                            "perks",
                            file_name)

    @property
    def icon_list(self) -> List[tuple]:
        return [
            (self.hash_id, self.icon_url)
        ]

    def to_json(self):
        _template = {
            "hash": self.hash_id,
            "name": self.name,
            "icons": {
                "icon": self.icon_url,
            }
        }
        return _template
