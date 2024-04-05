#!/usr/bin/env python

import asyncio


async def hello_left():
    for _ in range(10):
        print('hello left')
        await asyncio.sleep(0.5)

async def hello_right():
    for _ in range(10):
        print('hello right'.rjust(60))
        await asyncio.sleep(0.4)

async def hello_middle():
    for _ in range(10):
        print('hello middle'.center(60))
        await asyncio.sleep(0.3)

async def main():
    t1 = asyncio.create_task(hello_left())
    t2 = asyncio.create_task(hello_right())
    t3 = asyncio.create_task(hello_middle())

    await t1
    await t2
    await t3

asyncio.run(main())
