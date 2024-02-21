import asyncio
import gpiod
import itertools

MATRIX = (
    (11, 10, 27,  4,  2),
    ( 0,  9, 22, 17,  3),
    ( 5, 20,  1, 25, 18),
    ( 6, 16,  7, 24, 15),
    (13, 12,  8, 23, 14),
)
ALL_IOS = sum(MATRIX, start=())
OUTER_SQUARE = (11, 10, 27, 4, 2, 3, 18, 15, 14, 23, 8, 12, 13, 6, 5, 0)
INNER_SQUARE = (9, 22, 17, 25, 24, 7, 16, 20)
SLASH = (13, 16, 1, 17, 2)
BACKSLASH = (11, 9, 1, 24, 14)

REQUEST = gpiod.request_lines(
    '/dev/gpiochip0',
    consumer='glt2023',
    config={ALL_IOS: gpiod.LineSettings(direction=gpiod.line.Direction.OUTPUT)})

def SET_VALUES(ios, b):
    REQUEST.set_values({i: gpiod.line.Value(b) for i in ios})

def program(func):
    def factory(*args, **kwargs):
        def create_coro():
            return func(*args, **kwargs)
        return create_coro
    return factory

def launch(prog):
    return asyncio.ensure_future(prog())

@program
async def on(ios):
    try:
        SET_VALUES(ios, 1)
        await asyncio.get_running_loop().create_future()   # <--- sit until cancelled
    finally:
        SET_VALUES(ios, 0)

@program
async def blink(ios, interval, ntimes=None):
    loop = (ntimes is None) and itertools.count() or range(ntimes)
    try:
        for _ in loop:
            SET_VALUES(ios, 1)
            await asyncio.sleep(interval)
            SET_VALUES(ios, 0)
            await asyncio.sleep(interval)
    finally:
        SET_VALUES(ios, 0)

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
async def all(progs):
    task = None
    try:
        task = asyncio.gather(*[launch(p) for p in progs])
        await task
    finally:
        if task:
            task.cancel()

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
    try:
        for i in itertools.cycle(ios):
            current = launch(blink((i,), interval, 1))
            await current
    finally:
        current.cancel()

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
