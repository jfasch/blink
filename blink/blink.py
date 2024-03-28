import asyncio
import itertools
import functools
import contextvars


def program(func):
    @functools.wraps(func)
    def factory(*args, **kwargs):
        @functools.wraps(func)
        def create_coro():
            return func(*args, **kwargs)
        return create_coro
    return factory


TASK_GROUP = contextvars.ContextVar('_BLINK_TASK_GROUP')

async def launch_isolated(prog):
    async with asyncio.TaskGroup() as tg:
        global TASK_GROUP
        TASK_GROUP.set(tg)
        await launch(prog)

def launch(prog):
    tg = TASK_GROUP.get()
    return tg.create_task(prog())

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
