from .program import program, launch

import asyncio
import itertools


@program
async def on(output):
    try:
        output.set(True)
        await asyncio.get_running_loop().create_future()   # <--- sit until cancelled
    finally:
        output.set(False)

@program
async def sleep(secs):
    await asyncio.sleep(secs)

@program
async def repeat(prog, ntimes=None):
    if ntimes is None:
        loop = itertools.count()
    else:
        loop = range(ntimes)

    for _ in loop:
        await prog()

@program
async def forever(prog):
    prog = repeat(prog, ntimes=None)
    await prog()

@program
async def sequence(*progs):
    for p in progs:
        await p()

@program
async def walk(outputs, interval):
    for output in outputs:
        prog = any(on(output), sleep(interval))
        await prog()

@program
async def cycle(outputs, interval):
    for output in itertools.cycle(outputs):
        prog = any(on(output), sleep(interval))
        await prog()

@program
async def any(*progs):
    tasks = [launch(p) for p in progs]
    try:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for p in pending:
            p.cancel()
    finally:
        for t in tasks:
            t.cancel()

@program
async def all(*progs):
    await asyncio.gather(*[p() for p in progs])

@program
async def blink(output, interval, ntimes=None):
    prog = repeat(
        sequence(
            any(
                on(output),
                sleep(interval),
            ),
            sleep(interval),
        ),
        ntimes=ntimes)

    await prog()

@program
async def wait_button(input, debounce_milli=10):
    import gpiod
    import datetime
    import asyncio

    with gpiod.request_lines(input.device,
                             consumer='glt2024',
                             config={input.number: gpiod.LineSettings(edge_detection=gpiod.line.Edge.RISING,
                                                                      debounce_period=datetime.timedelta(milliseconds=debounce_milli),
                                                                      )
                                     },
                             ) as request:
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        loop.create_future()

        def callback():
            request.read_edge_events(1)
            future.set_result(True)

        loop.add_reader(request.fd, callback)
        try:
            await future
        finally:
            loop.remove_reader(request.fd)
