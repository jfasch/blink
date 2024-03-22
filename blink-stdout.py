#!/usr/bin/env python

from blink import blink
import asyncio


class IOStdout:
    def __init__(self, nums):
        self.nums = nums
    def set(self, value):
        for n in self.nums:
            print(f'{n}: {value}')
    def iter(self):
        for n in self.nums:
            yield IOStdout([n])

program = blink.blink(IOStdout((1, 2, 3)), 0.2)
#program = blink.on(IOStdout((1, 2, 3)))

asyncio.run(program())
