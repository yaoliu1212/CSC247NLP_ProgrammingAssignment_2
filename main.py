import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
nltk.download('punkt')
import gensim
from gensim.models import Word2Vec

import gensim.downloader as api
wv = api.load('word2vec-google-news-300')
print("similarity: ", wv.similarity('dog', 'cat'))
# print("similarity: ", round(wv.similarity('dog', 'house'), 3))
# print("similarity: ", round(wv.similarity('cat', 'house'), 3))
#
# print("similarity: ", round(wv.similarity('bottle', 'house'), 3))
# print("similarity: ", round(wv.similarity('bottle', 'run'), 3))
# print("similarity: ", round(wv.similarity('house', 'run'), 3))
#
# print("similarity: ", round(wv.similarity('drum', 'health'), 3))
# print("similarity: ", round(wv.similarity('drum', 'milk'), 3))
# print("similarity: ", round(wv.similarity('health', 'milk'), 3))
#
# print("similarity: ", round(wv.similarity('doc', 'queen'), 3))
# print("similarity: ", round(wv.similarity('doc', 'friend'), 3))
# print("similarity: ", round(wv.similarity('queen', 'friend'), 3))
#
# print("similarity: ", round(wv.similarity('save', 'help'), 3))
# print("similarity: ", round(wv.similarity('save', 'waste'), 3))
# print("similarity: ", round(wv.similarity('help', 'waste'), 3))


