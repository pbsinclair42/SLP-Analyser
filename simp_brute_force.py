import time
import cProfile

class PosSLPAnalyser:

    def __init__(self):
        self.slps = [{(1,)}]
        self.values = {1}
        self.current_size = 1

    def get_all_next_slps(self, slp, l):
        all_next_slps = set()
        for i in range(l):
            for j in range(i, l):
                next_slps = set()
                if slp[i]+slp[j] > slp[-1]:
                    new = slp+(slp[i]+slp[j],)
                    all_next_slps.add(new)
                if slp[i]*slp[j] > slp[-1]:
                    new = slp+(slp[i]*slp[j],)
                    all_next_slps.add(new)
        return all_next_slps

    def calculate_next_values(self):
        new_slps = []
        l=self.current_size
        for slp in self.slps[-1]:
            next_slps = self.get_all_next_slps(slp, l)
            new_slps += next_slps
        new_values = {slp[-1] for slp in new_slps}
        self.values.update(new_values)
        self.slps.append(new_slps)
        self.current_size += 1

class SLPAnalyser(PosSLPAnalyser):

    def __init__(self):
        self.slps = [{(1,)}]
        self.values = {1}
        self.current_size = 1

    def get_all_next_slps(self, slp, l):
        all_next_slps = set()
        for i in range(l):
            for j in range(l):
                next_slps = set()
                if slp[i]+slp[j] not in slp:
                    new = slp+(slp[i]+slp[j],)
                    all_next_slps.add(new)
                if slp[i]+slp[j] not in slp:
                    new = slp+(slp[i]*slp[j],)
                    all_next_slps.add(new)
                if slp[i]-slp[j] > 0 and slp[i]-slp[j] not in slp:
                    new = slp+(slp[i]-slp[j],)
                    all_next_slps.add(new)
        return all_next_slps


if __name__ == '__main__':
    SLP_MAX_SIZE = 7
    MSLP_MAX_SIZE = 10

    slpAnalyser = SLPAnalyser()
    mslpAnalyser = PosSLPAnalyser()

    start_time = time.time()

    def do_the_stuff():
        for _ in range(MSLP_MAX_SIZE - 1):
            mslpAnalyser.calculate_next_values()
            print('MSLP size ' + str(mslpAnalyser.current_size) + ' complete')
        for _ in range(SLP_MAX_SIZE - 1):
            slpAnalyser.calculate_next_values()
            print('SLP size ' + str(slpAnalyser.current_size) + ' complete')
    #cProfile.run("do_the_stuff()")

    do_the_stuff()
    end_time = time.time()
    total_time = end_time - start_time

    print(total_time)
    print(slpAnalyser.values - mslpAnalyser.values)