import requests
from bs4 import BeautifulSoup

class E3372:
    def __init__(self, ip: str):
        self.ip = ip
        self.headers = {}
        pass

    def auth(self):
        pass

    def _request(self, endpoint: str, method='GET'):
        url = f"http://{self.ip}/api/webserver/SesTokInfo"
        r = requests.get(url) if method == 'GET' else requests.post(url)
        soup = BeautifulSoup(r.text, "lxml")
        print(soup)