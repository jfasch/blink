#!/usr/bin/env python

from stuff.gpios import MATRIX
from stuff.program_decorated import blink, cycle, sequence, loop

import numpy
import asyncio
import random
import sys
import os


async def main():
    rows = MATRIX
    cols = numpy.transpose(MATRIX).tolist()

    # prog = loop(
    #     sequence([
    #         blink(rows[0], 0.05, 2),
    #         blink(rows[1], 0.10, 2),
    #         blink(rows[2], 0.15, 2),
    #         blink(rows[3], 0.20, 2),
    #         blink(rows[4], 0.25, 2),

    #         cycle(cols[0], 0.05, 2),
    #         cycle(cols[1], 0.05, 2),
    #         cycle(cols[2], 0.05, 2),
    #         cycle(cols[3], 0.05, 2),
    #         cycle(cols[4], 0.05, 2),
    #     ]),
    #     3
    # )

    prog = blink(rows[0], 0.05, 2)


    coro = prog()
    await coro

asyncio.run(main())
