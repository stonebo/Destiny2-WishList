import os
import logging
import json as jsonlib
import urllib.parse
from requests import Session
from requests.auth import AuthBase
from .entity_type import EntityType

__url_cache__ = {}
logger = logging.getLogger()


class TokenAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token[:4]}"

    def __call__(self, request):
        request.headers["X-API-Key"] = self.token


class Destiny2Session(Session):
    Baseurl = "https://bungie.net/Platform"

    def __init__(self):
        self.auth = TokenAuth(os.environ["TOKEN"])

    def build_url(self, *args, **kwargs):
        parts = [kwargs.get("base_url") or self.base_url]
        parts.extend(args)
        parts = [str(p) for p in parts]
        key = tuple(parts)
        logger.info("Building a url from %s", key)
        if key not in __url_cache__:
            logger.info("Missed the cache building the url")
            __url_cache__[key] = "/".join(parts)
        return __url_cache__[key]

    def build_destiny2_url(self, *args, **kwargs):
        base_url = urllib.parse.urljoin(self.Baseurl, "Destiny2")
        kwargs.update({"base_url": base_url})
        return self.build_url(*args, **kwargs)


class Destiny2API:
    def __init__(self):
        self.session = Destiny2Session()

    def _request(self, method, *args, **kwargs):
        request_method = getattr(self.session, method)
        return request_method(*args, **kwargs)

    def _delete(self, url, **kwargs):
        logger.debug("DELETE %s with %s", url, kwargs)
        return self._request("delete", url, **kwargs)

    def _get(self, url, **kwargs):
        logger.debug("GET %s with %s", url, kwargs)
        return self._request("get", url, **kwargs)

    def _patch(self, url, **kwargs):
        logger.debug("PATCH %s with %s", url, kwargs)
        return self._request("patch", url, **kwargs)

    def _post(self, url, data=None, json=True, **kwargs):
        if json:
            data = jsonlib.dumps(data) if data is not None else data
        logger.debug("POST %s with %s, %s", url, data, kwargs)
        return self._request("post", url, data, **kwargs)

    def _put(self, url, **kwargs):
        logger.debug("PUT %s with %s", url, kwargs)
        return self._request("put", url, **kwargs)

    def get_entity_definition(self, entity_type: EntityType, hash_id: str):
        _url = self.session.build_destiny2_url("Manifest", entity_type.value, hash_id)
        return self._get(_url)


if __name__ == '__main__':
    print(1)
