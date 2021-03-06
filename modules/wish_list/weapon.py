import logging
import os
import json as jsonlib
from typing import List
from .perks import Perks
from ..utils import workspace, gen_hash
from .inventory_item import Destiny2Inventory

logger = logging.getLogger()


class Destiny2Weapon(Destiny2Inventory):
    def __init__(self, hash_id: str, profile: str = "default"):
        self.profile = profile
        self.resp = self._get_resp_from_bungie(hash_id)
        self.perks = []
        self._load_exist_perks()

    @property
    def screenshot_url(self) -> str:
        return self._build_icon_link(self.response_data['screenshot'])

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
        water_mark = self.response_data.get('iconWatermarkShelved',
                                            self.response_data['iconWatermark'])
        return self._build_icon_link(water_mark)

    @property
    def json_data_path(self):
        return os.path.join(workspace(),
                            "data",
                            "wish_list",
                            self.profile,
                            self.category,
                            self.weapon_type,
                            self.name.replace(' ', '_').lower(),
                            "data.json")

    @property
    def category(self):
        _weapon_category = {
            "2": "KineticWeapon",
            "3": "EnergyWeapon",
            "4": "PowerWeapon"
        }
        return _weapon_category.get(str(self.response_data['itemCategoryHashes'][0]), "Unknow")

    @property
    def icon_list(self) -> List[tuple]:
        return [
            ("icon", self.icon_url),
            ("watermark", self.water_mark),
            ("screenshot", self.screenshot_url),
        ]

    def _load_exist_data(self) -> dict:
        _file = self.json_data_path
        if os.path.isfile(_file):
            with open(_file, "r") as fp:
                json_data = jsonlib.load(fp)
        else:
            json_data = None
        return json_data

    def _load_exist_perks(self):
        try:
            _json_data = self._load_exist_data()
        except jsonlib.JSONDecodeError:
            _json_data = None
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

    def _add_perks(self,
                  perk_list: list,
                  pvp: bool = False,
                  pve: bool = False,
                  god_roll: bool = False):
        hash_id = gen_hash(f"{','.join(perk_list)}{str(pvp)}{str(pve)}{str(god_roll)}")
        if hash_id not in self._get_perks_hash():
            _template = {
                "perks": self._gen_perk_list(perk_list),
                "pvp": pvp,
                "pve": pve,
                "god_roll": god_roll,
                "hash": hash_id
            }
            self.perks.append(_template)
        else:
            logger.warning(f"{self.name}'s perk {','.join(perk_list)} already exist")

    def _gen_perk_list(self, perk_id_list: list):
        perk_list = []
        for perk_id in perk_id_list:
            _perk = Perks(perk_id)
            _perk.save()
            perk_list.append(_perk.to_json())
        return perk_list

    def _get_perks_hash(self):
        return [prek['hash'] for prek in self.perks]

    def add_perks(self, perk_list: list, god_roll: bool = False):
        self._add_perks(perk_list=perk_list, pvp=False, pve=False, god_roll=god_roll)

    def add_pvp_perks(self, perk_list: list, god_roll: bool = False):
        self._add_perks(perk_list=perk_list, pvp=True, pve=False, god_roll=god_roll)

    def add_pve_perks(self, perk_list: list, god_roll: bool = False):
        self._add_perks(perk_list=perk_list, pvp=False, pve=True, god_roll=god_roll)

    def add_both_perks(self, perk_list: list, god_roll: bool = False):
        self._add_perks(perk_list=perk_list, pvp=True, pve=True, god_roll=god_roll)
