import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
import gensim
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser, ENGLISH_CONNECTOR_WORDS
import gensim.downloader as api
from nltk.corpus import brown
from gensim.models.word2vec import Text8Corpus
from gensim.test.utils import datapath

# with open('input.txt') as s:
#     inputList = s.readlines()
# print(inputList)
# with open('word_similarity.txt') as s:
#     outputList = s.readlines()
# print(outputList)

# wv = api.load('word2vec-google-news-300')
# x = wv.similarity('hello hello', 'telephone')
# print("xxxxxxxxxxxxxxxxxxx = ", x)
# # print(wv.similarity('dog', 'cat'))

# sentences = brown.sents()
sentences = Text8Corpus(datapath('testcorpus.txt'))
phraseModel = Phrases(sentences, min_count=1, threshold=1, connector_words=ENGLISH_CONNECTOR_WORDS)
frozenPhrases = phraseModel.freeze()
print(frozenPhrases['drive', 'very', 'fast', 'drive', 'extreme', 'hurry', 'depictive', 'classifier', 'vehicle', 'over', 'surface'])
print(frozenPhrases['trees', 'graph', 'minors'])

# def maxSimilarityWord(word, outputList):
#     maxSimWord = ''
#     maxSimScore = 0
#     for i in outputList:
#         score = wv.similarity(word, i)
#         if score >= maxSimScore:
#             maxSimWord = i
#             maxSimScore = score
#     return maxSimWord
#
def count(element, target):
    count = 0
    for i in element:
        if i == target:
            count += 1
    return count
# print(count('red_bus_bus', '_'))
def preprocessing(list):
    for i in range(len(list)):
        list[i] = list[i].replace('\n', '')
        # # if one element has two words, make them as a phrase
        if count(list[i], " ") == 1:
            list[i] = list[i].replace(' ', '_')
        # # else, treat the element as a sentence
        else:
    return list
#
# # def buildPhraseModel(sentences):
#
#
# print("=================", preprocessing2phrase(inputList))
# # result = maxSimilarityWord('hello_hello')
