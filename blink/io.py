from gpiod.line import Value


class Output:
    def __init__(self, request, numbers):
        self.request = request
        self.numbers = numbers

    def set(self, value):
        v = Value.ACTIVE if value else Value.INACTIVE
        lines = {n: v for n in self.numbers}
        self.request.set_values(lines)

    @classmethod
    def from_many(cls, outputs):
        assert len(outputs) > 0
        request = outputs[0].request
        numbers = []
        for output in outputs:
            numbers.extend(output.numbers)

        return Output(request=request, numbers=numbers)
