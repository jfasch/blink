#!/usr/bin/env python

from blink.glt2024.box import Box
from blink.glt2024.programs import mad_spiral, mad_spiral_until_left_button, mickey, all_directions, spiral, kaa, kaa_spiral, blink_rows, blink_cols, raindrops
from blink.base.program import launch_isolated

import asyncio


box = Box()

async def main():
    prog = blink_rows(box)
    # prog = blink_cols(box)
    # prog = raindrops(box)
    # prog = spiral(box)
    # prog = mad_spiral(box)
    # prog = mad_spiral_until_left_button(box)
    # prog = mickey(box)
    # prog = all_directions(box)
    # prog = kaa(box)
    # prog = kaa_spiral(box)

    await launch_isolated(prog)
    
asyncio.run(main())
