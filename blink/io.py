from gpiod.line import Value


class IOS:
    def __init__(self, request, numbers):
        self.request = request
        self.numbers = numbers

    def set(self, value):
        v = Value.ACTIVE if value else Value.INACTIVE
        lines = {n: v for n in self.numbers}
        self.request.set_values(lines)

    @classmethod
    def from_ios(cls, ios):
        assert len(ios) > 0
        request = ios[0].request
        numbers = []
        for io in ios:
            for num in io.numbers:
                numbers.append(num)

        return IOS(request=request, numbers=numbers)

    def iter(self):
        for num in self.numbers:
            yield IOS(request=self.request, numbers=(num,))
