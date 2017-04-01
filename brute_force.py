from slp import SLP, mSLP
from utils import Line
import time
import cProfile


class Analyser:
    def __init__(self, monotone=False):
        self.slps = [{mSLP(minimized=False) if monotone else SLP(minimized=False)}]
        self.values = {1}
        self.current_size = 0
        self.monotone = monotone

    def get_all_next_slps(self, slp):
        all_next_slps = set()
        for i in range(len(slp)):
            for j in range(len(slp)):
                next_slps = [slp.deepcopy() for _ in range(2 if self.monotone else 3)]
                next_slps[0].add(Line(i, j, '*'))
                next_slps[1].add(Line(i, j, '+'))
                if not self.monotone:
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

    def breadth_first_traversal(self, max_depth):
        for _ in range(max_depth):
            self.calculate_next_values()
            print(('m' if self.monotone else '') + 'SLP size ' + str(self.current_size) + ' complete')
        return self.values


if __name__ == '__main__':
    SLP_MAX_SIZE = 5
    MSLP_MAX_SIZE = 5

    slpAnalyser = Analyser()
    mslpAnalyser = Analyser(monotone=True)

    start_time = time.time()

    def do_the_stuff():
        mslpAnalyser.breadth_first_traversal(MSLP_MAX_SIZE)
        slpAnalyser.breadth_first_traversal(MSLP_MAX_SIZE)
        print(slpAnalyser.values - mslpAnalyser.values)

    cProfile.run("do_the_stuff()")

    # do_the_stuff()
    end_time = time.time()
    total_time = end_time - start_time
    # print[slp for slp in mslpAnalyser.slps[-1] if slp[-1]==4088]
    # print(total_time)
    # print({v for v in slpAnalyser.values if v>0} - mslpAnalyser.values)
    # print(mslpAnalyser.slps)
