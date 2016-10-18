from copy import deepcopy

from slp import SLP, PosSLP
from utils import Line


class Analyser:

    def __init__(self, pos=False):
        self.slps = [{PosSLP() if pos else SLP()}]
        self.values = {1}
        self.current_size = 1
        self.pos = pos

    def get_all_next_slps(self, slp):
        all_next_slps = []
        for i in range(len(slp)):
            for j in range(len(slp)):
                next_slps = [deepcopy(slp) for _ in range(2 if self.pos else 3)]
                next_slps[0].add(Line(i, j, '*'))
                next_slps[1].add(Line(i, j, '+'))
                if not self.pos:
                    next_slps[2].add(Line(i, j, '-'))
                all_next_slps += next_slps
        return all_next_slps

    def calculate_next_values(self):
        new_slps = set()
        for slp in self.slps[-1]:
            next_slps = self.get_all_next_slps(slp)
            next_slps = {slp for slp in next_slps if slp.value > 0}
            new_values = {slp.value for slp in next_slps}
            self.values.update(new_values)
            new_slps.update(next_slps)
        seen = set()
        new_slps = {slp for slp in new_slps if tuple(slp.values) not in seen and not seen.add(tuple(slp.values))}
        self.slps.append(new_slps)
        self.current_size += 1
