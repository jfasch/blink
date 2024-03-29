from .blink import program, launch, sequence, cycle, blink, all, any, walk, forever, sleep, on, repeat
from .io import Input, Output

from gpiod import request_lines, LineSettings
from gpiod.line import Direction

OUTPUTS = (
    (27,  0, 20, 12, 24),
    (17, 11, 16,  1, 23),
    ( 4,  9, 13,  7, 18),
    ( 3, 10,  6,  8, 15),
    ( 2, 22,  5, 25, 14),
)

class GLTMatrix:
    def __init__(self):
        all_numbers = sum(OUTPUTS, ())

        self.request = request_lines(
            '/dev/gpiochip0',
            consumer='glt2024',
            config={all_numbers: LineSettings(direction=Direction.OUTPUT)},
        )

        self.matrix = []
        for rowno in range(len(OUTPUTS)):
            row = []
            for colno in range(len(OUTPUTS[rowno])):
                row.append(Output(request=self.request, numbers=(OUTPUTS[rowno][colno],)))

            self.matrix.append(row)

    def shape(self):
        return len(self.matrix), len(self.matrix[0])

    def row(self, rowno):
        return self.matrix[rowno]

    def col(self, colno):
        return [self.matrix[rowno][colno] for rowno in range(len(self.matrix))]

    def all(self):
        return sum(self.matrix, [])

    def get(self, x, y):
        return self.matrix[x][y]

    def outer_ring_clockwise(self):
        return (self.get(0, 0),
                self.get(0, 1),
                self.get(0, 2),
                self.get(0, 3),
                self.get(0, 4),
                self.get(1, 4),
                self.get(2, 4),
                self.get(3, 4),
                self.get(4, 4),
                self.get(4, 3),
                self.get(4, 2),
                self.get(4, 1),
                self.get(4, 0),
                self.get(3, 0),
                self.get(2, 0),
                self.get(1, 0),
                )

    def inner_ring_clockwise(self):
        return (self.get(1, 1),
                self.get(1, 2),
                self.get(1, 3),
                self.get(2, 3),
                self.get(3, 3),
                self.get(3, 2),
                self.get(3, 1),
                self.get(2, 1),
                )

class GLTButtons:
    def __init__(self):
        self.left = Input('/dev/gpiochip0', 26);
        self.right = Input('/dev/gpiochip0', 19);
    

@program
async def blink_rows(matrix):
    nrows, _ = matrix.shape()
    rows = [matrix.row(rowno) for rowno in range(nrows)]

    prog = sequence(
        (blink(Output.from_many(rows[0]), 0.09, 3),
         blink(Output.from_many(rows[1]), 0.08, 3),
         blink(Output.from_many(rows[2]), 0.07, 3),
         blink(Output.from_many(rows[3]), 0.06, 3),                 
         blink(Output.from_many(rows[4]), 0.05, 3),                 
         )
    )
    await prog()

@program
async def blink_cols(matrix):
    _, ncols = matrix.shape()
    cols = [matrix.col(colno) for colno in range(ncols)]

    prog = launch(
        sequence(
            (blink(Output.from_many(cols[0]), 0.09, 3),
             blink(Output.from_many(cols[1]), 0.08, 3),
             blink(Output.from_many(cols[2]), 0.07, 3),
             blink(Output.from_many(cols[3]), 0.06, 3),                 
             blink(Output.from_many(cols[4]), 0.05, 3),                 
             )
        )
    )
    await prog()

@program
async def cycle_cols(matrix):
    prog = all(
        (cycle(matrix.col(0), 0.09),
         cycle(matrix.col(1), 0.08),
         cycle(matrix.col(2), 0.07),
         cycle(matrix.col(3), 0.06),
         cycle(matrix.col(4), 0.05),
         )
    )
    await prog()

@program
async def spiral(matrix, buttons):
    prog = any(
        forever(
            sequence(
                walk(matrix.outer_ring_clockwise(), 0.07),
                walk(matrix.inner_ring_clockwise(), 0.10),
                any(
                    blink(matrix.get(2,2), 0.01),
                    wait_button(buttons.left),
                ),
            )
        ),
        wait_button(buttons.right),
    )
    await prog()

@program 
async def mad(matrix):
    prog = all(
        cycle(matrix.outer_ring_clockwise(), 0.07),
        cycle(reversed(matrix.inner_ring_clockwise()), 0.10),
        blink(matrix.get(2,2), 0.07),
    )
    await prog()

@program
async def wait_button(button):
    import gpiod
    import datetime
    import asyncio

    with gpiod.request_lines(button.device,
                             consumer='glt2024',
                             config={button.number: gpiod.LineSettings(edge_detection=gpiod.line.Edge.RISING,
                                                                       debounce_period=datetime.timedelta(milliseconds=10),
                                                                       )
                                     },
                             ) as request:
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        loop.create_future()

        def callback():
            request.read_edge_events(1)
            future.set_result(True)

        loop.add_reader(request.fd, callback)
        try:
            await future
        finally:
            loop.remove_reader(request.fd)

