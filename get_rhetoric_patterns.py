from itertools import zip_longest, combinations
import music21.interval as interval
from get_patterns import parse_midi_file, show_patterns_in_score, read_patterns
from music21 import converter


def parse_intervals(p):
    patterns = []
    for el in p:
        out = el[:el.find(']') + 1]
        out = out.replace('[', '').replace(']', '').replace("'", '').replace(',', ' ')
        out = out.split()
        patterns.append((out, int(el[el.find(']') + 1:].replace('\n', ''))))
    return patterns


def parse_patterns(pats):
    patts=[]
    for p in pats:
        pat=p.replace("(", '').replace(")", "").replace(",","").replace('\n',"")
        pat= pat.split()
        pat=grouper(pat, 3)
        patts.append(list(pat))
    return patts


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def check_rhet(pats, seqs):
    rhet_pat=[]
    for num, p in enumerate(pats):
        notes=[]
        inds=[]
        rhet = []
        for k in p:
            lista=seqs[int(k[0])]
            notes.append(lista[int(k[1])])
            inds.append((int(k[0]),int(k[1]), int(k[2])))
            print(inds)
            print(k)
        dis = inds[0][1]-inds[0][2]
        for a, b in combinations(enumerate(inds), 2):
            inter = interval.notesToGeneric(notes[a[0]], notes[b[0]])
            if a[1][0] == b[1][0]:
                if (inter.directed == 1 or abs(inter.directed) == 8) and (a[1][2]-b[1][1]<16 and a[1][2]-b[1][1]>=dis):
                    rhet.append((num, a[0], b[0], 'pal'))
                elif a[1][2]-b[1][1]<16 and (inter.directed != 1 or abs(inter.directed) != 8) and a[1][2]-b[1][1]>=dis:
                    rhet.append((num, a[0], b[0], 'sin'))
            else:
                if (inter.directed == 1 or abs(inter.directed) == 8) and (a[1][2]-b[1][1]>=0 and a[1][2]-b[1][1]<8):
                    rhet.append((num, a[0], b[0], 'pol'))
                elif a[1][2]-b[1][1]<=-1 and a[1][2]-b[1][1]>=dis:
                    rhet.append((num, a[0], b[0], 'epi'))
        if rhet !=[]:
            rhet_pat.append(rhet)
    return rhet_pat


def write_rhetoric(rhets, pats, output_file, labels_file):
    output = open(output_file, 'w')
    labels = open(labels_file, 'w')
    for r in rhets:
        print(r[0][0])
        line=pats[r[0][0]]
        print(line)
        output.write(str(line[r[0][1]]))
        output.write(",")
        output.write(str(line[r[0][2]]))
        output.write("\n")
        labels.write(str(r[0][3]))
        labels.write("\n")


def get_rhet(pat_file='./output/closed_patterns.txt'):
    all_seq, seq = parse_midi_file('obras/veni_sponsa_christe.mid')
    pats = open(pat_file, "r")
    pats = pats.readlines()
    pats = parse_patterns(pats)
    seqs = [sum(s, []) for s in seq]
    rhet_patterns = check_rhet(pats, seqs)
    write_rhetoric(rhet_patterns, pats, 'output/rhetoric/rhetoric_patterns.txt', 'output/rhetoric/rhetoric_labels.txt')

    patterns2 = read_patterns('output/closed_patterns.txt')
    patterns = read_patterns('output/rhetoric/rhetoric_patterns.txt')
    obra = converter.parse('obras/veni_sponsa_christe.mid')
    show_patterns_in_score(obra, patterns)

