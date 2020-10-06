import logging
import sys

from server import server


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    server.run_server()


if __name__ == '__main__':
    main()
