#!/usr/bin/env python

from blink.glt2024.box import Box
from blink.base.program import launch_isolated, on, sleep, any, all, repeat, forever, sequence, walk, blink, wait_button

import asyncio


box = Box()

prog = on(box.matrix.get(2,2))

async def main():
    await launch_isolated(prog)

asyncio.run(main())
