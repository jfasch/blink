#!/usr/bin/env python

from blink.glt2024.box import Box
import random
import asyncio


box = Box()
led = box.matrix.get(2,2)

async def blink(led, interval, ntimes):
    try:
        for _ in range(ntimes):
            led.set(True)
            await asyncio.sleep(interval)
            led.set(False)
            await asyncio.sleep(interval)
    finally:
        led.set(False)

async def main():
    tasks = []

    for x in range(5):
        for y in range(5):
            led = box.matrix.get(x,y)
            tasks.append(asyncio.create_task(blink(led, random.uniform(0.1, 1.5), 50)))

    for t in tasks:
        await t

asyncio.run(main())
