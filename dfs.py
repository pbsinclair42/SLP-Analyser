import cProfile

class PosSLPAnalyser:

    def __init__(self):
        pass

    def get_all_next_slps(self, slp):
        # Given an mSLP slp, returns all mSLPs which can be created by adding a single line to slp
        # Does some clever things to avoid duplicates, see Section 3.2: Challenges for more information
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

    def _depth_limited_search(self, slp, depth):
        values = {slp[-1]}
        if depth>0:
            depth -= 1
            next_slps = self.get_all_next_slps(slp)
            for next_slp in next_slps:
                values.update(self._depth_limited_search(next_slp, depth))
        return values

    def depth_limited_search(self, depth):
        # Performs a depth limited traversal of the graph of all SLPs up to a maximum SLP size of depth
        values = {1}
        if depth>0:
            depth -= 1
            next_slps = self.get_all_next_slps((1,))
            for next_slp in next_slps:
                values.update(self._depth_limited_search(next_slp, depth))
        return values


class SLPAnalyser(PosSLPAnalyser):

    def get_all_next_slps(self, slp):
        # Given an SLP slp, returns all SLPs which can be created by adding a single line to slp
        # Does some clever things to avoid duplicates, see Section 3.2: Challenges for more information
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
    slpAnalyser = SLPAnalyser()
    mslpAnalyser = PosSLPAnalyser()

    SLP_MAX_SIZE = 1
    MSLP_MAX_SIZE= 1

    found = set()

    while True:
        mvalues = mslpAnalyser.depth_limited_search(MSLP_MAX_SIZE)
        values = slpAnalyser.depth_limited_search(SLP_MAX_SIZE)
        found.update(values-mvalues)
        print("Values that can be created by SLPs of length " + str(SLP_MAX_SIZE) +
              " but not mSLPs of length " + str(MSLP_MAX_SIZE) + ':')
        print(values - mvalues)
        print("Smallest value not computed by SLPs of length " + str(SLP_MAX_SIZE)+':')
        smallest_not_found=1
        while smallest_not_found in values:
            smallest_not_found+=1
        print(smallest_not_found)
        print("Sequence so far: ")
        print(sorted([v for v in found if v < smallest_not_found]))

        SLP_MAX_SIZE+=1
        MSLP_MAX_SIZE+=1       
