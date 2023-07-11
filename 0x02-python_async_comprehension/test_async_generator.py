import asyncio
import unittest
from typing import AsyncGenerator
from unittest.mock import patch, MagicMock

async_generator = __import__('0-async_generator').async_generator


class TestAsyncGenerator(unittest.TestCase):
    """Test suite for async_generator function"""

    @patch('asyncio.sleep', new_callable=MagicMock)
    async def test_async_generator(self, mock_sleep: MagicMock) -> None:
        """Test async_generator function"""
        mock_sleep.return_value = asyncio.sleep(0)
        async with async_generator() as agen:
            res = [i async for i in agen]
        self.assertEqual(len(res), 10)
        self.assertTrue(all(isinstance(i, float) for i in res))
        self.assertTrue(all(0 <= i <= 10 for i in res))