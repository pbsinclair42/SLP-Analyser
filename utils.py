class SLPException(Exception):
    pass


class Line:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        if symbol not in ['*', '-', '+']:
            raise SLPException("Unknown Symbol")
