import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
import gensim
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser
import gensim.downloader as api
from gensim.models.phrases import Phrases, ENGLISH_CONNECTOR_WORDS
from nltk.corpus import brown
from gensim.models.word2vec import Text8Corpus
from gensim.test.utils import datapath
import argparse

# load word2vec model
wv = api.load('word2vec-google-news-300')
# model = gensim.models.Word2Vec()
# model.wv.most_similar(positive = w1)

# sentences = brown.sents()
sentences = Text8Corpus(datapath('testcorpus.txt'))
phraseModel = Phrases(sentences, min_count=1, threshold=1, connector_words=ENGLISH_CONNECTOR_WORDS)
frozenPhrases = phraseModel.freeze()
# print(frozenPhrases['drive', 'very', 'fast', 'drive', 'extreme', 'hurry', 'depictive', 'classifier', 'vehicle', 'over', 'surface'])
# print(frozenPhrases['trees', 'graph', 'minors'])

def count(element, target):
    count = 0
    for i in element:
        if i == target:
            count += 1
    return count

# in each element, remove '/n'
def preprocessing(list):
    for i in range(len(list)):
        list[i] = list[i].replace('\n', '')
    return list

# connect two words in the phrase with '_'
# find out the possible phrases in a sentence using trained phrase model
# def phraseSentence(list):
#     for i in range(len(list)):
#         # # if one element has two words, make them as a phrase
#         if count(list[i], " ") == 1:
#             list[i] = list[i].replace(' ', '_')
#         # # # else, treat the element as a sentence
#         # elif count(list[i], " ") >=2:
#         #     list[i].split(" ")
#         #     list[i] = frozenPhrases[list[i]]
#     return list

# if the element is a sentence
# get the similarity score between input and the sentence
# divide the sentences into phrases, calculate sim score for each phrase and get average for the whole sentence
def similarScoreSentence(inputWord, element):
    score = 0.0
    count = 0
    list = element.split(" ")
    phraseList = frozenPhrases[list]
    for i in phraseList:
        score += wv.similarity(inputWord, i)
        count += 1
    return score/count

print(similarScoreSentence('daddy drive the bus'))
# get the most similar word/phrase
def maxSimilarityWord(word, outputList):
    maxSimWord = ''
    maxSimScore = 0.0
    for i in outputList:
        # if i is a word
        if count(i, " ") == 0:
            score = wv.similarity(word, i)
            if score >= maxSimScore:
                maxSimWord = i
                maxSimScore = score
        # if i is a phrase or a sentence
        else:
            score = similarScoreSentence(i)
            if score >= maxSimScore:
                maxSimWord = i
                maxSimScore = score
    return maxSimWord





# # read arguments
# parser = argparser.ArgumentParser()
# parser.add_argument('input', type= str, default = 'input.txt')
# parser.add_argument('output', type= str, default = 'output.txt')
# args = parser.parse_args()
# # open input file
# inputFilename = str(args.input)
# def openFile(filename):
#     with open(filename) as f:
#         inputList = f.readlines()
#     return inputList
#
# inputList = openFile(inputFilename)
# output = []
# # open corpus file
# with open('word_similarity.txt') as s:
#     outputList = s.readlines()
# # get the most similar word for each input word
# # store result in output list
# for i in inputList:
#     temp = maxSimilarityWord(i, outputList)
#     output.append(temp)
# # create output file: input word/phrase + most similar word/phrase
# outputFilename = str(args.output)
# with open(outputFilename,'w') as f:
#     for i in range(len(inputList)):
#         f.write(inputList[i])
#         f.write(" ")
#         f.write(outputList[i])
#         f.write("\n")
