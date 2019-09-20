from pygapbide import Gapbide
from ClosedPatterns import ClosedPatterns
from music21 import *
from music21 import converter
from dtwpy import dtw
import pandas as pd
from itertools import product
from copy import deepcopy
import sys

def parse_midi_file(file):
    midi_file = converter.parse(file)
    phrases = []
    for part in midi_file.getElementsByClass(stream.Part):
        partFlat = part.flat
        notesandrests = partFlat.notesAndRests
        myPhrase = []
        countElement = 0
        for element in notesandrests:
            countElement += 1
            if isinstance(element, note.Note):
                myPhrase.append(element)
            else:
                if (len(myPhrase) > 0):
                    phrases.append(myPhrase)
                myPhrase = []

            if countElement == len(notesandrests):
                phrases.append(myPhrase)
                myPhrase = []

    return phrases


def get_intervals(notes):
    intervals=[]
    for n in range(0, len(notes)-1):
        if notes[n].isNote and notes[n+1].isNote:
            dist = interval.notesToChromatic(notes[n], notes[n+1])
            if dist.directed>0:
                interstring = str(dist.directed)+'1'
                intervals.append(interstring)
            else:
                interstring = str(abs(dist.directed))+'0'
                intervals.append(interstring)
    return intervals


def get_durations(seq):
    durations = []
    for sq in seq:
        durations.append(sq.duration.quarterLength)
    return durations


def write_patterns(index, file1, file2, output_file1, output_file2):
    f1 = open(file1, "r")
    f1 = f1.readlines()
    f2 = open(file2, "r")
    f2 = f2.readlines()
    file_1 = open(output_file1, 'w')
    file_2 = open(output_file2, 'w')
    for i in index:
        file_1.write(f1[i])
        file_2.write(f2[i])
    file_1.close()
    file_2.close()


def filter_patterns(patterns, index, length):
    out_pat=[]
    out_ind=[]
    for num, elem in enumerate(patterns):
        if len(elem)>=length:
            out_pat.append(patterns[num])
            out_ind.append(index[num])
    return out_pat, out_ind


def read_patterns(filename):
    patterns = []
    with open(filename, 'r') as input:
        for line in input.readlines():
            elements = line.split('), (')
            S = []
            for e in elements:
                elementList=e.split(',')
                s=[]
                for element in elementList:
                    element=element.replace('(','')
                    element=element.replace(')','')
                    s.append(int(element))
                S.append(s)
            patterns.append(S)
    return patterns


def getPhrases(piece):
    phrases = []
    for part in piece.getElementsByClass(stream.Part):
        partFlat = part.flat
        notesandrests = partFlat.notesAndRests
        myPhrase = []
        countElement = 0
        for element in notesandrests:
            countElement += 1
            if isinstance(element, note.Note):
                myPhrase.append(element)
            else:
                if (len(myPhrase) > 0):
                    phrases.append(myPhrase)
                myPhrase = []

            if countElement == len(notesandrests):
                phrases.append(myPhrase)
                myPhrase = []

    return phrases


def show_patterns_in_score(score, patterns):
    sequences = getPhrases(score)
    index = 0
    for patternLine in patterns:
        index += 1
        for pattern in patternLine:
            indexPhrase = pattern[0]
            startPosition = pattern[1]
            endPosition = pattern[2]
            notes = sequences[indexPhrase]
            startPosition = startPosition - 1
            if startPosition < 0:
                startPosition = 0
            for i in range (startPosition, endPosition + 1):
                notes[i].addLyric (index)

    score.show ()


