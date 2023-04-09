#!/usr/bin/env python

from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value

from stuff.gpios import MATRIX, request_gpios

from time import sleep
import itertools
import sys
import os


CHIP = '/dev/gpiochip0'
CONSUMER = os.path.basename(sys.argv[0])

request = request_gpios()

for _ in range(10):
    request.set_values({i: Value(1) for i in itertools.chain(*MATRIX)})
    sleep(0.2)
    request.set_values({i: Value(0) for i in itertools.chain(*MATRIX)})
    sleep(0.2)
