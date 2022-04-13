from abc import ABC, abstractmethod
import os
import logging
import json as jsonlib
import urllib.parse
import requests
from typing import List
from ..destiny2_api import Destiny2API
from ..utils import cache_dir

logger = logging.getLogger()


class Destiny2Inventory(ABC):
    Baseurl = "https://bungie.net"

    def __init__(self, hash_id: str, profile: str = "default"):
        self.profile = profile
        self.resp = self._get_resp_from_bungie(hash_id)

    def _get_resp_from_bungie(self, hash_id: str, refresh: bool = False):
        cache_file = os.path.join(cache_dir(), f"{hash_id}.json")
        if refresh is False:
            resp = self._resp_cache(cache_file)
        else:
            resp = None
        if resp is None:
            logger.info(f"Item {hash_id} cache not exist, start get from Bungie API")
            _api = Destiny2API()
            resp = _api.get_inventory_item_definition(hash_id)
            with open(cache_file, "w+") as fp:
                jsonlib.dump(resp, fp, indent=4)
            logger.info(f"Store item {hash_id}'s cache to cache file: {cache_file}")
        return resp

    def _resp_cache(self, cache_file: str):
        if os.path.exists(cache_file):
            with open(cache_file, "r") as fp:
                resp = jsonlib.load(fp)
        else:
            resp = None
        return resp

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
        for icon in self.icon_list:
            self._download_icons(icon[0], icon[1])

    def _build_icon_link(self, link_path: str):
        return str(urllib.parse.urljoin(self.Baseurl, link_path))

    def _download_icons(self, icon_name: str, icon_url: str, refresh: bool = False):
        _dir = os.path.dirname(self.json_data_path)
        _icon_dir = os.path.join(_dir, "icons")
        _icon_image = os.path.join(_icon_dir, f"{icon_name}.jpg")
        if os.path.isdir(_icon_dir) is False:
            logger.info(f"Create Icon Dir: {_icon_dir}")
            os.makedirs(_icon_dir, exist_ok=True)
        if os.path.isfile(_icon_image) and refresh is False:
            logger.info(f"{icon_name} Icon File Exist, Skip Download")
        else:
            image = requests.get(icon_url, stream=True).content
            with open(_icon_image, "wb") as fp:
                fp.write(image)
            logger.info(f"{icon_name} icon download to {_icon_image}")

    @property
    @abstractmethod
    def json_data_path(self):
        pass

    @property
    @abstractmethod
    def icon_list(self) -> List[tuple]:
        """
        [
            (<icon name>, <icon url>),
        ]
        """
        pass

    @abstractmethod
    def to_json(self):
        pass