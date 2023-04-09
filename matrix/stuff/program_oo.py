from .gpios import REQUEST

from gpiod.line import Value
import asyncio
import random
import itertools


class BlinkFactory:
    def __init__(self, ios, interval, ntimes):
        self.ios = ios
        self.interval = interval
        self.ntimes = ntimes

    def create_coro(self):
        async def coro():
            for _ in range(self.ntimes):
                REQUEST().set_values({i: Value(1) for i in self.ios})
                await asyncio.sleep(self.interval)
                REQUEST().set_values({i: Value(0) for i in self.ios})
                await asyncio.sleep(self.interval)

        return coro()


class CycleFactory:
    def __init__(self, ios, interval, ntimes):
        self.ios = ios
        self.interval = interval
        self.ntimes = ntimes

    def create_coro(self):
        async def coro():
            for _ in range(self.ntimes):
                for i in self.ios:
                    REQUEST().set_value(i, Value(1))
                    await asyncio.sleep(self.interval)
                    REQUEST().set_value(i, Value(0))

        return coro()

class SequenceFactory:
    def __init__(self, factories):
        self.factories = factories
        
    def create_coro(self):
        async def coro():
            for f in self.factories:
                c = f.create_coro()
                await c
        return coro()

class LoopFactory:
    def __init__(self, factory, ntimes):
        self.factory = factory
        self.ntimes = ntimes

    def create_coro(self):
        async def coro():
            for _ in range(self.ntimes):
                coro = self.factory.create_coro()
                await coro

        return coro()
        
