#!/usr/bin/env python

from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Bias, Value

from stuff.gpios import MATRIX

import sys
import os


CHIP = '/dev/gpiochip0'
CONSUMER = os.path.basename(sys.argv[0])

request = request_lines(
    CHIP, 
    consumer=CONSUMER, 
    config={MATRIX[0][0]: LineSettings(direction=Direction.OUTPUT, bias=Bias.PULL_DOWN)})

request.set_value(MATRIX[0][0], Value(1))
