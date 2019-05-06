'''
Finds closed subpatterns given a set of patterns and Maximal patterns.
Closed pattern is defined as the subpattern contained in a longer pattern whose frequency is larger than the pattern that contains it
#Parameters
sequences= list of input sequences
patterns_file = txt file with maximum lenght patterns
The output of this class is the set of closed, maximal and minimal patterns and their indices. A minimal pattern is any sequence that is not a maximal or closed pattern.
'''

class ClosedPatterns:

    def __init__(self, patterns_file, pattern_len):
        self.patterns = patterns_file
        self.pattern_len = pattern_len


    def execute(self):
        patterns = self.read_files()
        closed=[]
        maximal=[]
        index=[]
        max_index=[]
        minimal=[]
        minimal_index=[]
        blocked=[]
        for i in range (0, len(patterns)):
            for k in range (0, len(patterns)):
                if k == i:
                    continue
                else:
                    if self.isSubpattern(patterns[k][0], patterns[i][0]) and patterns[i][1]>1 and patterns[i][1]>patterns[k][1]:
                        if patterns[i][0] not in closed and patterns[i][0] not in maximal:
                            closed.append(patterns[i][0])
                            index.append(i)
                    elif self.isSubpattern(patterns[k][0], patterns[i][0]) and patterns[i][1]>1 and patterns[i][1]<=patterns[k][1] and patterns[i][0] in closed:
                        ind = closed.index(patterns[i][0])
                        closed.remove(patterns[i][0])
                        index.pop(ind)
                        blocked.append(patterns[i][0])
                    elif not self.isSubpattern(patterns[k][0], patterns[i][0]) and patterns[i][1]>1 and patterns[i][0] not in maximal and patterns[i][0] not in closed and len(patterns[i][0])>self.pattern_len:
                        maximal.append(patterns[i][0])
                        max_index.append(i)
                    elif not self.isSubpattern(patterns[k][0], patterns[i][0]) and patterns[i][1]==1 and patterns[i][0] not in maximal and patterns[i][0] not in closed and patterns[i][0] not in minimal:
                        minimal.append(patterns[i][0])
                        minimal_index.append(i)
        return closed, index, maximal, max_index, minimal, minimal_index


    def read_files(self):
        p = open(self.patterns, "r")
        p = p.readlines()
        pat = self.parse_patterns(p)
        return pat


    def isSubpattern(self, pattern, sub):
        if len(sub) >= len(pattern):
            return False
        for i in range (0, len (pattern) - len (sub) + 1):
            if pattern[i:i + len (sub)] == sub:
                return True
        return False


    def parse_patterns(self, p):
        patterns = []
        for el in p:
            out = el[:el.find (']') + 1]
            out = out.replace ('[', '').replace(']', '').replace("'", '').replace(',', ' ')
            out = out.split()
            patterns.append((out, int(el[el.find(']') + 1:].replace('\n',''))))
        return patterns