import asyncio
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


_TASK_GROUP_VAR = contextvars.ContextVar('_BLINK_TASK_GROUP')

async def launch_isolated(prog):
    async with asyncio.TaskGroup() as tg:
        _TASK_GROUP_VAR.set(tg)
        await launch(prog)

def launch(prog):
    tg = _TASK_GROUP_VAR.get()
    return tg.create_task(prog())

