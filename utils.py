class SLPException(Exception):
    pass


class Line:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        if symbol not in ['*', '-', '+']:
            raise SLPException("Unknown Symbol")

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x)+str(self.y)+str(self.symbol))
