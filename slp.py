from math import log

from utils import Line, SLPException


class SLP:
    def __init__(self, minimized=False):
        self.minimized = minimized
        if not self.minimized:
            self.lines = [Line("DUMMY", "LINE", '+')]
        self.values = [1]
        self.value = 1

    def add(self, line):
        if line.x >= len(self.values) or line.y >= len(self.values):
            raise SLPException("Line index too large")
        if not self.minimized:
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

    def minimize(self):
        if not self.minimized:
            self.minimized = True
            del self.lines

    def __len__(self):
        return len(self.values)

    def __str__(self):
        if self.minimized:
            return str(self.values)
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
        if self.minimized:
            return str(self.values)
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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.minimized and other.minimized:
                return frozenset(self.values) == frozenset(other.values)
            else:
                return self.lines == other.lines
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if self.minimized:
            return hash(frozenset(self.values))
        else:
            return hash(tuple(self.lines))

    def deepcopy(self):
        if self.minimized:
            copy = SLP(minimized=True)
            copy.values = list(self.values)
            copy.value = copy.values[-1]
            return copy
        else:
            copy = SLP()
            for line in self.lines[1:]:
                copy.add(line)
            return copy


class mSLP(SLP):
    def add(self, line):
        if line.symbol == '-':
            raise SLPException("No subtraction allowed in mSLPs")
        super().add(line)
