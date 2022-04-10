import logging

logger = logging.getLogger()


class Destiny2Weapon:
    Baseurl = "https://bungie.net"

    def __init__(self, reps: dict):
        self.resp = reps
        self.perks = []

    @property
    def response_data(self):
        return self.resp['Response']

    @property
    def name(self):
        return self.response_data['displayProperties']['name']

    @property
    def icon_url(self):
        return f"{self.Baseurl}{self.response_data['displayProperties']['icon']}"

    @property
    def hash_id(self):
        return self.response_data['hash']

    @property
    def screenshot_url(self):
        return f"{self.Baseurl}{self.response_data['screenshot']}"

    @property
    def damage_type(self):
        _type = {
            "1": "Kinetic",
            "2": "Arc",
            "3": "Thermal/Solar",
            "4": "Void",
            "6": "Stasis"
        }
        return _type.get(str(self.response_data['defaultDamageType']), "Unknow")

    @property
    def weapon_type(self):
        return self.response_data['itemTypeDisplayName']

    @property
    def water_mark(self):
        return f"{self.Baseurl}{self.response_data['iconWatermarkShelved']}"

    def to_json(self):
        pass

    def add_perks(self,
                  perk_list: list,
                  pvp: bool = False,
                  pve: bool = False,
                  god_roll: bool = False):
        pass

    def add_pvp_perks(self, perk_list: list, god_roll: bool = False):
        self.add_perks(perk_list=perk_list, pvp=True, pve=False, god_roll=god_roll)

    def add_pve_perks(self, perk_list: list, god_roll: bool = False):
        self.add_perks(perk_list=perk_list, pvp=False, pve=True, god_roll=god_roll)

    def add_both_perks(self, perk_list: list, god_roll: bool = False):
        self.add_perks(perk_list=perk_list, pvp=True, pve=True, god_roll=god_roll)
