#!/usr/bin/env python

from blink.glt2024 import GLTMatrix, blink_rows, blink_cols, cycle_cols, spiral, mad
from blink.blink import launch

import asyncio


matrix = GLTMatrix()

async def main():
    await launch(mad(matrix))

asyncio.run(main())
