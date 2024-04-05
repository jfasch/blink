#!/usr/bin/env python

from blink.glt2024 import dbus_iface
from blink.glt2024.box import Box
from blink.glt2024.programs import menu

import sdbus
import asyncio


box = Box()

async def main():
    blink_object = dbus_iface.Blink(box, menu)

    await sdbus.request_default_bus_name_async('me.faschingbauer.blinktest')
    blink_object.export_to_dbus('/')
    while True: # hmm. can't I await something from sdbus?
        await asyncio.sleep(10000)

asyncio.run(main())
