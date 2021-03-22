import requests
import sys

from datetime import datetime
from bs4 import BeautifulSoup


def build_request(params: dict):
    items = []
    for key, value in params.items():
        items.append(f'<{key}>{value}</{key}>')
    return '<request>'+''.join(items)+'</request>'


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

    # def device_information(self):
    #     response = self.request('device/information')
    #     print(response)
    #
    # def device_signal(self):
    #     response = self.request('device/signal')
    #     print(response)

    def get_sms(self, count=10, page=1):
        request = build_request({
            'PageIndex': page,
            'ReadCount': count,
            'BoxType': 1,
            'SortType': 0,
            'Ascending': 0,
            'UnreadPreferred': 1
        })
        response = self.request('sms/sms-list', data=request)

        sms_list = []
        for message in response.find_all('Message'):
            sms = SMS(
                index=int(message.find('Index').get_text()),
                phone=message.find('Phone').get_text(),
                content=message.find('Content').get_text(),
                date=message.find('Date').get_text()
            )
            sms_list.append(sms)

        return sms_list


    def send_sms(self):
        pass

    def request(self, endpoint: str, data=None):
        url = f'http://{self.ip}/api/{endpoint}'
        r = requests.get(url) if data is None else requests.post(url, data=data)

        soup = BeautifulSoup(r.text, 'lxml-xml')

        error = soup.find('error')
        if error:
            code = 0
            message = ''

            code_node = error.find('code')
            message_node = error.find('message')

            if code_node:
                code = int(code_node.get_text())

            if message_node:
                message = message_node.get_text()

            raise E3372Error(code, message=message)

        return soup.find('response')



class SMS:
    def __init__(self, index=None, phone=None, content=None, date=None):
        self.index = index
        self.phone = phone
        self.content = content
        self.date = date

    def timestamp(self):
        # input example: 2020-08-11 14:55:51
        return int(datetime.strptime(self.date, '%Y-%m-%d %H-%M-%S').strftime("%s"))


class E3372Error(Exception):
    def __init__(self, error_code, message='', *args, **kwargs):
        self.error_code = error_code
        self.traceback = sys.exc_info()

        try:
            msg = '[{0}] {1}'.format(error_code, message.format(*args, **kwargs))
        except (IndexError, KeyError):
            msg = '[{0}] {1}'.format(error_code, message)

        super().__init__(msg)