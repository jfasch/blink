#!/usr/bin/env python

from  pathlib import Path
import time
import itertools
import os

from stuff.gpios import MATRIX

LINEAR = tuple(itertools.chain(*MATRIX))

base = Path('/sys/class/gpio')

try:
    print('requesting IOs ...')
    for nr in LINEAR:
        gpiodir = base / f'gpio{nr}'
        if os.path.isdir(gpiodir):
            continue
        with open(base / 'export', 'w') as f:
            f.write(str(nr))

    time.sleep(1)

    print('configuring IOs ...')
    for nr in LINEAR:
        gpiodir = base / f'gpio{nr}'
        with open(gpiodir / 'direction', 'w') as f:
            f.write('out')

    time.sleep(1)

    for nr in LINEAR:
        gpiodir = base / f'gpio{nr}'
        with open(gpiodir / 'value', 'w') as f:
            f.write('1')
        input(f'{nr} (RET to continue)')
        with open(gpiodir / 'value', 'w') as f:
            f.write('0')

finally:
    print('unrequesting IOs ...')
    for nr in LINEAR:
        gpiodir = base / f'gpio{nr}'
        if not os.path.isdir(gpiodir):
            continue
        with open(base / 'unexport', 'w') as f:
            f.write(str(nr))

    time.sleep(0.5)
