import argparse
import pandas as pd
import nltk
import csv
from nltk import sent_tokenize
from nltk import word_tokenize
nltk.download('punkt')
import gensim
from gensim.models import Word2Vec
import gensim.downloader as api
import jsontrips
import json
from numpy import dot
from numpy.linalg import norm
import math
import mat

# Measure 1: word2vec vectors
wv = api.load('word2vec-google-news-300')

# Measure 2:
ontology_dict = jsontrips.ontology()
file = open('lex-ont.json')
f = json.load(file)
def getParent(testWord):
    return f[testWord]['lf_parent']
def depth(initialNode):
    d = 1
    if initialNode == 'ROOT':
        d = 0
        return d
    if ontology_dict[initialNode]['parent'] != 'ROOT':
        d = depth(ontology_dict[initialNode]['parent'])+1
    return d
def getTree(initialNode):
    tree = [initialNode]
    if ontology_dict[initialNode]['parent'] != 'ROOT':
        tree += getTree(ontology_dict[initialNode]['parent'])
    else:
        tree.append('ROOT')
    return tree
def findCommon(word1, word2):
    word1 = word1.upper()
    word2 = word2.upper()
    commonParent = []
    # [CONTAINMENT, LODGING]
    start1 = getParent(word1)
    start2 = getParent(word2)
    # len(start1) = 2, r = 0, 1
    list1 = []
    list2 = []
    for r in range(len(start1)):
        list1.append(getTree(start1[r]))
    for i in range(len(start2)):
        list2.append(getTree(start2[i]))

    if start1 == start2:
        return start1
    if start1 != start2:
        for r in range(len(start1)):
            for i in range(len(list1[r])):
                for x in range(len(start2)):
                    for y in range(len(list2[x])):
                        if list1[r][i] == list2[x][y]:
                            commonParent.append(list1[r][i])
                            commonParent.append(r)
                            commonParent.append(x)
                            break
    return commonParent
# print(findCommon('DOG', 'HOUSE'))
def finalCommon(list1):
    length = len(list1)
    removeIndex = []
    finalList = []
    fullIndex = []
    for i in range(1, length, 3):
        for r in range(i+3, length, 3):
            fullIndex.append(r)
            if list1[i] == list1[r] and list1[i+1]==list1[r+1]:
                removeIndex.append(r)
    keepIndex = list(set(fullIndex) - set(removeIndex))
    finalList.append(list1[0])
    finalList.append(list1[1])
    finalList.append(list1[2])
    for i in range(len(keepIndex)):
        finalList.append(list1[keepIndex[i]-1])
        finalList.append(list1[keepIndex[i]])
        finalList.append(list1[keepIndex[i]+1])
    return finalList

def sim(commonNode, index1, index2, word1, word2):
    depthLCS = depth(commonNode)
    depth1 = depth(getParent(word1)[index1])
    depth2 = depth(getParent(word2)[index2])
    sim = 2*depthLCS/(depth1+depth2)
    return sim

def wuPalmerSimilarity(word1, word2):
    word1 = word1.upper()
    word2 = word2.upper()
    list1 = findCommon(word1, word2)
    list2 = finalCommon(list1)
    maxSim = 0.0
    for i in range(0, len(list2), 3):
        if sim(list2[i], list2[i+1], list2[i+2], word1, word2)>maxSim:
            maxSim = sim(list2[i], list2[i+1], list2[i+2], word1, word2)
    maxSim=round(maxSim, 3)
    return maxSim

# Measure 3: Cosine Similarity
sample = open('brown_lemmatized.txt')
s = sample.read()
file = s.replace('\n', ' ')
brownWord = file.split(' ')

with open('trips-brown_NV_overlap.txt', 'r') as file:
    wordString = file.read().replace('\n', ' ')
    overlapWordArray = wordString.split()

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
def getWindowWord(word):
    length = len(brownWord)
    wordInWindow = []
    vector = 0
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
# Measure 4: combination of other 3 measures
def measure4(word1, word2):
    measure1 = round(wv.similarity(word1, word2), 3)
    measure2 = wuPalmerSimilarity(word1, word2)
    measure3 = getCosSim(word1, word2)
    result = 2/5*measure1 + 2/5*measure2 + 1/5*measure3
    result = round(result, 3)
    return result

#inputList = [['word1', 'word2', 'word3'], ['dog', 'cat', 'house'], ['bottle', 'house', 'run'], ['drum', 'health', 'milk'], ['doc', 'queen', 'friend'], ['save', 'help', 'waste']]
# argparser
parser = argparse.ArgumentParser()
parser.add_argument('input', type= str, default = 'input.csv')
parser.add_argument('output', type= str, default = 'output.csv')
parser.add_argument('score', type= str, default = 'score.csv')

args = parser.parse_args()

