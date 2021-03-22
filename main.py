from argparse import ArgumentParser
from pprint import pprint
from e3372 import E3372

def main():
    client = E3372('192.168.8.1')
    client.auth()
    pprint(client.headers)

if __name__ == '__main__':
    main()
