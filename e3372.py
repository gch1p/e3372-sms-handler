import requests
import sys
import os
import json
import traceback

from typing import Callable
from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import Tag


def build_request(params: dict, depth=1):
    if depth == 1:
        return build_request({
            'request': params
        }, depth=depth + 1)

    items = []
    for key, value in params.items():
        if isinstance(value, dict):
            value = build_request(value, depth=depth + 1)
        items.append(f'<{key}>{value}</{key}>')
    return ''.join(items)


def xml2dict(node):
    data = {}

    for c in node.children:
        if isinstance(c, Tag):
            data[c.name] = c.get_text()

    return data


class WebAPI:
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
        return xml2dict(self.request('device/information'))

    def device_signal(self):
        return xml2dict(self.request('device/signal'))

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
                text=message.find('Content').get_text(),
                date=message.find('Date').get_text()
            )
            sms_list.append(sms)

        return sms_list

    def send_sms(self, phone: str, content: str):
        return self.request('sms/send-sms', build_request({
            'Index': -1,
            'Phones': {
                'Phone': phone,
            },
            'Sca': '',
            'Content': content,
            'Length': len(content),
            'Reserved': 1,
            'Date': -1
        })).get_text() == 'OK'

    def dataswitch(self, on=True):
        return self.request('dialup/mobile-dataswitch', data=build_request({
            'dataswitch': 1 if on else 0
        }))

    def reboot(self):
        return self.request('device/control', data=build_request({
            'Control': 1
        }))

    def request(self, endpoint: str, data=None):
        url = f'http://{self.ip}/api/{endpoint}'
        r = requests.get(url, headers=self.headers) if data is None else requests.post(url, data=data,
                                                                                       headers=self.headers)
        r.encoding = 'utf-8'

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

            raise WebAPIError(code, message=message)

        return soup.find('response')


class SMSHandler:
    def __init__(self, api: WebAPI, config_dir: str):
        self.api = api

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        self.config_dir = config_dir
        self.state_file = os.path.join(config_dir, 'state.dat')

    def read_state(self):
        if not os.path.exists(self.state_file):
            default_state = {
                'last_timestamp': 0
            }
            self.write_state(default_state)
            return default_state

        with open(self.state_file, 'r') as f:
            return json.loads(f.read())

    def write_state(self, state: dict):
        with open(self.state_file, 'w') as f:
            f.write(json.dumps(state))

    def process(self, handler: Callable):
        state = self.read_state()
        max_ts = state['last_timestamp']

        # loop backwards
        messages = self.api.get_sms(10, 1)
        for sms in reversed(messages):
            ts = sms.timestamp()
            if state['last_timestamp'] >= ts:
                continue

            if ts > max_ts:
                max_ts = ts

            try:
                handler(sms, self.api)
            except:
                traceback.print_exc()
                continue

        if max_ts != state['last_timestamp']:
            state['last_timestamp'] = max_ts
            self.write_state(state)


class SMS:
    def __init__(self, index=None, phone=None, text=None, date=None):
        self.index = index
        self.phone = phone
        self.text = text
        self.date = date

    def timestamp(self):
        # input example: 2020-08-11 14:55:51
        return int(datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S').strftime("%s"))


class WebAPIError(Exception):
    def __init__(self, error_code, message='', *args, **kwargs):
        self.error_code = error_code
        self.traceback = sys.exc_info()

        try:
            msg = '[{0}] {1}'.format(error_code, message.format(*args, **kwargs))
        except (IndexError, KeyError):
            msg = '[{0}] {1}'.format(error_code, message)

        super().__init__(msg)