# print(type(args.input))
# print(args.output)
# print(args.score)

# open input file
#[['word1', 'word2', 'word3'], ['dog', 'cat', 'house'], ['bottle', 'house', 'run'], ['drum', 'health', 'milk'], ['doc', 'queen', 'friend'], ['save', 'help', 'waste']]
def openFile(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        mylist = list(reader)
    # print(mylist)
    # print(mylist[1][0])
    return mylist

filename = str(args.input)
inputList = openFile(filename)
# print(inputList[1][0].upper())

# generate score file
scoreFilename = str(args.score)
headerScore = ['tripleid', 'word1', 'word2', 'word2vec-score', 'wu-palmer-score', 'brown-vector-score', 'your-novel-score']
dataScore = []
# len(inputList) = 6
rowNumber = len(inputList) -1
for i in range(rowNumber):
    word1 = inputList[i+1][0]
    word2 = inputList[i+1][1]
    word3 = inputList[i+1][2]
    # print(word1.upper())
    # print(word2.upper())
    # print(word3.upper())
    # 0 dog cat
    list1 = []
    list1.append(i)
    list1.append(word1)
    list1.append(word2)
    list1.append(round(wv.similarity(word1, word2), 3))
    list1.append(wuPalmerSimilarity(word1.upper(), word2.upper()))
    list1.append(getCosSim(word1, word2))
    list1.append(measure4(word1, word2))
    # print(list1)
    # 0 dog house
    list2 = []
    list2.append(i)
    list2.append(word1)
    list2.append(word3)
    list2.append(round(wv.similarity(word1, word3), 3))
    list2.append(wuPalmerSimilarity(word1.upper(), word3.upper()))
    list2.append(getCosSim(word1, word3))
    list2.append(measure4(word1, word3))
    # 0 cat house
    list3 = []
    list3.append(i)
    list3.append(word2)
    list3.append(word3)
    list3.append(round(wv.similarity(word2, word3), 3))
    list3.append(wuPalmerSimilarity(word2.upper(), word3.upper()))
    list3.append(getCosSim(word2, word3))
    list3.append(measure4(word2, word3))

    dataScore.append(list1)
    dataScore.append(list2)
    dataScore.append(list3)

tempData = dataScore
# # dataScore = [['word2_dogcat', 'wu12', 'brown12', 'madeup12'], ['word_bottlehouse', 'wubottle', 'brownbottle', 'madeupbottle']]
with open(scoreFilename, 'w', encoding = 'UTF8', newline = '') as s:
    writer = csv.writer(s)
    writer.writerow(headerScore)
    writer.writerows(dataScore)


# # generate output file
outputFilename = str(args.output)
headerOutput = ['word2vec-score-choice', 'wu-palmer-score-choice', 'brown-vector-score-choice', 'your-novel-score-choice']
# # dataOutput = [['word2_dogcat', 'wu12', 'brown12', 'madeup12'], ['word_bottlehouse', 'wubottle', 'brownbottle', 'madeupbottle']]
dataOutput = []
rowNumber = len(inputList) -1
for i in range(rowNumber):
    # dog cat house
    word1 = inputList[i+1][0]
    word2 = inputList[i+1][1]
    word3 = inputList[i+1][2]
    line = []
    word2vec12 = tempData[3*i][3]
    word2vec13 = tempData[3*i+1][3]
    word2vec23 = tempData[3*i+2][3]
    if word2vec12>word2vec13 and word2vec12>word2vec23:
        line.append(word3)
    elif word2vec13>word2vec23 and word2vec13>word2vec12:
        line.append(word2)
    else:
        line.append(word1)

    wuSim12 = tempData[3*i][4]
    wuSim13 = tempData[3*i+1][4]
    wuSim23 = tempData[3*i+2][4]
    if wuSim12>wuSim13 and wuSim12>wuSim23:
        line.append(word3)
    elif wuSim13>wuSim23 and wuSim13>wuSim12:
        line.append(word2)
    else:
        line.append(word1)

    vector12 = tempData[3*i][5]
    vector13 = tempData[3*i+1][5]
    vector23 = tempData[3*i+2][5]
    if vector12>vector13 and vector12>vector23:
        line.append(word3)
    elif vector13>vector23 and vector13>vector12:
        line.append(word2)
    else:
        line.append(word1)

    combination12 = tempData[3*i][6]
    combination13 = tempData[3*i+1][6]
    combination23 = tempData[3*i+2][6]
    if combination12>combination13 and combination12>combination23:
        line.append(word3)
    elif combination13>combination23 and combination13>combination12:
        line.append(word2)
    else:
        line.append(word1)

    dataOutput.append(line)


with open(outputFilename, 'w', encoding = 'UTF8', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(headerOutput)
    writer.writerows(dataOutput)


