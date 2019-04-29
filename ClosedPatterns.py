'''
Finds closed subpatterns given a set of patterns and subpatterns.
Closed pattern is defined as the subpattern contained in a longer pattern whose frequency is larger than the pattern that contains it.
#Parameters
sequences= list of input sequences
patterns_file = txt file with maximum lenght patterns
subpatterns_file = txt file with smaller patterns
'''

class ClosedPatterns:

    def __init__(self, patterns_file, subpatterns_file):
        self.patterns = patterns_file
        self.subpatterns = subpatterns_file


    def execute(self):
        patterns, subpatterns = self.read_files()
        closed=[]
        index=[]
        filtered_patterns = [pa[0] for pa in patterns]
        k=-1
        for s in subpatterns:
            k+=1
            for p in patterns:
                if self.isSubpattern(p[0], s[0]) and s[1]>p[1]:
                    if s[0] not in closed and s[0] not in filtered_patterns:
                        closed.append(s[0])
                        index.append(k)
        return closed, index


    def read_files(self):
        p = open(self.patterns, "r")
        p = p.readlines()
        s = open(self.subpatterns, "r")
        s = s.readlines()
        pat = self.parse_patterns(p)
        sub = self.parse_patterns(s)
        return pat, sub


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
            out = out.replace ('[', '').replace (']', '').replace ("'", '').replace (',', ' ')
            out = out.split()
            patterns.append((out, int(el[el.find(']') + 1:].replace('\n',''))))
        return patterns