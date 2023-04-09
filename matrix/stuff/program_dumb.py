from .gpios import REQUEST

from gpiod.line import Value
import asyncio
import random
import itertools


async def blink(ios, interval, ntimes):
    for _ in range(ntimes):
        REQUEST().set_values({i: Value(1) for i in ios})
        await asyncio.sleep(interval)
        REQUEST().set_values({i: Value(0) for i in ios})
        await asyncio.sleep(interval)

async def cycle(ios, interval):
    for i in itertools.cycle(ios):
        REQUEST().set_value(i, Value(1))
        await asyncio.sleep(interval)
        REQUEST().set_value(i, Value(0))

async def cycle_multiple(mult_ios, low_interval, high_interval):
    for ios in mult_ios:
        tasks = [asyncio.create_task(cycle(ios, random.uniform(low_interval, high_interval)))]
    for t in tasks:
        await t

async def loop(coros, n):
    for _ in range(n):
        for coro in coros:
            await coro

        