def get_similar_sequences(patterns, candidates):
    output_patterns=[]
    patt=[]
    for num, c in enumerate(candidates):
        for numb, p in enumerate(patterns):
            if len(c) == len(p):
                dif = [1 for i, j in zip(c, p) if i != j]
                if sum(dif) == 0:
                    continue
                elif len(dif) / len(p) >= 0.5:
                    continue
                elif 0.5 > (len(dif) / len(p)) > 0.2 and c not in patt and c not in p:
                    output_patterns.append((c, num, p, numb, 'p1'))
                    patt.append(c)
                elif len(dif) / len(p) <= 0.2 and c not in patt and c not in p:
                    output_patterns.append((c, num, p, numb, 'p2'))
                    patt.append(c)
            elif len(c) != len(p):
                dif = [1 for i, j in zip(c, p) if i != j]
                if sum(dif) == 0:
                    continue
                elif len(dif) / len(p) >= 0.5:
                    continue
                elif len(dif) / len(p) <= 0.2 and c not in patt and c not in p:
                    output_patterns.append((c, num, p, numb, 'p4'))
                    patt.append(c)

    return output_patterns


def dtw_matrix_similarity(data):
    output_dtw=[]
    for ind1, d1 in enumerate(data):
        for ind2, d2 in enumerate(data):
            output_dtw.append((ind1, ind2, dtw(d1, d2)))
    return output_dtw


def filter_subpatterns(list1, indx):
    pat1= deepcopy(list1)
    pat_ind = deepcopy(indx)
    for p in product(pat1, repeat=2):
        if ClosedPatterns.isSubpattern(None, p[0], p[1]) and p[1] in pat1:
            ind = pat1.index(p[1])
            pat1.remove(p[1])
            pat_ind.pop(ind)
        elif ClosedPatterns.isSubpattern(None, p[1], p[0]) and p[0] in pat1:
            ind = pat1.index(p[0])
            pat1.remove(p[0])
            pat_ind.pop(ind)
    return pat1, pat_ind


if __name__ == '__main__':
    pattern_length = 4
    intervals_file = 'interval_patterns'
    #midi file
    seq = parse_midi_file(sys.argv[1])
    inter = [get_intervals(s) for s in seq]
    intervals = [[i[0] for i in it] for it in inter]
    contours = [[i[1] for i in it] for it in inter]
    durations = [get_durations(s) for s in seq]
    g1 = Gapbide(inter, 1, 0, 0, pattern_length, intervals_file)
    g1.run()
    closed_patterns = ClosedPatterns(intervals_file+'_intervals.txt', pattern_length+2)
    closed, index, maximal, max_index, minimal, minimal_index = closed_patterns.execute()
    maximal, max_index = filter_subpatterns(maximal, max_index)
    minimal, minimal_index = filter_subpatterns(minimal, minimal_index)
    closed, index = filter_subpatterns(closed, index)
    similar = get_similar_sequences(maximal, minimal)
    similar_ind = list(set([s[1] for s in similar]))
    similar_ind = [s for s in similar_ind if s not in max_index]
    dtw_sim =[(dtw(s[0], s[2]), s[1], s[3]) for s in similar]
    pairs_sim=[d for d in dtw_sim if d[0]<=90]
    candidates_id =[minimal_index[p[2]] for p in pairs_sim]
    mat = pd.DataFrame(dtw_matrix_similarity(maximal))
    mat.columns = ['index1', 'index2', 'dtw']
    #print to excel
    mat.to_excel("max_patterns.xlsx")
    filtered_pat, pat_ind = filter_patterns(maximal, max_index, 10)
    write_patterns (max_index, intervals_file + '_intervals.txt', intervals_file + '.txt', "output/maximal.txt", "output/maximal_patterns.txt")
    write_patterns(minimal_index, intervals_file + '_intervals.txt', intervals_file + '.txt', "output/minimal.txt",
                   "output/minimal_patterns.txt")
    write_patterns(index, intervals_file + '_intervals.txt', intervals_file + '.txt', "output/closed.txt",
                   "output/closed_patterns.txt")
    #Read patterns and show in score
    #patterns = read_patterns('output/maximal_patterns.txt')
    #patterns_similar = read_patterns('output/similar_int_patterns.txt')
    #obra = converter.parse(sys.argv[1])
    #show_patterns_in_score(obra, patterns)
    #Printing pairs of patterns