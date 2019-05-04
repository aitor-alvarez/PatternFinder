from pygapbide import Gapbide
import random
from ClosedPatterns import ClosedPatterns
from music21 import *
import statistics


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


def filter_patterns(patterns, index):
    length = [len(p) for p in patterns]
    mean_length = statistics.mean(length)
    out_pat=[]
    out_ind=[]
    for num, elem in enumerate(patterns):
        if len(elem)>=mean_length:
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


def show_patterns_in_score(score, patterns):
    sequences = parse_midi_file(score)
    index = 0
    for patternLine in patterns:
        index += 1
        color = "#%06x" % random.randint (0, 0xFFFFFF)
        for pattern in patternLine:
            indexPhrase = pattern[0]
            startPosition = pattern[1]
            endPosition = pattern[2]
            notes = sequences[indexPhrase]
            startPosition = startPosition - 1
            if startPosition < 0:
                startPosition = 0
            for i in range (startPosition, endPosition + 1):
                notes[i].style.color = color
                notes[i].addLyric (index)

    score.show ()


def get_similar_sequences(patterns, candidates, durations=False):
    output_patterns=[]
    if durations == False:
        for c, num in enumerate(candidates):
            for p, numb in enumerate(patterns):
                if len(c)==len(p):
                    dif_direction = [1 for i, j in zip(c, p) if i[-1] != j[-1]]
                    dif_interval = [abs(int(i[:-1])-int(j[:-1])) for i, j in zip(c, p) if i[:-1] != j[:-1]]
                    if sum (dif_direction)==0:
                        if sum(dif_interval)==0:
                            continue
                        elif len(dif_interval)/len(p)<=0.5:
                            continue
                        elif 0.5<(len (dif_interval) / len (p))<0.8:
                            output_patterns.append((c, num, p, numb, 'i1'))
                        elif len(dif_interval) / len (p) >= 0.8:
                            output_patterns.append ((c, num, p, numb, 'i2'))
                    if sum (dif_direction) / len (p) > 0.8:
                        if sum(dif_interval)>0.8:
                            output_patterns.append ((c, num, p, numb, 'i3'))
                    elif 0.5<(sum(dif_direction) / len (p))<0.8:
                        if len(dif_interval) / len (p) <= 0.5:
                            continue
                        elif 0.5 < (len (dif_interval) / len (p)) < 0.8:
                            output_patterns.append((c, num, p, numb, 'i4'))
                        elif len(dif_interval) / len (p) >= 0.8:
                            output_patterns.append((c, num, p, numb, 'i5'))
                if len(c) != len(p) and (ClosedPatterns.isSubpattern(0, p, c) or ClosedPatterns.isSubpattern(0, c, p)):
                    if len(p)>len(c):
                        diff = [i for i in p if not i in c]
                        dist = len(diff)/len(p)
                        if dist <= 0.5:
                            continue
                        elif dist > 0.5:
                            output_patterns.append ((c, num, p, numb, 'i6'))
                    elif len(c)>len(p):
                        diff = [i for i in c if not i in p]
                        dist = len (diff) / len (c)
                        if dist <= 0.5:
                            continue
                        elif dist > 0.5:
                            output_patterns.append ((c, num, p, numb, 'i6'))
    if durations == True:
        for c, num in enumerate(candidates):
            for p, numb in enumerate(patterns):
                if len(c)==len(p):
                    dif_duration = [1 for i, j in zip(c, p) if i != j]
                    if sum (dif_duration)==0:
                        continue
                    elif len(dif_duration)/len(p)<=0.5:
                        continue
                    elif (len (dif_duration) / len (p))>0.5:
                            output_patterns.append((c, num, p, numb, 'd1'))

                if len(c) != len(p) and (ClosedPatterns.isSubpattern(0, p, c) or ClosedPatterns.isSubpattern(0, c, p)):
                    if len(p)>len(c):
                        diff = [i for i in p if not i in c]
                        dist = len(diff)/len(p)
                        if dist <= 0.5:
                            continue
                        elif dist > 0.5:
                            output_patterns.append ((c, num, p, numb, 'd2'))
                    elif len(c)>len(p):
                        diff = [i for i in c if not i in p]
                        dist = len (diff) / len (c)
                        if dist <= 0.5:
                            continue
                        elif dist > 0.5:
                            output_patterns.append ((c, num, p, numb, 'd2'))
    return output_patterns



if __name__ == '__main__':
    pattern_length = 4
    intervals_file = 'interval_patterns'
    seq = parse_midi_file("obras/misa_quarti_toni_v.mid")
    inter = [get_intervals(s) for s in seq]
    durations = [get_durations(s) for s in seq]
    g1 = Gapbide(inter, 2, 0, 0, pattern_length, intervals_file)
    g1.run()
    closed_patterns = ClosedPatterns(intervals_file+'_intervals.txt', pattern_length+2)
    closed, index, maximal, max_index, minimal, minimal_index = closed_patterns.execute()
    closed, index = filter_patterns(closed, index)
    maximal, max_index = filter_patterns(maximal, max_index)
    write_patterns(index, intervals_file + '_intervals.txt',intervals_file+'.txt', "output/closed_int.txt", "output/closed_int_patterns.txt")
    write_patterns (max_index, intervals_file + '_intervals.txt', intervals_file + '.txt', "output/maximal_int.txt", "output/maximal_int_patterns.txt")
    patterns = read_patterns('interval_patterns.txt')
    show_patterns_in_score("obras/misa_quarti_toni_v.mid", patterns)