#!/usr/bin/env python3

import gpiod
from gpiod.line import Edge
from datetime import timedelta


request = gpiod.request_lines(
    '/dev/gpiochip0',
    config={26: gpiod.LineSettings(edge_detection=Edge.RISING)}
)
while True:
    for event in request.read_edge_events():   # blocks until events are available
        print(f'line: {event.line_offset}, seq: {event.line_seqno}, ns: {event.timestamp_ns}')
