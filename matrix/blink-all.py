#!/usr/bin/env python

from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value

from stuff.gpios import MATRIX, REQUEST

from time import sleep
import itertools
import sys
import os


CHIP = '/dev/gpiochip0'
CONSUMER = os.path.basename(sys.argv[0])

for _ in range(10):
    REQUEST().set_values({i: Value(1) for i in itertools.chain(*MATRIX)})
    sleep(0.2)
    REQUEST().set_values({i: Value(0) for i in itertools.chain(*MATRIX)})
    sleep(0.2)
