from aiohttp.test_utils import unittest_run_loop

from tests.test_base import TestBaseHandler


class TestDatabaseHandler(TestBaseHandler):
    @unittest_run_loop
    async def test_rub_to_usd(self):
        """
        Тест конвертации валют RUR -> USD.
        """
        resp = await self.client.post(path='/database?merge=1',  json={
            'USD': 62.90,
            'EUR': 69.92,
        })
        await resp.read()
        self.assertEqual(resp.status, 200, await resp.text())

        resp = await self.client.get(path='/convert?from=RUR&to=USD&amount=42.0')
        currencies = await resp.json()

        self.assertEqual(resp.status, 200, await resp.text())
        self.assertDictEqual(currencies, {'result': 0.67})

    @unittest_run_loop
    async def test_usd_to_eur(self):
        """
        Тест конвертации валют USD -> EUR.
        """
        resp = await self.client.post(path='/database?merge=1',  json={
            'USD': 62.90,
            'EUR': 69.92,
        })
        await resp.read()
        self.assertEqual(resp.status, 200, await resp.text())

        resp = await self.client.get(path='/convert?from=USD&to=EUR&amount=42.0')
        currencies = await resp.json()

        self.assertEqual(resp.status, 200, await resp.text())
        self.assertDictEqual(currencies, {'result': 37.78})
