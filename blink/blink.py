import asyncio
import itertools


if False:
    import gpiod

    MATRIX = (
        (11, 10, 27,  4,  2),
        ( 0,  9, 22, 17,  3),
        ( 5, 20,  1, 25, 18),
        ( 6, 16,  7, 24, 15),
        (13, 12,  8, 23, 14),
    )

    REQUEST = gpiod.request_lines(
        '/dev/gpiochip0',
        consumer='glt2023',
        config={sum(MATRIX, start=()): gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)})

    def SET_VALUES(ios, b):
        REQUEST.set_values({i: gpiod.line.Value(b) for i in ios})

def program(func):
    def factory(*args, **kwargs):
        def create_coro():
            return func(*args, **kwargs)
        return create_coro
    return factory

def launch(prog):
    # return asyncio.ensure_future(prog())
    return asyncio.create_task(prog())

@program
async def on(ios):
    try:
        ios.set(True)
        await asyncio.get_running_loop().create_future()   # <--- sit until cancelled
    finally:
        ios.set(False)

@program
async def crash():
#    open('/tmp/xxx', 'a').write('I was here\n')
    assert False, 'yay'

@program
async def blink(ios, interval, ntimes=None):
    loop = (ntimes is None) and itertools.count() or range(ntimes)
    try:
        for _ in loop:
            ios.set(True)
            await asyncio.sleep(interval)
            ios.set(False)
            await asyncio.sleep(interval)
    finally:
        ios.set(False)

@program
async def sleep(secs):
    await asyncio.sleep(secs)

@program
async def forever(prog):
    current = None
    try:
        while True:
            current = launch(prog)
            await current
    finally:
        current.cancel()

@program
async def sequence(progs):
    current = None
    try:
        for p in progs:
            current = launch(p)
            await current
    finally:
        if current:
            current.cancel()

@program
async def cycle(ios, interval):
    assert False
    for io in itertools.cycle(ios):
        io.set(True)
        await asyncio.sleep(interval)
        io.set(False)
        await asyncio.sleep(interval)

@program
async def any(progs):
    tasks = [launch(p) for p in progs]
    try:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for p in pending:
            p.cancel()
    finally:
        for t in tasks:
            t.cancel()

@program
async def all(progs):
    task = None
    try:
        task = asyncio.gather(*[p() for p in progs])
        await task
    finally:
        if task:
            task.cancel()

