from math import log

from utils import Line, SLPException


class SLP:
    def __init__(self):
        self.lines = [Line("DUMMY", "LINE", '+')]
        self.values = [1]
        self.value = 1

    def add(self, line):
        if line.x >= len(self.lines) or line.y >= len(self.lines):
            raise SLPException("Line index too large")
        self.lines.append(line)
        self.evaluate(line)

    def evaluate(self, line):
        if line.symbol == '*':
            self.values.append(self.values[line.x]*self.values[line.y])
        elif line.symbol == '+':
            self.values.append(self.values[line.x]+self.values[line.y])
        elif line.symbol == '-':
            self.values.append(self.values[line.x]-self.values[line.y])
        else:
            raise SLPException("Unknown Symbol")
        self.value = self.values[-1]

    def __str__(self):
        max_len = int(log(len(self.lines), 10))+1
        to_return = '{p1}L0: {p1}1\n'.format(
            p1=' ' * (max_len - 1),
            value=1
        )
        i = 1
        for line in self.lines[1:]:
            to_return += '{p1}L{i}: {p2}L{x} {symbol} L{y}\n'.format(
                p1=' ' * (max_len - len(str(i))),
                p2=' ' * (max_len - len(str(line.x))),
                p3=' ' * (max_len - len(str(line.y))),
                i=i,
                x=line.x,
                symbol=line.symbol,
                y=line.y
            )
            i += 1
        return to_return[:-1]

    def __repr__(self):
        max_len = int(log(len(self.lines), 10))+1
        to_return = '{p1}L0: {p1}1    {p1}    = {value}\n'.format(
            p1=' ' * (max_len - 1),
            value=1
        )
        i = 1
        for line in self.lines[1:]:
            to_return += '{p1}L{i}: {p2}L{x} {symbol} L{y} {p3} = {value}\n'.format(
                p1=' ' * (max_len - len(str(i))),
                p2=' ' * (max_len - len(str(line.x))),
                p3=' ' * (max_len - len(str(line.y))),
                i=i,
                x=line.x,
                symbol=line.symbol,
                y=line.y,
                value=self.values[i]
            )
            i += 1
        return to_return[:-1]


class PosSLP(SLP):
    def add(self, line):
        if line.symbol == '-':
            raise SLPException("No subtraction allowed in PosSLPs")
        super().add(line)
