import time
import cProfile

class PosSLPAnalyser:

    def __init__(self):
        self.slps = [[(1,)]]
        self.values = {1}
        self.current_size = 0

    def get_all_next_slps(self, slp):
        all_next_slps = set()
        l=len(slp)
        for i in range(l):
            for j in range(i, l):
                if slp[i]+slp[j] > slp[-1]:
                    new = slp+(slp[i]+slp[j],)
                    all_next_slps.add(new)
                if slp[i]*slp[j] > slp[-1]:
                    new = slp+(slp[i]*slp[j],)
                    all_next_slps.add(new)
        return all_next_slps

    def depth_limited_search(self, slp, depth):
        values = {slp[-1]}
        if depth>0:
            depth -= 1
            next_slps = self.get_all_next_slps(slp)
            for slp in next_slps:
                values.update(self.depth_limited_search(slp, depth))
        return values

    def calculate_next_values(self):
        new_slps = []
        l=self.current_size
        for slp in self.slps[-1]:
            next_slps = self.get_all_next_slps(slp)
            new_slps += next_slps
        new_values = {slp[-1] for slp in new_slps}
        self.values.update(new_values)
        self.slps.append(new_slps)
        self.current_size += 1

class SLPAnalyser(PosSLPAnalyser):

    def get_all_next_slps(self, slp):
        all_next_slps = []
        l=len(slp)
        for i in range(l):
            for j in range(l):
                if slp[i]+slp[j] not in slp:
                    new = slp+(slp[i]+slp[j],)
                    all_next_slps.append(new)
                if slp[i]+slp[j] not in slp:
                    new = slp+(slp[i]*slp[j],)
                    all_next_slps.append(new)
                if slp[i]-slp[j] > 0 and slp[i]-slp[j] not in slp:
                    new = slp+(slp[i]-slp[j],)
                    all_next_slps.append(new)
        return all_next_slps


if __name__ == '__main__':
    SLP_MAX_SIZE = 6
    MSLP_MAX_SIZE = 7

    slpAnalyser = SLPAnalyser()
    mslpAnalyser = PosSLPAnalyser()

    start_time = time.time()

    def do_the_stuff():
        for _ in range(MSLP_MAX_SIZE):
            mslpAnalyser.calculate_next_values()
            print('MSLP size ' + str(mslpAnalyser.current_size) + ' complete')
        for _ in range(SLP_MAX_SIZE):
            slpAnalyser.calculate_next_values()
            print('SLP size ' + str(slpAnalyser.current_size) + ' complete')
    #cProfile.run("do_the_stuff()")
    
    #do_the_stuff()
    end_time = time.time()
    total_time = end_time - start_time
    #print(len(slpAnalyser.slps[-1]))
    #print[slp for slp in mslpAnalyser.slps[-1] if slp[-1]==4088]
    #print(total_time)
    #print(mslpAnalyser.values)
    
    start_time = time.time()

    values = mslpAnalyser.depth_limited_search((1,), MSLP_MAX_SIZE)
    end_time = time.time()
    total_time = end_time - start_time
    print(total_time)

    #print(mslpAnalyser.slps)
