import requests
from urllib.parse import urlencode
from typing import Optional

from hackdb.exceptions import _get_exception, HackDBOriginException


class HackDB:
    def __init__(self, site_key: str, origin: str, endpoint: str = "https://app.hackingtons.com/api/v1") -> None:
        """
        Initialize a HackDB instance
        :param site_key: the site key
        :param origin: the website's origin
        :param endpoint: optional endpoint override; you don't need to change this
        """
        self.endpoint: str = endpoint
        """HackDB API endpoint"""
        self.session: Optional[dict] = None
        """The session if the user is logged in"""
        self.headers: dict[str, str] = {
            "Authorization": f"Bearer {site_key}",
            "Content-Type": "application/json",
            "Origin": origin,
        }
        """Headers to send with every request"""

    def login(self, username: str, password: str) -> None:
        """
        Log into a website with a username and password
        :param username: your user's username
        :param password: your user's password
        """
        resp = requests.post(f"{self.endpoint}/site/login", json={
            "username": username,
            "password": password
        }, headers=self.headers).json()

        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        self.session = resp
        self.headers["X-Site-Session"] = resp["session"]

    def signup(self, username: str, password: str) -> None:
        """
        Sign up for a website
        :param username: your user's username
        :param password: your user's password
        """
        resp = requests.post(f"{self.endpoint}/site/signup", json={
            "username": username,
            "password": password
        }, headers=self.headers).json()

        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])

    def logout(self) -> None:
        """
        Logs out of a website and forgets the session
        """
        if not self.session:
            return

        resp = requests.post(f"{self.endpoint}/site/logout", headers=self.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        self.headers.pop("X-Site-Session")
        self.session = None

    def me(self) -> dict:
        """
        Gets data about the current user
        :return: data about the current user
        """
        resp = requests.get(f"{self.endpoint}/site/me", headers=self.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        self.session["username"] = resp["username"]
        self.session["status"] = resp["status"]
        return resp

    def get_collection(self, collection: str) -> Collection:
        """
        Initializes a Collection object
        :param collection: collection name
        :return: the collection
        """
        return Collection(collection, self)


class Collection:
    def __init__(self, collection: str, db: HackDB) -> None:
        """
        Initializes a Collection object
        :param collection: collection name
        :param db: the HackDB instance
        """
        self.collection: str = collection
        """collection name"""
        self.db: HackDB = db
        """HackDB instance"""

    def list(self, limit: int = 50, sort: Optional[str] = None, order: Optional[str] = None) -> dict:
        """
        Gets the data from a bunch of documents
        :param limit: the maximum number of documents to return, defaults to 50, max is 200
        :param sort: the field to sort by
        :param order: the order to sort by, either "asc" or "desc"
        :return: documents
        """
        options: dict[str, int | str] = {"limit": limit}
        if sort: options["sort"] = sort
        if order: options["order"] = order

        params = urlencode(options)
        resp = requests.get(f"{self.db.endpoint}/data/{self.collection}?{params}", headers=self.db.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        return resp

    def get(self, document_id: str) -> dict:
        """
        Gets a single document by id
        :param document_id: id of the document
        :return: document
        """
        resp = requests.get(f"{self.db.endpoint}/data/{self.collection}/{document_id}", headers=self.db.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        return resp["document"]

    def insert(self, data) -> dict:
        """
        Inserts a document
        :param data: document content
        :return: document
        """
        resp = requests.post(f"{self.db.endpoint}/data/{self.collection}", json=data, headers=self.db.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        return resp["document"]

    def update(self, document_id: str, data) -> dict:
        """
        Updates the contents of a document
        :param document_id: id of the document
        :param data: document content
        :return: document
        """
        resp = requests.put(f"{self.db.endpoint}/data/{self.collection}/{document_id}", json=data, headers=self.db.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])
        return resp["document"]

    def delete(self, document_id: str) -> dict:
        """
        Deletes a document
        :param document_id: id of the document
        """
        resp = requests.delete(f"{self.db.endpoint}/data/{self.collection}/{document_id}", headers=self.db.headers).json()
        if "error" in resp:
            raise _get_exception(resp["error"]["code"])(resp["error"]["message"])

