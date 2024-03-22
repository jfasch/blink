#!/usr/bin/env python3

import time
import sys
from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value

ios = (11, 10, 27,  4,  2, 0,  9, 22, 17,  3, 5, 20,  1, 25, 18, 6, 16,  7, 24, 15, 13, 12,  8, 23, 14)

request = request_lines(
    '/dev/gpiochip0',
    consumer='mytest',
    config={ios: LineSettings(direction=Direction.OUTPUT)})

for io in sorted(ios):
    request.set_value(io, Value.ACTIVE)
    input(io)
    request.set_value(io, Value.INACTIVE)

