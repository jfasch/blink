#!/usr/bin/env python

from stuff.gpios import MATRIX
from stuff.program_dumb import blink, cycle, cycle_multiple, loop

import numpy
import asyncio
import random
import sys
import os


# async def main():
#     cols = numpy.transpose(numpy.array(MATRIX)).tolist()

#     # tasks = []
#     # for col in cols:
#     #     tasks.append(asyncio.create_task(cycle(col, random.uniform(0.2, 0.8))))

#     # for t in tasks:
#     #     await t

#     await cycle_multiple(cols, 0.2, 0.8)


async def main():
    coros = [
        blink(MATRIX[0], 0.1, 5),
        blink(MATRIX[1], 0.2, 4),
        blink(MATRIX[2], 0.3, 3),
        blink(MATRIX[3], 0.4, 2),
        blink(MATRIX[4], 0.5, 1),
    ]
    await loop(coros, 3)

asyncio.run(main())
