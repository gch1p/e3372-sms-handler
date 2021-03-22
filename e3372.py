import requests
from bs4 import BeautifulSoup

class E3372:
    def __init__(self, ip: str):
        self.ip = ip
        self.headers = {}
        pass

    def auth(self):
        response = self.request("webserver/SesTokInfo")

        cookie = response.find('SesInfo').get_text()
        token = response.find('TokInfo').get_text()

        self.headers['Cookie'] = cookie
        self.headers['__RequestVerificationToken'] = token
        self.headers['Content-Type'] = 'text/xml'

    def device_information(self):
        response = self.request('device/information')
        print(response)

    def device_signal(self):
        response = self.request('device/signal')
        print(response)

    def request(self, endpoint: str, method='GET'):
        url = f'http://{self.ip}/api/{endpoint}'
        r = requests.get(url) if method == 'GET' else requests.post(url)
        return BeautifulSoup(r.text, 'xml').find('response')