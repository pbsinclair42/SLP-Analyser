import time
import cProfile


class mSLPAnalyser:
    def __init__(self):
        # Note that an SLP is saved as tuple of integers
        # Once computed, self.slps[i] contains all SLPs of length i
        self.slps = [[(1,)]]
        # All the values of any slps constructed so far
        self.values = {1}
        # The current maximum size of SLP we have investigated
        self.current_size = 0

    def get_all_next_slps(self, slp, l):
        # Given an mSLP slp of length l, returns all SLPs which can be created by adding a single line to slp
        # Does some clever things to avoid duplicates, see Section 3.2: Challenges for more information
        all_next_slps = set()
        for i in range(l):
            for j in range(i, l):
                if slp[i] + slp[j] > slp[-1]:
                    new = slp + (slp[i] + slp[j],)
                    all_next_slps.add(new)
                if slp[i] * slp[j] > slp[-1]:
                    new = slp + (slp[i] * slp[j],)
                    all_next_slps.add(new)
        return all_next_slps

    def calculate_next_values(self):
        new_slps = []
        l = self.current_size + 1
        for slp in self.slps[-1]:
            next_slps = self.get_all_next_slps(slp, l)
            new_slps += next_slps
        new_values = {slp[-1] for slp in new_slps}
        self.values.update(new_values)
        self.slps.append(new_slps)
        self.current_size += 1

    def breadth_first_traversal(self, max_depth):
        for _ in range(max_depth):
            self.calculate_next_values()
            print(('' if isinstance(self, SLPAnalyser) else 'm') + 'SLP size ' + str(self.current_size) + ' complete')
        return self.values


class SLPAnalyser(mSLPAnalyser):
    def get_all_next_slps(self, slp, l):
        all_next_slps = set()
        for i in range(l):
            for j in range(i, l):
                if slp[i] + slp[j] not in slp:
                    new = slp + (slp[i] + slp[j],)
                    all_next_slps.add(new)
                if slp[i] + slp[j] not in slp:
                    new = slp + (slp[i] * slp[j],)
                    all_next_slps.add(new)
            for j in range(l):
                if slp[i] - slp[j] > 0 and slp[i] - slp[j] not in slp:
                    new = slp + (slp[i] - slp[j],)
                    all_next_slps.add(new)
        return all_next_slps


if __name__ == '__main__':
    SLP_MAX_SIZE = 6
    MSLP_MAX_SIZE = 7

    slpAnalyser = SLPAnalyser()
    mslpAnalyser = mSLPAnalyser()

    start_time = time.time()

    def do_the_stuff():
        mslpAnalyser.breadth_first_traversal(MSLP_MAX_SIZE)
        slpAnalyser.breadth_first_traversal(SLP_MAX_SIZE)
        print(slpAnalyser.values - mslpAnalyser.values)

    cProfile.run("do_the_stuff()")

    # do_the_stuff()
    end_time = time.time()
    total_time = end_time - start_time
    # print[slp for slp in mslpAnalyser.slps[-1] if slp[-1]==4088]
    # print(total_time)
    # print({v for v in slpAnalyser.values if v>0} - mslpAnalyser.values)
    # print(mslpAnalyser.slps)

    # def allpos(slp):
    #    for i in slp:
    #        if i<0:
    #            return False
    #    return True
    # weird=({slp for slp in slpAnalyser.slps[-1] if slp[-1]>0 and not allpos(slp)})
    # posvals=({slp[-1] for slp in slpAnalyser.slps[-1] if slp[-1]>0 and allpos(slp)})
    # print({slp for slp in weird if slp[-1] not in posvals})
    # print(len({slp for slp in slpAnalyser.slps[-1] if slp[-1]>0}))
