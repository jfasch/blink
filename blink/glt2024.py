from .blink import program, launch, sequence, cycle, blink, all, walk, forever
from .io import Output

from gpiod import request_lines, LineSettings
from gpiod.line import Direction

_GLT_MATRIX = (
    (27,  0, 20, 12, 24),
    (17, 11, 16,  1, 23),
    ( 4,  9, 13,  7, 18),
    ( 3, 10,  6,  8, 15),
    ( 2, 22,  5, 25, 14),
)

class GLTMatrix:
    def __init__(self):
        all_numbers = sum(_GLT_MATRIX, ())

        self.request = request_lines(
            '/dev/gpiochip0',
            consumer='mytest',
            config={all_numbers: LineSettings(direction=Direction.OUTPUT)},
        )

        self.matrix = []
        for rowno in range(len(_GLT_MATRIX)):
            row = []
            for colno in range(len(_GLT_MATRIX[rowno])):
                row.append(Output(request=self.request, numbers=(_GLT_MATRIX[rowno][colno],)))

            self.matrix.append(row)

    def shape(self):
        return len(self.matrix), len(self.matrix[0])

    def row(self, rowno):
        return self.matrix[rowno]

    def col(self, colno):
        return [self.matrix[rowno][colno] for rowno in range(len(self.matrix))]

    def get(self, x, y):
        return self.matrix[x][y]

    def outer(self):
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

    def inner(self):
        return (self.get(1, 1),
                self.get(1, 2),
                self.get(1, 3),
                self.get(2, 3),
                self.get(3, 3),
                self.get(3, 2),
                self.get(3, 1),
                self.get(2, 1),
                )

@program
async def blink_rows(matrix):
    nrows, _ = matrix.shape()
    rows = [matrix.row(rowno) for rowno in range(nrows)]

    await launch(
        sequence(
            (blink(Output.from_many(rows[0]), 0.09, 3),
             blink(Output.from_many(rows[1]), 0.08, 3),
             blink(Output.from_many(rows[2]), 0.07, 3),
             blink(Output.from_many(rows[3]), 0.06, 3),                 
             blink(Output.from_many(rows[4]), 0.05, 3),                 
             )
        )
    )

@program
async def blink_cols(matrix):
    _, ncols = matrix.shape()
    cols = [matrix.col(colno) for colno in range(ncols)]

    await launch(
        sequence(
            (blink(Output.from_many(cols[0]), 0.09, 3),
             blink(Output.from_many(cols[1]), 0.08, 3),
             blink(Output.from_many(cols[2]), 0.07, 3),
             blink(Output.from_many(cols[3]), 0.06, 3),                 
             blink(Output.from_many(cols[4]), 0.05, 3),                 
             )
        )
    )

@program
async def cycle_cols(matrix):
    await launch(
        all(
            (cycle(matrix.col(0), 0.09),
             cycle(matrix.col(1), 0.08),
             cycle(matrix.col(2), 0.07),
             cycle(matrix.col(3), 0.06),
             cycle(matrix.col(4), 0.05),
             )
        )
    )

@program
async def spiral(matrix):
    await launch(
        forever(
            sequence(
                (walk(matrix.outer(), 0.07),
                 walk(matrix.inner(), 0.10),
                 blink(matrix.get(2,2), 0.01),
                 )
            )
        )
    )

@program 
async def mad(matrix):
    await launch(
        all(
            (cycle(matrix.outer(), 0.07),
             cycle(reversed(matrix.inner()), 0.10),
             blink(matrix.get(2,2), 0.07),
             )
        )
    )
