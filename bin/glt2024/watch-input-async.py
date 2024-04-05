#!/usr/bin/env python3

import gpiod
from gpiod.line import Edge

import asyncio
from datetime import timedelta


request = gpiod.request_lines('/dev/gpiochip0',
                              consumer="watch-input-async.py",
                              config={19: gpiod.LineSettings(edge_detection=Edge.RISING,
                                                             debounce_period=timedelta(milliseconds=10),
                                                             )
                                      },
                              )

async def read_events(request):
    loop = asyncio.get_running_loop()

    while True:
        future = loop.create_future()
        def callback():
            events = request.read_edge_events()
            future.set_result(events)

        loop.add_reader(request.fd, callback)
        await future

        events = future.result()
        for event in events:
            print(f'line: {event.line_offset}, type: falling, seq: {event.line_seqno}')


asyncio.run(read_events(request))
