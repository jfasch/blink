#!/usr/bin/env python3

import gpiod
from gpiod.line import Edge

from datetime import timedelta


request = gpiod.request_lines('/dev/gpiochip0',
                              consumer="watch-input-blocking.py",
                              config={19: gpiod.LineSettings(edge_detection=Edge.RISING,
                                                             debounce_period=timedelta(milliseconds=10),
                                                             )
                                      },
                              )
while True:
    for event in request.read_edge_events():   # blocks until events are available
        print(f'line: {event.line_offset}, type: falling, seq: {event.line_seqno}')
