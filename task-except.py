#!/usr/bin/env python

from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Button

import asyncio

async def crash():
    assert False

async def main():
    task = asyncio.create_task(crash())
    await task

asyncio.run(main())
