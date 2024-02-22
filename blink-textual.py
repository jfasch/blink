#!/usr/bin/env python

from textual.app import App
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static

import asyncio
import itertools


class ButtonMatrix:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.matrix = []
        for j in range(y):
            self.matrix.append([Button(f'({i},{j})') for i in range(x)])

    def get_buttons(self, coords):
        buttons = []
        for x, y in coords:
            buttons.append(self.matrix[x][y])
        return buttons

class BlinkApp(App):
    def compose(self):
        self.matrix = ButtonMatrix(10, 10)
    
        async def blink_corofunc():
            all_buttons = sum(self.matrix.matrix, start=[])
            for button in itertools.cycle(all_buttons):
                await asyncio.sleep(0.2)
                button.disabled = not button.disabled                

        self.blinker = asyncio.create_task(blink_corofunc())

        horiz = []
        for j in range(self.matrix.y):
            horiz.append(Horizontal(*self.matrix.matrix[j]))

        yield Vertical(*horiz)

if __name__ == "__main__":
    app = BlinkApp()
    app.run()
