from blink.base.program import launch_isolated

import sdbus
import asyncio


class Blink(
    sdbus.DbusInterfaceCommonAsync,
    interface_name='me.faschingbauer.Blink'
):
    def __init__(self, box, menu):
        super().__init__()

        self.box = box
        self.menu = menu
        self.progtask = None

    @sdbus.dbus_method_async(
        result_signature='as',
    )
    async def Programs(self):
        return [prog.__name__ for prog in self.menu]

    @sdbus.dbus_method_async(
        input_signature='s',
    )
    async def Launch(self, progname):
        if self.progtask:
            self.progtask.cancel()
        for prog in self.menu:
            if prog.__name__ == progname:
                self.progtask = asyncio.create_task(self._run_prog(prog))
                break
        else:
            assert False, f'{progname} not found'

    async def _run_prog(self, prog):
        p = prog(self.box)
        await launch_isolated(p)
