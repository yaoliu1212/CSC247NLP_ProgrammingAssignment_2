import nltk
import nltk.data
from numpy import dot
from numpy.linalg import norm
import numpy as np


import math
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import brown


sample = open('brown_lemmatized.txt')
s = sample.read()
file = s.replace('\n', ' ')

brownWord = file.split(' ')


with open('trips-brown_NV_overlap.txt', 'r') as file:
    wordString = file.read().replace('\n', ' ')
    overlapWordArray = wordString.split()
# print(overlapWordArray[0])
# print(overlapWordArray[1])
# print(len(overlapWordArray))
#
# listTest = []
def getVector(overlapList, wordInWindow):
    vector = []
    length = len(overlapList)
    for i in range(length):
        vector.append(0)
    # print(len(vector))
    for i in range(length):
        for r in range(len(wordInWindow)):
            if overlapList[i] == wordInWindow[r]:
                vector[i] = vector[i]+1
    # print(len(vector))
    return vector

# getVector(overlapWordArray, listTest)

def getWindowWord(word):
    length = len(brownWord)
    wordInWindow = []
    dogNumber = 0
    for x in range(0, 4):
        if brownWord[x] == word:
            for y in range(0, x):
                wordInWindow.append(brownWord[y])
            for z in range(x+1, x+5):
                wordInWindow.append(brownWord[z])

    for i in range(4, length-4):
        if brownWord[i] == word:
            for a in range(i-4, i):
                wordInWindow.append(brownWord[a])
            for b in range(i+1, i+5):
                wordInWindow.append(brownWord[b])

    for x in range(length-5, length):
        if brownWord[x] == word:
            for y in range(x-4, x):
                wordInWindow.append(brownWord[y])
            for z in range(x+1, length):
                wordInWindow.append(brownWord[z])

    return wordInWindow

def calculateCosine(vector1, vector2):
    cos_sim = dot(vector1, vector2)/(norm(vector1)*norm(vector2))
    return cos_sim

def getCosSim(word1, word2):
    wordInWindow1 = getWindowWord(word1)
    vector1 = getVector(overlapWordArray, wordInWindow1)
    wordInWindow2 = getWindowWord(word2)
    vector2 = getVector(overlapWordArray, wordInWindow2)
    cosSim = calculateCosine(vector1, vector2)
    cosSim = round(cosSim, 3)
    return cosSim

print(getCosSim('dog', 'cat'))
print(getCosSim('dog', 'house'))
print(getCosSim('cat', 'house'))

print(getCosSim('bottle', 'house'))
print(getCosSim('bottle', 'run'))
print(getCosSim('house', 'run'))

print(getCosSim('drum', 'health'))
print(getCosSim('drum', 'milk'))
print(getCosSim('health', 'milk'))

print(getCosSim('doc', 'queen'))
print(getCosSim('doc', 'friend'))
print(getCosSim('queen', 'friend'))

print(getCosSim('save', 'help'))
print(getCosSim('save', 'waste'))
print(getCosSim('help', 'waste'))
