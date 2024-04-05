#!/usr/bin/env python

import gpiod
from gpiod.line import Direction, Value
import time


request = gpiod.request_lines('/dev/gpiochip0',
                              config={
                                  13: gpiod.LineSettings(direction=Direction.OUTPUT)
                              })

request.set_value(13, Value.ACTIVE)
time.sleep(1)
request.set_value(13, Value.INACTIVE)
