import os
import sys
import itertools

from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value


MATRIX = (
    (11, 10, 27,  4,  2),
    ( 0,  9, 22, 17,  3),
    ( 5, 20,  1, 25, 18),
    ( 6, 16,  7, 24, 15),
    (13, 12,  8, 23, 14),
)
LINEAR = tuple(itertools.chain(*MATRIX))
CHIP = '/dev/gpiochip0'

def request_gpios():
    return request_lines(
        CHIP, 
        consumer=os.path.basename(sys.argv[0]), 
        config={LINEAR: LineSettings(direction=Direction.OUTPUT)})
