#!/usr/bin/env python

from blink.glt2024 import GLTMatrix, GLTButtons, blink_rows, blink_cols, cycle_cols, spiral, mad, wait_button, mad_spiral_until_left_button
from blink.blink import launch_isolated, walk, on, sleep, any, all, forever, sequence, blink, TASK_GROUP
from blink.io import Output

import asyncio
import contextvars


buttons = GLTButtons()
matrix = GLTMatrix()

# @program:
# async def mickey(matrix, left_ear, right_ear):
#     lefteye = Output.from_many(
#         (
#             matrix.get(0,0),
#             matrix.get(0,1),
#             matrix.get(0,2),
#             matrix.get(1,0),
#             matrix.get(1,1),
#             matrix.get(1,2),
#             matrix.get(2,0),
#             matrix.get(2,1),
#             matrix.get(2,2),
#         ))
#     righteye = Output.from_many(
#         (
#             matrix.get(0,2),
#             matrix.get(0,3),
#             matrix.get(0,4),
#             matrix.get(1,2),
#             matrix.get(1,3),
#             matrix.get(1,4),
#             matrix.get(2,2),
#             matrix.get(2,3),
#             matrix.get(2,4),
#         ))

#     mouthup = Output.from_many(
#         (
#             matrix.get(3,0),
#             matrix.get(4,1),
#             matrix.get(4,2),
#             matrix.get(4,3),
#             matrix.get(3,4),
#         ))

#     await launch(
#         any(
#             sleep(2),
            
#     )

async def main():
    context = contextvars.copy_context()
    async with asyncio.TaskGroup() as tg:
        global TASK_GROUP
        TASK_GROUP.set(tg)
        await launch_isolated(mad_spiral_until_left_button(matrix=matrix, buttons=buttons))
    
asyncio.run(main())
