#!/usr/bin/env python

from blink.glt2024 import GLTMatrix, GLTButtons, blink_rows, blink_cols, cycle_cols, spiral, mad, wait_button, mad_spiral_until_left_button
from blink.blink import launch_isolated, launch, walk, on, sleep, any, all, forever, sequence, blink, TASK_GROUP, program, repeat, cycle
from blink.io import Output

import asyncio
import contextvars


buttons = GLTButtons()
matrix = GLTMatrix()

@program
async def mickey(matrix, left_ear, right_ear):
    left_eye_full = Output.from_many(
        (
            matrix.get(0,0),
            matrix.get(0,1),
            matrix.get(0,2),
            matrix.get(1,0),
            matrix.get(1,1),
            matrix.get(1,2),
            matrix.get(2,0),
            matrix.get(2,1),
            matrix.get(2,2),
        ))
    left_eye_cross = Output.from_many(
        (
            matrix.get(0,0),
            matrix.get(0,2),
            matrix.get(1,1),
            matrix.get(2,0),
            matrix.get(2,2),
        ))
    left_eye_dot = matrix.get(1,1)
    right_eye_full = Output.from_many(
        (
            matrix.get(0,2),
            matrix.get(0,3),
            matrix.get(0,4),
            matrix.get(1,2),
            matrix.get(1,3),
            matrix.get(1,4),
            matrix.get(2,2),
            matrix.get(2,3),
            matrix.get(2,4),
        ))
    right_eye_cross = Output.from_many(
        (
            matrix.get(0,2),
            matrix.get(0,4),
            matrix.get(1,3),
            matrix.get(2,2),
            matrix.get(2,4),
        ))
    right_eye_dot = matrix.get(1, 3)

    mouth_up = Output.from_many(
        (
            matrix.get(3,0),
            matrix.get(4,1),
            matrix.get(4,2),
            matrix.get(4,3),
            matrix.get(3,4),
        ))
    mouth_straight = Output.from_many(
        (
            matrix.get(4,0),
            matrix.get(4,1),
            matrix.get(4,2),
            matrix.get(4,3),
            matrix.get(4,4),
        ))
    mouth_down = Output.from_many(
        (
            matrix.get(4,0),
            matrix.get(3,1),
            matrix.get(3,2),
            matrix.get(3,3),
            matrix.get(4,4),
        ))

    await launch(
        sequence(
            any(
                on(mouth_up),
                any(
                    repeat(
                        sequence(                
                            any(
                                blink(left_eye_full, interval=0.5),
                                wait_button(left_ear),
                            ),
                            any(
                                blink(left_eye_dot, interval=0.5),
                                wait_button(left_ear),
                            ),
                        ),
                        ntimes=3
                    ),
                    repeat(
                        sequence(                
                            sleep(0.5),
                            any(
                                blink(right_eye_full, interval=0.5),
                                wait_button(right_ear),
                            ),
                            any(
                                blink(right_eye_dot, interval=0.5),
                                wait_button(right_ear),
                            ),
                        ),
                        ntimes=3
                    ),
                ),
            ),
            any(
                on(mouth_straight),
                all(
                    any(
                        on(left_eye_dot),
                        wait_button(left_ear),
                    ),
                    any(
                        on(right_eye_dot),
                        wait_button(right_ear),
                    ),
                ),
            ),
            any(
                on(mouth_straight),
                all(
                    on(left_eye_cross),
                    on(right_eye_cross),
                ),
                all(
                    wait_button(left_ear),
                    wait_button(right_ear),
                )
            ),
            all(
                on(left_eye_cross),
                on(right_eye_cross),
                on(mouth_down),
            ),
        )
    )

@program
async def all_directions(matrix, left_ear, right_ear):
    await launch(
        all(
            forever(
                sequence(
                    any(
                        cycle(matrix.outer_ring_clockwise(), interval=0.1),
                        wait_button(left_ear),
                    ),
                    any(
                        cycle(list(reversed(matrix.outer_ring_clockwise())), interval=0.1),
                        wait_button(left_ear),
                    ),
                )
            ),
            forever(
                sequence(
                    any(
                        cycle(matrix.inner_ring_clockwise(), interval=0.2),
                        wait_button(right_ear),
                    ),
                    any(
                        cycle(list(reversed(matrix.inner_ring_clockwise())), interval=0.2),
                        wait_button(right_ear),
                    ),
                )
            ),
        )
    )

    

async def main():
    # prog = mad_spiral_until_left_button(matrix=matrix, buttons=buttons)
    # prog = mickey(matrix=matrix, left_ear=buttons.left, right_ear=buttons.right)
    prog = all_directions(matrix=matrix, left_ear=buttons.left, right_ear=buttons.right)

    context = contextvars.copy_context()
    async with asyncio.TaskGroup() as tg:
        global TASK_GROUP
        TASK_GROUP.set(tg)
        await launch_isolated(prog)
    
asyncio.run(main())
