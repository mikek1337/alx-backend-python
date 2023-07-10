#!/usr/bin/env python3
"""execute multiple coroutines at the same time with async"""


from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """Wait for a random delay between 0 and max_delay"""
    delay_list: List[float] = []
    for i in range(n):
        delay_list.append(await wait_random(max_delay))
    return sorted(delay_list)
