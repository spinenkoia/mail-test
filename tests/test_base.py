from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web import Application

from backend.main import handlers
from backend.currencies import Currencies


class TestBaseHandler(AioHTTPTestCase):
    def setUp(self):
        super().setUp()
        self.app['currencies'].clean()

    def tearDown(self):
        self.app['currencies'].close()
        super().tearDown()

    async def get_application(self):
        app = Application()

        app.router.add_routes(handlers)
        app['currencies'] = Currencies()

        return app
