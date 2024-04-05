from ..base.program import program, launch, on, sleep, sequence, any, all, blink, cycle, wait_button, forever, repeat, walk
from ..base.io import Output


@program
async def blink_rows(box):
    '''Running down row-wise, blink each row as we go

    '''

    nrows, _ = box.matrix.shape()
    rows = [box.matrix.row(rowno) for rowno in range(nrows)]

    prog = sequence(
        blink(Output.from_many(rows[0]), 0.09, 3),
        blink(Output.from_many(rows[1]), 0.08, 3),
        blink(Output.from_many(rows[2]), 0.07, 3),
        blink(Output.from_many(rows[3]), 0.06, 3),                 
        blink(Output.from_many(rows[4]), 0.05, 3),                 
    )
    await prog()

@program
async def blink_cols(box):
    '''Blink each column, left-to-right'''

    _, ncols = box.matrix.shape()
    cols = [box.matrix.col(colno) for colno in range(ncols)]

    prog = sequence(
        blink(Output.from_many(cols[0]), 0.09, 3),
        blink(Output.from_many(cols[1]), 0.08, 3),
        blink(Output.from_many(cols[2]), 0.07, 3),
        blink(Output.from_many(cols[3]), 0.06, 3),                 
        blink(Output.from_many(cols[4]), 0.05, 3),                 
    )
    await prog()

@program
async def raindrops(box):
    '''
    Five columns of rain
    '''
    prog = all(
        cycle(box.matrix.col(0), 0.11),
        cycle(box.matrix.col(1), 0.13),
        cycle(box.matrix.col(2), 0.15),
        cycle(box.matrix.col(3), 0.17),
        cycle(box.matrix.col(4), 0.19),
    )
    await prog()

@program
async def spiral(box):
    '''
    Spiral, running clockwise inwards, ending in rapidly blinking center.

    * Left button: start over
    * Right button: quit
    '''
    prog = any(
        forever(
            sequence(
                walk(box.matrix.outer_ring_clockwise(), 0.07),
                walk(box.matrix.inner_ring_clockwise(), 0.10),
                any(
                    blink(box.matrix.get(2,2), 0.04),
                    wait_button(box.buttons.left),
                ),
            )
        ),
        wait_button(box.buttons.right),
    )
    await prog()

@program 
async def mad_spiral(box):
    '''
    Outer and inner ring rotating in opposite directions, center blinking madly
    '''
    prog = all(
        cycle(box.matrix.outer_ring_clockwise(), 0.07),
        cycle(reversed(box.matrix.inner_ring_clockwise()), 0.10),
        blink(box.matrix.get(2,2), 0.07),
    )
    await prog()

@program
async def mad_spiral_until_left_button(box):
    '''
    * Beginning: outer and inner ring rotating in opposite directions, center blinking madly
    * On left button: center blinking in 1-second interval
    * On left button: center blinking rapidly, and then quits
    '''
    prog = sequence(
        any(
            all(
                forever(walk(box.matrix.outer_ring_clockwise(), 0.05)),
                forever(walk(list(reversed(box.matrix.inner_ring_clockwise())), 0.07)),
                blink(box.matrix.get(2,2), 0.5),
            ),
            wait_button(box.buttons.left),
        ),
        any(
            blink(box.matrix.get(2,2), 1),
            any(wait_button(box.buttons.left), wait_button(box.buttons.right)),
        ),
        any(
            blink(box.matrix.get(2,2), 0.03),
            sleep(2),
        ),
    )
    await prog()

@program
async def mickey(box):
    '''
    Mickey mouse. Hit on his ears until dead.
    '''
    left_eye_full = Output.from_many(
        (
            box.matrix.get(0,0),
            box.matrix.get(0,1),
            box.matrix.get(0,2),
            box.matrix.get(1,0),
            box.matrix.get(1,1),
            box.matrix.get(1,2),
            box.matrix.get(2,0),
            box.matrix.get(2,1),
            box.matrix.get(2,2),
        ))
    left_eye_cross = Output.from_many(
        (
            box.matrix.get(0,0),
            box.matrix.get(0,2),
            box.matrix.get(1,1),
            box.matrix.get(2,0),
            box.matrix.get(2,2),
        ))
    left_eye_dot = box.matrix.get(1,1)
    right_eye_full = Output.from_many(
        (
            box.matrix.get(0,2),
            box.matrix.get(0,3),
            box.matrix.get(0,4),
            box.matrix.get(1,2),
            box.matrix.get(1,3),
            box.matrix.get(1,4),
            box.matrix.get(2,2),
            box.matrix.get(2,3),
            box.matrix.get(2,4),
        ))
    right_eye_cross = Output.from_many(
        (
            box.matrix.get(0,2),
            box.matrix.get(0,4),
            box.matrix.get(1,3),
            box.matrix.get(2,2),
            box.matrix.get(2,4),
        ))
    right_eye_dot = box.matrix.get(1, 3)

    mouth_up = Output.from_many(
        (
            box.matrix.get(3,0),
            box.matrix.get(4,1),
            box.matrix.get(4,2),
            box.matrix.get(4,3),
            box.matrix.get(3,4),
        ))
    mouth_straight = Output.from_many(
        (
            box.matrix.get(4,0),
            box.matrix.get(4,1),
            box.matrix.get(4,2),
            box.matrix.get(4,3),
            box.matrix.get(4,4),
        ))
    mouth_down = Output.from_many(
        (
            box.matrix.get(4,0),
            box.matrix.get(3,1),
            box.matrix.get(3,2),
            box.matrix.get(3,3),
            box.matrix.get(4,4),
        ))

    await launch(
        sequence(
            any(
                on(mouth_up),
                any(
                    repeat(
                        sequence(                
                            any(
                                blink(left_eye_full, interval=0.5),
                                wait_button(box.buttons.left),
                            ),
                            any(
                                blink(left_eye_dot, interval=0.5),
                                wait_button(box.buttons.left),
                            ),
                        ),
                        ntimes=3
                    ),
                    repeat(
                        sequence(                
                            sleep(0.5),
                            any(
                                blink(right_eye_full, interval=0.5),
                                wait_button(box.buttons.right),
                            ),
                            any(
                                blink(right_eye_dot, interval=0.5),
                                wait_button(box.buttons.right),
                            ),
                        ),
                        ntimes=3
                    ),
                ),
            ),
            any(
                on(mouth_straight),
                all(
                    any(
                        on(left_eye_dot),
                        wait_button(box.buttons.left),
                    ),
                    any(
                        on(right_eye_dot),
                        wait_button(box.buttons.right),
                    ),
                ),
            ),
            any(
                on(mouth_straight),
                all(
                    on(left_eye_cross),
                    on(right_eye_cross),
                ),
                all(
                    wait_button(box.buttons.left),
                    wait_button(box.buttons.right),
                )
            ),
            all(
                on(left_eye_cross),
                on(right_eye_cross),
                on(mouth_down),
            ),
        )
    )

