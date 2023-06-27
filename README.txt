Name: Yao Liu
NetID: yliu204

1. Example of terminal command line:
C:\Users\liuya\OneDrive\桌面\CSC247\Programming Assignment\programming 2>python homework2.py input.csv output.csv score.csv

2. Four Measures
a. Word2Vec
I used 'word2vec-google-news-300'. 
Word2Vec is easy to understand, and I think it works well for word meaning classification

b. Wu-Palmer
I think Wu-Palmer also works well in word meaning. Because it considers different meaning of a same word.

c. Vector
The approach that works poorly (or maybe it will works better when we use a larger corpus to train). 
It does not work well because 1)small size corpus; 2)method of calculating vectors; 3)the given word we counts; (also the changing the size of the window may increase the accuracy)

d. Combination of three
Since three of them are work well, especially the first two, I combined the score of these three scores. 
I gave more weight to word2vec and Wu-Palmer score because I think they are more accurate then vector approach.

