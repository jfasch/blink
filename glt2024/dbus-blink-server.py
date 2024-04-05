#!/usr/bin/env python

from blink import dbus_iface

import sdbus
import asyncio


async def main():
    blink_object = dbus_iface.Blink()

    await sdbus.request_default_bus_name_async('me.faschingbauer.blinktest')
    blink_object.export_to_dbus('/')
    while True: # hmm. can't I await something from sdbus?
        await asyncio.sleep(10000)

asyncio.run(main())
