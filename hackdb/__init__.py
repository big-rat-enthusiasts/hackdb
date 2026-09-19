from hackdb.exceptions import _get_exception
import requests


class HackDB:
    def __init__(self, site_key: str, origin: str, endpoint: str = "https://app.hackingtons.com/api/v1"):
        self._site_key = site_key
        self._endpoint = endpoint
        self._origin = origin
        self.session = None
        self.headers = {
            "Authorization": f"Bearer {site_key}",
            "Content-Type": "application/json",
            "Origin": origin,
        }

    def login(self, username: str, password: str):
        resp = requests.post(f"{self._endpoint}/site/login", json={
            "username": username,
            "password": password
        }, headers=self.headers).json()

        print(resp, flush=True)
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        self.session = resp
        self.headers["X-Site-Session"] = resp["session"]


