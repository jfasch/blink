#!/usr/bin/env python

import gpiod
from blink.glt2024.box import Box
import asyncio


box = Box()

async def blink(output, interval):
    try:
        for _ in range(10):
            output.set(True)
            await asyncio.sleep(interval)
            output.set(False)
            await asyncio.sleep(interval)
    finally:
        output.set(False)

async def main():
    t1 = asyncio.create_task(blink(box.matrix.get(0,0), 0.2))
    t2 = asyncio.create_task(blink(box.matrix.get(2,2), 0.4))
    t3 = asyncio.create_task(blink(box.matrix.get(4,4), 0.6))

    await t1
    await t2
    await t3

asyncio.run(main())
