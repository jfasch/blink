#!/usr/bin/env python

from blink.glt2024 import GLTMatrix, GLTButtons, blink_rows, blink_cols, cycle_cols, spiral, mad, wait_button, mad_spiral_until_left_button, blackhole, blackhole_spiral, mickey, all_directions
from blink.blink import launch_isolated, launch, walk, on, sleep, any, all, forever, sequence, blink, TASK_GROUP, program, repeat, cycle
from blink.io import Output

import asyncio
import contextvars


buttons = GLTButtons()
matrix = GLTMatrix()

async def main():
    # prog = mad_spiral_until_left_button(matrix, buttons)
    # prog = mickey(matrix=matrix, left_ear=buttons.left, right_ear=buttons.right)
    # prog = all_directions(matrix, buttons)
    # prog = spiral(matrix, buttons)
    # prog = blackhole(matrix, buttons)
    prog = blackhole_spiral(matrix, buttons)

    context = contextvars.copy_context()
    async with asyncio.TaskGroup() as tg:
        global TASK_GROUP
        TASK_GROUP.set(tg)
        await launch_isolated(prog)
    
asyncio.run(main())
