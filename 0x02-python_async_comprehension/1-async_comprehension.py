#!/usr/bin/env python3
""" Import async_generator from the previous task and then write a
coroutine called async_comprehension that takes no arguments

"""
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """each time asynchronously wait 1 second,
    then yield a random number between 0 and 10

    """
    for i in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10


async def async_comprehension():
    """ return the 10 random numbers."""
    rand_nos = [number async for number in async_generator()]
    return rand_nos