@program
async def mad_spiral_until_left_button(matrix, buttons):
    # await sequence(
    prog = sequence(
        any(
            all(
                forever(walk(matrix.outer_ring_clockwise(), 0.05)),
                forever(walk(list(reversed(matrix.inner_ring_clockwise())), 0.07)),
                blink(matrix.get(2,2), 0.5),
            ),
            wait_button(buttons.left),
        ),
        any(
            blink(matrix.get(2,2), 1),
            any(wait_button(buttons.left), wait_button(buttons.right)),
        ),
        any(
            blink(matrix.get(2,2), 0.01),
            sleep(2),
        ),
    )
    await prog()

@program
async def mickey(matrix, left_ear, right_ear):
    left_eye_full = Output.from_many(
        (
            matrix.get(0,0),
            matrix.get(0,1),
            matrix.get(0,2),
            matrix.get(1,0),
            matrix.get(1,1),
            matrix.get(1,2),
            matrix.get(2,0),
            matrix.get(2,1),
            matrix.get(2,2),
        ))
    left_eye_cross = Output.from_many(
        (
            matrix.get(0,0),
            matrix.get(0,2),
            matrix.get(1,1),
            matrix.get(2,0),
            matrix.get(2,2),
        ))
    left_eye_dot = matrix.get(1,1)
    right_eye_full = Output.from_many(
        (
            matrix.get(0,2),
            matrix.get(0,3),
            matrix.get(0,4),
            matrix.get(1,2),
            matrix.get(1,3),
            matrix.get(1,4),
            matrix.get(2,2),
            matrix.get(2,3),
            matrix.get(2,4),
        ))
    right_eye_cross = Output.from_many(
        (
            matrix.get(0,2),
            matrix.get(0,4),
            matrix.get(1,3),
            matrix.get(2,2),
            matrix.get(2,4),
        ))
    right_eye_dot = matrix.get(1, 3)

    mouth_up = Output.from_many(
        (
            matrix.get(3,0),
            matrix.get(4,1),
            matrix.get(4,2),
            matrix.get(4,3),
            matrix.get(3,4),
        ))
    mouth_straight = Output.from_many(
        (
            matrix.get(4,0),
            matrix.get(4,1),
            matrix.get(4,2),
            matrix.get(4,3),
            matrix.get(4,4),
        ))
    mouth_down = Output.from_many(
        (
            matrix.get(4,0),
            matrix.get(3,1),
            matrix.get(3,2),
            matrix.get(3,3),
            matrix.get(4,4),
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
                                wait_button(left_ear),
                            ),
                            any(
                                blink(left_eye_dot, interval=0.5),
                                wait_button(left_ear),
                            ),
                        ),
                        ntimes=3
                    ),
                    repeat(
                        sequence(                
                            sleep(0.5),
                            any(
                                blink(right_eye_full, interval=0.5),
                                wait_button(right_ear),
                            ),
                            any(
                                blink(right_eye_dot, interval=0.5),
                                wait_button(right_ear),
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
                        wait_button(left_ear),
                    ),
                    any(
                        on(right_eye_dot),
                        wait_button(right_ear),
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
                    wait_button(left_ear),
                    wait_button(right_ear),
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
async def all_directions(matrix, buttons):
    await launch(
        all(
            forever(
                sequence(
                    any(
                        cycle(matrix.outer_ring_clockwise(), interval=0.1),
                        wait_button(buttons.left),
                    ),
                    any(
                        cycle(list(reversed(matrix.outer_ring_clockwise())), interval=0.1),
                        wait_button(buttons.left),
                    ),
                )
            ),
            forever(
                sequence(
                    any(
                        cycle(matrix.inner_ring_clockwise(), interval=0.2),
                        wait_button(buttons.right),
                    ),
                    any(
                        cycle(list(reversed(matrix.inner_ring_clockwise())), interval=0.2),
                        wait_button(buttons.right),
                    ),
                )
            ),
        )
    )

@program
async def blackhole(matrix, buttons):
    inner = matrix.get(2,2)
    middle = Output.from_many(matrix.inner_ring_clockwise())
    outer = Output.from_many(matrix.outer_ring_clockwise())

    prog = sequence(
        any(
            forever(
                sequence(
                    any(
                        cycle([inner, middle, outer], interval=0.4),
                        wait_button(buttons.left),
                    ),
                    any(
                        cycle([outer, middle, inner], interval=0.4),
                        wait_button(buttons.left),
                    ),
                )
            ),
            wait_button(buttons.right),
        ),
        blink(Output.from_many(matrix.all()), interval=0.04, ntimes=15),
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
async def blackhole_spiral(matrix, buttons):
    inner = matrix.get(2,2)

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
                                    _walk_inner(matrix, clockwise=True, interval=0.05),
                                    sleep(1),
                                ),
                                any(
                                    _walk_outer(matrix, clockwise=True, interval=0.05),
                                    sleep(1),
                                ),
                            ),
                        ),
                        wait_button(buttons.left),
                    ),
                    any(
                        forever(
                            sequence(
                                any(
                                    _walk_outer(matrix, clockwise=False, interval=0.05),
                                    sleep(1),
                                ),
                                any(
                                    _walk_inner(matrix, clockwise=False, interval=0.05),
                                    sleep(1),
                                ),
                                any(
                                    blink(inner, interval=0.05),
                                    sleep(0.5),
                                ),
                            ),
                        ),
                        wait_button(buttons.left),
                    ),
                )
            ),
            wait_button(buttons.right),
        ),
        blink(Output.from_many(matrix.all()), interval=0.04, ntimes=15),
    )

    await prog()

