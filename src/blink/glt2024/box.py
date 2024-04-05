from ..base.io import Input, Output

from gpiod import request_lines, LineSettings
from gpiod.line import Direction


class Box:
    def __init__(self):
        self.matrix = LEDMatrix()
        self.buttons = Buttons()

class LEDMatrix:
    OUTPUTS = (
        (27,  0, 20, 12, 24),
        (17, 11, 16,  1, 23),
        ( 4,  9, 13,  7, 18),
        ( 3, 10,  6,  8, 15),
        ( 2, 22,  5, 25, 14),
    )

    def __init__(self):
        all_numbers = sum(self.OUTPUTS, ())  # <--- cool

        self.request = request_lines(
            '/dev/gpiochip0',
            config={all_numbers: LineSettings(direction=Direction.OUTPUT)},
        )

        self.matrix = []
        for rowno in range(len(self.OUTPUTS)):
            row = []
            for colno in range(len(self.OUTPUTS[rowno])):
                row.append(Output(request=self.request, numbers=(self.OUTPUTS[rowno][colno],)))

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

class Buttons:
    def __init__(self):
        self.left = Input('/dev/gpiochip0', 26);
        self.right = Input('/dev/gpiochip0', 19);
