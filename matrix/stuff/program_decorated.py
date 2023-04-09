from .gpios import REQUEST

from gpiod.line import Value
import asyncio
import random
import itertools


def program(corofunc):
    def factory(*args, **kwargs):
        def create_coro():
            return corofunc(*args, **kwargs)
        return create_coro
    return factory

@program
async def blink(ios, interval, ntimes):
    for _ in range(ntimes):
        REQUEST().set_values({i: Value(1) for i in ios})
        await asyncio.sleep(interval)
        REQUEST().set_values({i: Value(0) for i in ios})
        await asyncio.sleep(interval)

@program
async def cycle(ios, interval, ntimes):
    for _ in range(ntimes):
        for i in ios:
            REQUEST().set_value(i, Value(1))
            await asyncio.sleep(interval)
            REQUEST().set_value(i, Value(0))

@program
async def sequence(progs):
    for p in progs:
        c = p()
        await c

@program
async def loop(prog, ntimes):
    for _ in range(ntimes):
        coro = prog()
        await coro
