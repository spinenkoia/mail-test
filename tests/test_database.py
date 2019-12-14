from aiohttp.test_utils import unittest_run_loop

from tests.test_base import TestBaseHandler


class TestDatabaseHandler(TestBaseHandler):
    @unittest_run_loop
    async def test_replace(self):
        """
        Тест перезаписи валют.
        """
        resp = await self.client.post(path='/database?merge=1',  json={
            'USD': 62.90,
            'EUR': 69.92,
        })
        await resp.read()

        self.assertEqual(resp.status, 200, await resp.text())

        resp = await self.client.get(path='/database')
        currencies = await resp.json()

        self.assertEqual(resp.status, 200, await resp.text())
        self.assertDictEqual(currencies, {'EUR': 69.92, 'USD': 62.9})

    @unittest_run_loop
    async def test_update(self):
        """
        Тест обновления валют.
        """
        resp = await self.client.post(path='/database?merge=1',  json={
            'USD': 62.90,
            'EUR': 69.92,
        })
        await resp.read()
        self.assertEqual(resp.status, 200, await resp.text())

        resp = await self.client.get(path='/database')
        currencies = await resp.json()
        self.assertEqual(resp.status, 200, await resp.text())
        self.assertDictEqual(currencies, {'EUR': 69.92, 'USD': 62.9})

        resp = await self.client.post(path='/database?merge=0',  json={
            'USD': 62.90,
        })
        await resp.read()

        self.assertEqual(resp.status, 200, await resp.text())

        resp = await self.client.get(path='/database')
        currencies = await resp.json()
        self.assertEqual(resp.status, 200, await resp.text())
        self.assertDictEqual(currencies, {'EUR': 69.92, 'USD': 62.9})
