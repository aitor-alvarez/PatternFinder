'''
Created on 17 Jun 2015

@author: victor
'''
import ViewPoints
from music21 import voiceLeading

import random
import copy

def read(filename):
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


        

def findPatternColor(score,patterns):
    phrases=ViewPoints.getPhrases(score)
    index=0
    for patternLine in patterns:
        index+=1
        color = "#%06x" % random.randint(0,0xFFFFFF)
        for pattern in patternLine:
            indexPhrase=pattern[0]
            startPosition=pattern[1]
            endPosition=pattern[2]
            notes=phrases[indexPhrase]
            startPosition=startPosition-1
            if startPosition<0:
                startPosition=0
            for i in range(startPosition,endPosition+1):
  
                notes[i].style.color = color   
                notes[i].addLyric(index)
 

    score.show()
        