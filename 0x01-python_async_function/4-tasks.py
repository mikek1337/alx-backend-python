#!/usr/bin/env python3
"""execute multiple coroutines at the same time with async"""


from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """Wait for a random delay between 0 and max_delay"""
    delay_list: List[float] = []
    for i in range(n):
        delay_list.append(await task_wait_random(max_delay))
    return sorted(delay_list)