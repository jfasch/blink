#!/usr/bin/env python

from blink.glt2024 import GLTMatrix, blink_rows, blink_cols, cycle_cols, spiral
from blink.blink import launch, cycle, blink
from blink.io import IOS

import asyncio


matrix = GLTMatrix()

async def main():
    await launch(spiral(matrix))

asyncio.run(main())
