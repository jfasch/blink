from .gpios import REQUEST

from gpiod.line import Value
import asyncio
import random
import itertools


def blink(ios, interval, ntimes):
    def create_coro():
        async def coro():
            for _ in range(ntimes):
                REQUEST().set_values({i: Value(1) for i in ios})
                await asyncio.sleep(interval)
                REQUEST().set_values({i: Value(0) for i in ios})
                await asyncio.sleep(interval)

        return coro()
    return create_coro

def cycle(ios, interval, ntimes):
    def create_coro():
        async def coro():
            for _ in range(ntimes):
                for i in ios:
                    REQUEST().set_value(i, Value(1))
                    await asyncio.sleep(interval)
                    REQUEST().set_value(i, Value(0))

        return coro()
    return create_coro

def sequence(progs):
    def create_coro():
        async def coro():
            for p in progs:
                c = p()
                await c
        return coro()
    return create_coro

def loop(prog, ntimes):
    def create_coro():
        async def coro():
            for _ in range(ntimes):
                coro = prog()
                await coro

        return coro()
    return create_coro

