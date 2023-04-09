#!/usr/bin/env python

from stuff.gpios import MATRIX, request_gpios

from gpiod.line import Value
from time import sleep
import itertools


request = request_gpios()

for i in itertools.chain(*MATRIX):
    request.set_value(i, Value(1))
    sleep(0.05)
    request.set_value(i, Value(0))
