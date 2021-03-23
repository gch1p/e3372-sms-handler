import pathlib

from argparse import ArgumentParser
from pprint import pprint
from e3372 import WebAPI, SMSHandler, SMS


config_dir = pathlib.Path.home() + '/.e3372-sms-handler'


def sms_handler(sms: SMS):
    print(f'from: {sms.phone}')
    print(f'text: {sms.content}')


def main():
    parser = ArgumentParser()
    parser.add_argument('--ip',
                        default='192.168.8.1',
                        help='Modem IP address')
    parser.add_argument('--phone')
    parser.add_argument('--content')
    args = parser.parse_args()

    client = WebAPI(args.ip)
    client.auth()

    smshandler = SMSHandler(api=client, config_dir=config_dir)
    smshandler.process(sms_handler)

    # info = client.device_information()
    # signal = client.device_signal()

    result = client.send_sms(phone=args.phone,
                             content=args.content)
    print(result)
    print(type(result))

    # messages = client.get_sms()
    #
    # for m in messages:
    #     print(f"phone:   {m.phone}")
    #     print(f"date:    {m.date} ({m.timestamp()})")
    #     print(f"content: {m.content}")
    #     print('-----')


if __name__ == '__main__':
    main()
