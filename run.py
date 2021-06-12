import argparse
import os
import pathlib

from app.infra.wsgi import create_wsgi_app, load_configuration

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-H', '--host', default='0.0.0.0')
parser.add_argument(
    '-p', '--port', type=int,
    default=int(os.environ.get('PORT', 8080)),
    help='port number to listen',
)
parser.add_argument('-d', '--debug', action='store_true', default=False)
parser.add_argument('config', type=pathlib.Path)


def main():
    args = parser.parse_args()
    if not args.config.is_file():
        parser.error(f'file not found: {args.config}')
    wsgi_app = create_wsgi_app(load_configuration(args.config))
    wsgi_app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
