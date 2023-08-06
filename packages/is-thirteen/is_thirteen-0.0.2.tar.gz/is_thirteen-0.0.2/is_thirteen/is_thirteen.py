from math import ceil, floor


class Number:
    def __init__(self, number):
        self.number = number

    def thirteen(self):
        return self.number == 13

    def roughly(self):
        if ceil(self.number) == 13:
            self.number = ceil(self.number)
        elif floor(self.number) == 13:
            self.number = floor(self.number)
        return self

    def within(self, _range: int):
        if self.number + _range > 13 or self.number - _range < 13:
            self.number = 13
            return self

    def plus(self, item: int):
        self.number += item
        return self

    def minus(self, item: int):
        self.number -= item
        return self

    def times(self, item: int):
        self.number *= item
        return self

    def divides(self, item: int):
        try:
            self.number /= item
        except ZeroDivisionError as e:
            print(e)
        return self


class Str:
    def __init__(self, string: str):
        self.string = string

    def thirteen(self):
        return self.string.lower() == "thirteen"

    def backwards(self):
        temp = list(self.string)
        self.string = ''.join(temp.pop() for _ in range(len(self.string)))
        del temp
        return self

