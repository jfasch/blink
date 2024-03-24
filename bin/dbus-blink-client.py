#!/usr/bin/env python

from blink import dbus_iface

import asyncio


async def main():
    proxy = dbus_iface.Blink.new_proxy('me.faschingbauer.blinktest', '/')    
    print(await proxy.Programs())

asyncio.run(main())
