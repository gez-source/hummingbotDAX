#!/usr/bin/env python
import aiohttp
from os.path import (
    join,
    realpath
)
import sys; sys.path.insert(0, realpath(join(__file__, "../../../../../")))

import asyncio
import logging
import unittest
from typing import List

from hummingbot.connector.exchange.openware.openware_api_order_book_data_source import (
    OpenwareAPIOrderBookDataSource,
)


class OpenwareAPIOrderBookDataSourceUnitTest(unittest.TestCase):
    trading_pairs: List[str] = [
        "ethusd",
    ]

    @classmethod
    def setUpClass(cls):
        cls.ev_loop: asyncio.BaseEventLoop = asyncio.get_event_loop()
        cls.data_source: OpenwareAPIOrderBookDataSource = OpenwareAPIOrderBookDataSource(
            trading_pairs=cls.trading_pairs,
            openware_api_url = "https://www.quantaexchange.org/api/v2/peatio",
            openware_ranger_url = "wss://www.quantaexchange.org/api/v2/ranger"
        )

    def test_get_trading_pairs(self):
        result: List[str] = self.ev_loop.run_until_complete(
            self.data_source.get_trading_pairs())

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], str)
        self.assertEqual(result[0], "ethusd")

    def test_size_snapshot(self):
        async def run_session_for_fetch_snaphot():
            async with aiohttp.ClientSession() as client:
                result = await self.data_source.get_snapshot(client, "ethusd")
                assert len(result["bids"]) == self.data_source.SNAPSHOT_LIMIT_SIZE
                assert len(result["asks"]) == self.data_source.SNAPSHOT_LIMIT_SIZE

                # 25 is default fetch value, that is very small for use in production
                assert len(result["bids"]) > 25
                assert len(result["asks"]) > 25

        self.ev_loop.run_until_complete(run_session_for_fetch_snaphot())


def main():
    logging.basicConfig(level=logging.INFO)
    unittest.main()


if __name__ == "__main__":
    main()
