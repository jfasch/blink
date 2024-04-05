#!/usr/bin/env python3

import gpiod
from gpiod.line import Edge
from datetime import timedelta
import asyncio


async def events(device, number):
    request = gpiod.request_lines(
        device,
        config={number: gpiod.LineSettings(edge_detection=Edge.FALLING,
                                           debounce_period=timedelta(milliseconds=10))}
    )

    loop = asyncio.get_running_loop()
    events_ready = loop.create_future()

    def callback():
        events = request.read_edge_events()
        events_ready.set_result(events)

    loop.add_reader(request.fd, callback)

    while True:
        await events_ready
        events = events_ready.result()
        events_ready = loop.create_future()
        for event in events:
            yield event

async def print_events(device, number):
    async for event in events(device, number):
        print(f'line: {event.line_offset}, seq: {event.line_seqno}, ns: {event.timestamp_ns}')

async def main():
    t1 = asyncio.create_task(print_events('/dev/gpiochip0', 26))
    t2 = asyncio.create_task(print_events('/dev/gpiochip0', 19))

    await t1
    await t2

asyncio.run(main())
