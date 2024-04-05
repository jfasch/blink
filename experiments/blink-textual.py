#!/usr/bin/env python

from blink import blink

from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static

import asyncio
import itertools


class ButtonIOS:
    def __init__(self, buttons):
        self.buttons = buttons
    def set(self, value):
        for b in self.buttons:
            b.label = 'ON' if value else 'OFF'
    def iter(self):
        for b in self.buttons:
            yield ButtonIOS([b])

async def runcoro(coro):
    try:
        await coro
    except Exception as e:
        open('/tmp/xxx', 'a').write(str(e)+'\n')
        
class BlinkApp(App):
    def compose(self):
        # self.program = blink.all([
        #     blink.blink(ButtonIOS(self.matrix[0]), 0.1),
        #     blink.blink(ButtonIOS(self.matrix[1]), 0.2),
        #     blink.blink(ButtonIOS(self.matrix[2]), 0.3),
        #     blink.blink(ButtonIOS(self.matrix[3]), 0.4),
        #     blink.blink(ButtonIOS(self.matrix[4]), 0.5),
        # ])

        # self.program = blink.cycle(ButtonIOS(self.matrix[0]), 0.2)

        #self.program = blink.blink(ButtonIOS(self.matrix[0][0]), 0.2)
        #self.program = blink.on(ButtonIOS(self.matrix[0]))

        self.program = blink.crash()

        with Vertical():
            for i in range(5):
                with Horizontal():
                    for j in range(5):
                        yield Button('OFF')

    def on_mount(self):
        # async with asyncio.TaskGroup() as tg:
        #     self.progtask = tg.create_task(blink.crash()())
#        self.progtask = asyncio.create_task(self.program())
        self.runner = asyncio.create_task(runcoro(self.program()))

app = BlinkApp()
app.run()
