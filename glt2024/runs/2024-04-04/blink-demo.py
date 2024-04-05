#!/usr/bin/env python

from blink.glt2024.box import Box
from blink.base.program import launch_isolated, on, sleep, any, all, forever, sequence, walk, blink, wait_button


import asyncio


box = Box()

prog = any(
    all(
        forever(walk(box.matrix.outer_ring_clockwise(), 0.05)),
        forever(walk(list(reversed(box.matrix.inner_ring_clockwise())), 0.07)),
	blink(box.matrix.get(2,2), 0.5),
    ),
    # sleep(3),
    wait_button(box.buttons.left),
)


async def main():
    await launch_isolated(prog)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
