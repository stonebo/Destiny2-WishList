from abc import ABC, abstractmethod
import os
import logging
import json as jsonlib
import urllib.parse
import requests
from ..destiny2_api import Destiny2API

logger = logging.getLogger()


class Destiny2Inventory(ABC):
    Baseurl = "https://bungie.net"

    def __init__(self, hash_id: str):
        self.resp = self._get_resp_from_bungie(hash_id)

    def _get_resp_from_bungie(self, hash_id: str):
        _api = Destiny2API()
        return _api.get_inventory_item_definition(hash_id)

    @property
    def response_data(self):
        return self.resp['Response']

    @property
    def hash_id(self) -> str:
        return self.response_data['hash']

    @property
    def name(self) -> str:
        return self.response_data['displayProperties']['name']

    @property
    def icon_url(self) -> str:
        return self._build_icon_link(self.response_data['displayProperties']['icon'])

    def save(self):
        _file = self.json_data_path
        _dir = os.path.dirname(_file)
        if os.path.isdir(_dir) is False:
            os.makedirs(_dir, exist_ok=True)
        with open(_file, "w+") as fp:
            jsonlib.dump(self.to_json(), fp, indent=4)
        logger.info(f"Json Data save to {_file}")

    def _build_icon_link(self, link_path: str):
        return str(urllib.parse.urljoin(self.Baseurl, link_path))

    def download_icon(self, icon_url: str):
        _dir = os.path.dirname(self.json_data_path)
        _icon_dir = os.path.join(_dir, "icons")
        if os.path.isdir(_icon_dir) is False:
            os.makedirs(_icon_dir, exist_ok=True)


    @property
    @abstractmethod
    def json_data_path(self):
        pass

    @abstractmethod
    def to_json(self):
        pass