import asyncio
import itertools
import functools


def program(func):
    @functools.wraps(func)
    def factory(*args, **kwargs):
        def create_coro():
            return func(*args, **kwargs)
        return create_coro
    return factory

def launch(prog):
    return asyncio.create_task(prog())

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

    current = None
    try:
        for _ in loop:
            current = launch(prog)
            await current
    finally:
        if current:
            current.cancel()

@program
async def forever(prog):
    await launch(repeat(prog, ntimes=None))

@program
async def sequence(*progs):
    current = None
    try:
        for p in progs:
            current = launch(p)
            await current
    finally:
        if current:
            current.cancel()

@program
async def walk(outputs, interval):
    for output in outputs:
        await launch(any(on(output), sleep(interval)))

@program
async def cycle(outputs, interval):
    for output in itertools.cycle(outputs):
        await launch(any(on(output), sleep(interval)))

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
    task = None
    try:
        task = asyncio.gather(*[p() for p in progs])
        await task
    finally:
        if task:
            task.cancel()

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

    try:
        current = launch(prog)
        await current
    finally:
        current.cancel()
