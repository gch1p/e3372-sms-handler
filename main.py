from argparse import ArgumentParser
from pprint import pprint
from e3372 import E3372


def main():
    parser = ArgumentParser()
    parser.add_argument('--ip',
                        default='192.168.8.1',
                        help='Modem IP address')
    args = parser.parse_args()

    client = E3372(args.ip)
    client.auth()

    messages = client.get_sms()

    for m in messages:
        print(f"phone: {m.phone}")
        print(f"ts: {m.timestamp()}")
        print(f"content: {m.content}")
        print('-----')


if __name__ == '__main__':
    main()
