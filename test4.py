sample = open('brown_lemmatized.txt')
s = sample.read()
file = s.replace('\n', ' ')
brownSentence = file.split(' ')

print(brownSentence[0])