@program
async def all_directions(box):
    '''
    Inner and outer circle rotate.

    * Left button: change direction of inner circle
    * Right button: change direction of outer circle
    '''
    await launch(
        all(
            forever(
                sequence(
                    any(
                        cycle(box.matrix.outer_ring_clockwise(), interval=0.1),
                        wait_button(box.buttons.left),
                    ),
                    any(
                        cycle(list(reversed(box.matrix.outer_ring_clockwise())), interval=0.1),
                        wait_button(box.buttons.left),
                    ),
                )
            ),
            forever(
                sequence(
                    any(
                        cycle(box.matrix.inner_ring_clockwise(), interval=0.2),
                        wait_button(box.buttons.right),
                    ),
                    any(
                        cycle(list(reversed(box.matrix.inner_ring_clockwise())), interval=0.2),
                        wait_button(box.buttons.right),
                    ),
                )
            ),
        )
    )

@program
async def kaa(box):
    '''
    Concentrically, hypnotize the audience.

    * Left button: reverse direction
    * Right button: furious termination
    '''

    inner = box.matrix.get(2,2)
    middle = Output.from_many(box.matrix.inner_ring_clockwise())
    outer = Output.from_many(box.matrix.outer_ring_clockwise())

    prog = sequence(
        any(
            forever(
                sequence(
                    any(
                        cycle([inner, middle, outer], interval=0.4),
                        wait_button(box.buttons.left),
                    ),
                    any(
                        cycle([outer, middle, inner], interval=0.4),
                        wait_button(box.buttons.left),
                    ),
                )
            ),
            wait_button(box.buttons.right),
        ),
        blink(Output.from_many(box.matrix.all()), interval=0.04, ntimes=15),
    )

    await prog()

@program
async def _walk_outer(matrix, clockwise, interval):
    if clockwise:
        outputs = matrix.outer_ring_clockwise()
    else:
        outputs = list(reversed(matrix.outer_ring_clockwise()))
        
    prog = walk(outputs, interval=interval)
    await prog()

@program
async def _walk_inner(matrix, clockwise, interval):
    if clockwise:
        outputs = matrix.inner_ring_clockwise()
    else:
        outputs = list(reversed(matrix.inner_ring_clockwise()))
        
    prog = walk(outputs, interval=interval)
    await prog()

@program
async def kaa_spiral(box):
    '''
    Concentrically, hypnotize the audience.

    * Left button: reverse direction
    * Right button: furious termination
    '''

    inner = box.matrix.get(2,2)

    prog = sequence(
        any(
            forever(
                sequence(
                    any(
                        forever(
                            sequence(
                                any(
                                    blink(inner, interval=0.05),
                                    sleep(0.5),
                                ),
                                any(
                                    _walk_inner(box.matrix, clockwise=True, interval=0.05),
                                    sleep(1),
                                ),
                                any(
                                    _walk_outer(box.matrix, clockwise=True, interval=0.05),
                                    sleep(1),
                                ),
                            ),
                        ),
                        wait_button(box.buttons.left),
                    ),
                    any(
                        forever(
                            sequence(
                                any(
                                    _walk_outer(box.matrix, clockwise=False, interval=0.05),
                                    sleep(1),
                                ),
                                any(
                                    _walk_inner(box.matrix, clockwise=False, interval=0.05),
                                    sleep(1),
                                ),
                                any(
                                    blink(inner, interval=0.05),
                                    sleep(0.5),
                                ),
                            ),
                        ),
                        wait_button(box.buttons.left),
                    ),
                )
            ),
            wait_button(box.buttons.right),
        ),
        blink(Output.from_many(box.matrix.all()), interval=0.04, ntimes=15),
    )

    await prog()

@program
async def the_nice_pattern(box):
    '''Inner circle rotates clockwise, outer circle rotates
    counterclockwise.

    * Left button: suspend
    * Right button: resume
    '''
    prog = forever(
        sequence(
            any(
                all(
                    forever(walk(box.matrix.outer_ring_clockwise(), 0.05)),
                    forever(walk(list(reversed(box.matrix.inner_ring_clockwise())), 0.07)),
                    blink(box.matrix.get(2,2), 0.5),
                ),
                wait_button(box.buttons.left),
            ),
            wait_button(box.buttons.right),
        )
    )

    await prog()
    

menu = (
    blink_rows,
    blink_cols,
    raindrops,
    spiral,
    mad_spiral,
    mad_spiral_until_left_button,
    mickey,
    all_directions,
    kaa,
    kaa_spiral,
    the_nice_pattern,
)
