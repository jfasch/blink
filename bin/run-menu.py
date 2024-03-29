#!/usr/bin/env python

from blink.glt2024.box import Box
from blink.glt2024.programs import menu
from blink.base.program import launch_isolated

from textual.app import App
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem
from textual.containers import Horizontal

import asyncio
import sys


class BlinkApp(App):
    CSS = '''
    #proglist {
        width: 30;
    }
    #progdoc {
        min-width: 50;
    }
    '''

    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.mytask = None

    def compose(self):
        yield Header()
        with Horizontal():
            proglist = ListView(id='proglist')
            for prog in self.menu:
                proglist.append(ListItem(Label(prog.__name__)))
            yield proglist
            yield Label(id='progdoc')
        yield Footer()

    def on_list_view_highlighted(self, event):
        self.query_one('#progdoc').update(self.menu[event.list_view.index].__doc__)

    def on_list_view_selected(self, event):
        if self.mytask is not None:
            self.mytask.cancel()

        prog = self.menu[event.list_view.index]
        self.mytask = asyncio.create_task(self.run_prog(prog))

    async def run_prog(self, prog):
        p = prog(box)
        await launch_isolated(p)

box = Box()
app = BlinkApp(menu)
app.run()
