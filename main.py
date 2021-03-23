import pathlib
import os

from argparse import ArgumentParser
from e3372 import WebAPI, SMSHandler, SMS


config_dir = os.path.join(pathlib.Path.home(), '.e3372-sms-handler')
trusted_phone = ''


def sms_handler(sms: SMS, api: WebAPI):
    global trusted_phone

    # print(f'from: {sms.phone}')
    # print(f'text: {sms.text}')

    if sms.phone == trusted_phone:
        text = sms.text.lower().strip()
        if text == 'you shall reboot!':
            api.reboot()

        elif text == 'yo, get me some status':
            info = api.device_information()
            signal = api.device_signal()
            buf = []

            for key, value in info.items():
                if key in ('workmode', 'WanIPAddress'):
                    buf.append(f'{key}={value}')

            for key, value in signal.items():
                if key in ('cell_id', 'rssi', 'rscp', 'ecio', 'mode'):
                    buf.append(f'{key}={value}')

            buf = ' '.join(buf)
            if buf != '':
                api.send_sms(phone=trusted_phone, content=buf)

        elif text == 'switch it off':
            api.dataswitch(False)

        elif text == 'switch it on':
            api.dataswitch(True)


def main():
    global trusted_phone

    # parse arguments
    parser = ArgumentParser()
    parser.add_argument('--ip',
                        default='192.168.8.1',
                        help='Modem IP address')
    parser.add_argument('--trusted-phone',
                        help='Trusted phone number')
    args = parser.parse_args()

    # set global trusted_phone
    trusted_phone = args.trusted_phone

    # webapi client
    client = WebAPI(args.ip)
    client.auth()

    # sms handler
    smshandler = SMSHandler(api=client, config_dir=config_dir)
    smshandler.process(sms_handler)


if __name__ == '__main__':
    main()
