#!/usr/bin/env python

from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value

from stuff.gpios import MATRIX

import asyncio
import itertools
import random
import sys
import os


CHIP = '/dev/gpiochip0'
CONSUMER = os.path.basename(sys.argv[0])

linear_matrix = tuple(itertools.chain(*MATRIX))

request = request_lines(
    CHIP, 
    consumer=CONSUMER, 
    config={linear_matrix: LineSettings(direction=Direction.OUTPUT)})

async def blink(ios, interval, ntimes):
    for _ in range(ntimes):
        request.set_values({i: Value(1) for i in ios})
        await asyncio.sleep(interval)
        request.set_values({i: Value(0) for i in ios})
        await asyncio.sleep(interval)

async def cycle(ios, interval):
    for i in itertools.cycle(ios):
        request.set_value(i, Value(1))
        await asyncio.sleep(interval)
        request.set_value(i, Value(0))

#fut = asyncio.ensure_future(blink(MATRIX[0], 0.2))

# coro = blink(MATRIX[0], 0.2)
# print(type(coro))

# fut = asyncio.ensure_future(blink(MATRIX[0], 0.2))
# print(type(fut))

# async def main():
#     tasks = []
#     for n,row in enumerate(MATRIX):
#         tasks.append(asyncio.create_task(blink(row, 0.1, 3)))
#     for t in tasks:
#         await t

async def main():
    tasks = []
    for n,row in enumerate(MATRIX):
        await asyncio.sleep(0.2)
        tasks.append(asyncio.create_task(cycle(row, random.uniform(0.1, 0.5))))
    for t in tasks:
        await t

asyncio.run(main())
