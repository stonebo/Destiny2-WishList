import json
import logging
import os
import json as jsonlib
from ..utils import workspace

logger = logging.getLogger()


class Destiny2Weapon:
    Baseurl = "https://bungie.net"

    def __init__(self, reps: dict):
        self.resp = reps
        self.perks = []
        self._load_exist_perks()

    @property
    def response_data(self):
        return self.resp['Response']

    @property
    def name(self) -> str:
        return self.response_data['displayProperties']['name']

    @property
    def icon_url(self) -> str:
        return f"{self.Baseurl}{self.response_data['displayProperties']['icon']}"

    @property
    def hash_id(self) -> str:
        return self.response_data['hash']

    @property
    def screenshot_url(self) -> str:
        return f"{self.Baseurl}{self.response_data['screenshot']}"

    @property
    def damage_type(self) -> str:
        _type = {
            "1": "Kinetic",
            "2": "Arc",
            "3": "Thermal/Solar",
            "4": "Void",
            "6": "Stasis"
        }
        return _type.get(str(self.response_data['defaultDamageType']), "Unknow")

    @property
    def weapon_type(self) -> str:
        return self.response_data['itemTypeDisplayName']

    @property
    def water_mark(self) -> str:
        return f"{self.Baseurl}{self.response_data['iconWatermarkShelved']}"

    @property
    def json_data_path(self):
        file_name = f"{self.name.replace(' ', '_').lower()}.json"
        return os.path.join(workspace(),
                            "data",
                            "wish_list",
                            self.category,
                            self.weapon_type,
                            file_name)

    @property
    def category(self):
        _weapon_category = {
            "2": "KineticWeapon",
            "3": "EnergyWeapon",
            "4": "PowerWeapon"
        }
        return _weapon_category.get(str(self.response_data['itemCategoryHashes'][0]), "Unknow")

    def _load_exist_data(self) -> dict:
        _file = self.json_data_path
        if os.path.isfile(_file):
            with open(_file, "r") as fp:
                json_data = json.load(fp)
        else:
            json_data = None
        return json_data

    def _load_exist_perks(self):
        _json_data = self._load_exist_data()
        if _json_data is not None:
            for perk in _json_data.get("perks", []):
                self.perks.append(perk)

    def to_json(self):
        _json = {
            "name": self.name,
            "id": self.hash_id,
            "damage_type": self.damage_type,
            "weapon_type": self.weapon_type,
            "category": self.category,
            "icons": {
                "icon": self.icon_url,
                "screenshot": self.screenshot_url,
                "water_mark": self.water_mark
            },
            "perks": self.perks
        }
        return _json

    def save(self):
        _file = self.json_data_path
        _dir = os.path.dirname(_file)
        if os.path.isdir(_dir) is False:
            os.makedirs(_dir, exist_ok=True)


    def _add_perks(self,
                  perk_list: list,
                  pvp: bool = False,
                  pve: bool = False,
                  god_roll: bool = False):
        _template = {
            "perks": perk_list,
            "pvp": pvp,
            "pve": pve,
            "god_roll": god_roll
        }
        self.perks.append(_template)

    def add_pvp_perks(self, perk_list: list, god_roll: bool = False):
        self._add_perks(perk_list=perk_list, pvp=True, pve=False, god_roll=god_roll)

    def add_pve_perks(self, perk_list: list, god_roll: bool = False):
        self._add_perks(perk_list=perk_list, pvp=False, pve=True, god_roll=god_roll)

    def add_both_perks(self, perk_list: list, god_roll: bool = False):
        self._add_perks(perk_list=perk_list, pvp=True, pve=True, god_roll=god_roll)
