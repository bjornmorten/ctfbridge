from abc import ABC, abstractmethod

import requests
from requests import Response


class PlatformMatcher(ABC):
    name: str

    @abstractmethod
    def matches(self, response: Response) -> bool:
        pass

    @abstractmethod
    def is_base_url(self, url: str) -> bool:
        pass

class CTFdMatcher(PlatformMatcher):
    name = "CTFd"

    def matches(self, response: Response) -> bool:
        return "Powered by CTFd" in response.text

    def is_base_url(self, url: str) -> bool:
        resp = requests.get(f'{url}/api/v1/swagger.json')
        return resp.status_code == 200

class RCTFMatcher(PlatformMatcher):
    name = "rCTF"

    def matches(self, response: Response) -> bool:
        return "rctf-config" in response.text

    def is_base_url(self, url: str) -> bool:
        resp = requests.get(f'{url}/api/v1/users/me')
        return "badToken" in resp.text

PLATFORM_MATCHERS = [
    CTFdMatcher(),
    RCTFMatcher()
]

