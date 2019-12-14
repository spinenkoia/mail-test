import logging
import redis

from argparse import ArgumentParser

from aiohttp.web import Application, run_app, view

from backend.handlers.convert import ConvertHandler
from backend.handlers.database import DatabaseHandler
from backend.currencies import Currencies

log = logging.getLogger(__name__)

handlers = [
    view('/convert', ConvertHandler),
    view('/database', DatabaseHandler),
]


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Enable debug mode.')

    return parser.parse_args()

def add_stderr_handler(debug: bool):
    handler = logging.StreamHandler()
    logging.raiseExceptions = False
    logging.captureWarnings(True)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)
    logging.getLogger('asyncio').setLevel(logging.ERROR)
    logging.getLogger('aiohttp').setLevel(logging.ERROR)


def main():
    cmd_args = parse_args()

    add_stderr_handler(cmd_args.debug)

    application = Application()
    application.router.add_routes(handlers)

    async def on_startup(app: Application):
        app['currencies'] = Currencies(redis.Redis)

    async def on_cleanup(app: Application):
        app['currencies'].close()

    application.on_startup.append(on_startup)
    application.on_cleanup.append(on_cleanup)

    log.info('Run backend.')

    run_app(application, host='0.0.0.0', port=8080)

    log.info('Shutdown.')


if __name__ == '__main__':
    main()
