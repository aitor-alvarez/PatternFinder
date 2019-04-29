from pygapbide import Gapbide
import ShowPatterns
from ClosedPatterns import ClosedPatterns
from music21 import *


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


def get_durations_all(file, full=0):
    durations = []
    all = []
    for n in range(0, len(file)):
        if file[n].isStream:
            for e in range(0, len(file[n].elements)):
                if file[n].elements[e].isStream:
                    for f in range(0, len(file[n].elements[e])):
                        if type(file[n].elements[e][f]).__name__=='Note':
                            try:
                                if float(file[n].elements[e][f].beat).is_integer():
                                    if full ==1:
                                        all.append(str(float(file[n].elements[e][f].duration.quarterLength))+'-'+file[n].elements[e][f].pitch.__str__())
                                    else:
                                        durations.append(str(float(file[n].elements[e][f].duration.quarterLength)))

                                else:
                                    if full == 1:
                                        all.append(str(float(file[n].elements[e][f].duration.quarterLength))+'-'+file[n].elements[e][f].pitch.__str__())
                                    else:
                                        durations.append(str(float(file[n].elements[e][f].duration.quarterLength)))
                            except:
                                if full == 1:
                                    all.append(str(float(file[n].elements[e][f].duration.quarterLength)) +
                                                file[n].elements[e][f].pitch.__str__())
                                else:
                                    durations.append( str(float(file[n].elements[e][f].duration.quarterLength)))

                        elif type(file[n].elements[e][f]).__name__=='Rest':
                            try:
                                if float(file[n].elements[e][f].beat).is_integer():
                                    if full == 1:
                                        all.append(str(float(file[n].elements[e][f].duration.quarterLength)))
                                    else:
                                        durations.append(str(float(file[n].elements[e][f].duration.quarterLength)))
                                else:
                                    if full == 1:
                                        all.append(str(float(file[n].elements[e][f].duration.quarterLength)))
                                    else:
                                        durations.append( str(float(file[n].elements[e][f].duration.quarterLength)))
                            except:
                                if full == 1:
                                    all.append(str(float(file[n].elements[e][f].duration.quarterLength)))
                                else:
                                    durations.append( str(float(file[n].elements[e][f].duration.quarterLength)))
    if full == 1:
        return all
    elif full == 0:
        return durations


def write_patterns(index, file1, file2):
    f1 = open(file1, "r")
    f1 = f1.readlines()
    f2 = open(file2, "r")
    f2 = f2.readlines()
    file_1 = open("output/closed_int.txt", 'a')
    file_2 = open("output/closed_int_patterns.txt", 'a')
    for i in index:
        file_1.write(f1[i])
        file_2.write(f2[i])
    file_1.close()
    file_2.close()

def filter_intervals(patterns_file):
    p = open(patterns_file, "r")
    p = p.readlines()
    for pat in p:
        


if __name__ == '__main__':
    intervals_file = 'interval_patterns'
    min_intervals = 'min_intervals'
    seq = parse_midi_file("obras/misa_quarti_toni_v.mid")
    inter = [get_intervals(s) for s in seq]
    g1 = Gapbide(inter, 2, 0, 0, 6, intervals_file)
    g2 = Gapbide(inter, 2, 0, 0, 3, min_intervals)
    g1.run()
    g2.run()
    closed_patterns = ClosedPatterns(intervals_file+'_intervals.txt', min_intervals+'_intervals.txt')
    closed, index = closed_patterns.execute()
    write_patterns(index, min_intervals + '_intervals.txt', min_intervals+'.txt')
    patterns = ShowPatterns.read('interval_patterns.txt')
    ShowPatterns.findPatternColor(converter.parse("obras/misa_quarti_toni_v.mid"), patterns)
