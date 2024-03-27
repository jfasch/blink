#!/usr/bin/env python

from blink.glt2024 import GLTMatrix, blink_rows, blink_cols, cycle_cols, spiral, mad
from blink.blink import launch, walk, on, sleep, any, all, forever, sequence, blink

import asyncio


matrix = GLTMatrix()

async def main():
    await launch(
        any(
            all(
                forever(walk(matrix.outer_ring_clockwise(), 0.05)),
                forever(walk(list(reversed(matrix.inner_ring_clockwise())), 0.07)),
                blink(matrix.get(2,2), 0.5),
            ),
            sleep(3),
        )
    )
    
asyncio.run(main())
