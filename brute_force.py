from slp import SLP, PosSLP
from utils import Line


class Analyser:

    def __init__(self, pos=False):
        self.slps = [{PosSLP(minimized=True) if pos else SLP(minimized=True)}]
        self.values = {1}
        self.current_size = 1
        self.pos = pos

    def get_all_next_slps(self, slp):
        all_next_slps = set()
        for i in range(len(slp)):
            for j in range(len(slp)):
                next_slps = [slp.deepcopy() for _ in range(2 if self.pos else 3)]
                next_slps[0].add(Line(i, j, '*'))
                next_slps[1].add(Line(i, j, '+'))
                if not self.pos:
                    next_slps[2].add(Line(i, j, '-'))
                # filter out negative slps and slps with multiple lines of the same value
                next_slps = {slp for slp in next_slps if slp.value > 0 and slp.value not in slp.values[:-1]}
                all_next_slps.update(next_slps)
        return all_next_slps

    def calculate_next_values(self):
        new_slps = set()
        for slp in self.slps[-1]:
            next_slps = self.get_all_next_slps(slp)
            new_values = {slp.value for slp in next_slps}
            self.values.update(new_values)
            new_slps.update(next_slps)
        self.slps.append(new_slps)
        self.current_size += 1
