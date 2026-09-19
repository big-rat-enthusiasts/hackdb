import requests
from urllib.parse import urlencode
from typing import Optional

from hackdb.exceptions import _get_exception, HackDBOriginException


class HackDB:
    def __init__(self, site_key: str, origin: str, endpoint: str = "https://app.hackingtons.com/api/v1"):
        self.site_key = site_key
        self.endpoint = endpoint
        self.origin = origin
        self.session = None
        self.headers = {
            "Authorization": f"Bearer {site_key}",
            "Content-Type": "application/json",
            "Origin": origin,
        }

    def login(self, username: str, password: str):
        resp = requests.post(f"{self.endpoint}/site/login", json={
            "username": username,
            "password": password
        }, headers=self.headers).json()

        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        self.session = resp
        self.headers["X-Site-Session"] = resp["session"]

    def signup(self, username: str, password: str):
        resp = requests.post(f"{self.endpoint}/site/signup", json={
            "username": username,
            "password": password
        }, headers=self.headers).json()

        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])

    def logout(self):
        if not self.session:
            return

        resp = requests.post(f"{self.endpoint}/site/logout", headers=self.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        self.headers.pop("X-Site-Session")
        self.session = None

    def me(self):
        resp = requests.get(f"{self.endpoint}/site/me", headers=self.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        self.session["username"] = resp["username"]
        self.session["status"] = resp["status"]
        return resp

    def get_collection(self, collection: str):
        return Collection(collection, self)


class Collection:
    def __init__(self, collection: str, db: HackDB):
        self.collection = collection
        self.db = db

    def list(self, limit: int = 50, sort: Optional[str] = None, order: Optional[str] = None):
        options: dict[str, int | str] = {"limit": limit}
        if sort: options["sort"] = sort
        if order: options["order"] = order

        params = urlencode(options)
        resp = requests.get(f"{self.db.endpoint}/data/{self.collection}?{params}", headers=self.db.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        return resp

    def get(self, document_id: str):
        resp = requests.get(f"{self.db.endpoint}/data/{self.collection}/{document_id}", headers=self.db.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        return resp["document"]

    def insert(self, data):
        resp = requests.post(f"{self.db.endpoint}/data/{self.collection}", json=data, headers=self.db.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])

    def update(self, document_id: str, data):
        resp = requests.put(f"{self.db.endpoint}/data/{self.collection}/{document_id}", json=data, headers=self.db.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        return resp["document"]

    def delete(self, document_id: str):
        resp = requests.delete(f"{self.db.endpoint}/data/{self.collection}/{document_id}", headers=self.db.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])

