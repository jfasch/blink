#!/usr/bin/env python

from stuff.gpios import MATRIX
from stuff.program_oo import BlinkFactory, CycleFactory, SequenceFactory, LoopFactory

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
    rows = MATRIX
    cols = numpy.transpose(MATRIX).tolist()

    loop = LoopFactory(
        SequenceFactory([
            BlinkFactory(rows[0], 0.05, 2),
            BlinkFactory(rows[1], 0.10, 2),
            BlinkFactory(rows[2], 0.15, 2),
            BlinkFactory(rows[3], 0.20, 2),
            BlinkFactory(rows[4], 0.25, 2),

            CycleFactory(cols[0], 0.05, 2),
            CycleFactory(cols[1], 0.05, 2),
            CycleFactory(cols[2], 0.05, 2),
            CycleFactory(cols[3], 0.05, 2),
            CycleFactory(cols[4], 0.05, 2),
        ]),
        300
    )
    coro = loop.create_coro()
    await coro

asyncio.run(main())
