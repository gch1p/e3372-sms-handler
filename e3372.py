import requests
from bs4 import BeautifulSoup

class E3372:
    def __init__(self, ip: str):
        self.ip = ip
        self.headers = {}
        pass

    def auth(self):
        soup = self._request("webserver/SesTokInfo")
        print(soup)

    def _request(self, endpoint: str, method='GET'):
        url = f"http://{self.ip}/api/{endpoint}"
        r = requests.get(url) if method == 'GET' else requests.post(url)
        return BeautifulSoup(r.text, "lxml")