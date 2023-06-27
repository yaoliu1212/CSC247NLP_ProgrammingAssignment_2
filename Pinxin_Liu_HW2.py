# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 17:46:53 2022

@author: andyp
"""

import jsontrips
import gensim.downloader
import json
import pandas as pd
import numpy as np
import argparse

root = 'ROOT'

model = gensim.downloader.load('word2vec-google-news-300')
ontology_dict = jsontrips.ontology()
address1 = 'trips-brown_NV_overlap.txt'
address2 = 'brown_lemmatized.txt'
with open("lex-ont.json",'r', encoding='UTF-8') as f:
    dic = json.load(f)
    


def find_depth(word):
    depth = 0
    cur_dir = word
    while cur_dir != 'ROOT':
        cur_dir = ontology_dict[cur_dir]['parent']
        depth = depth + 1
    return depth

def palmer_score(word1, word2, dic):
    parent1 = dic[word1.upper()]['lf_parent']
    parent2 = dic[word2.upper()]['lf_parent']
    scores = []
    for i in parent1:
        for j in parent2:
            CS1 = []
            cur_dir = i
            CS1.append(cur_dir)
            while cur_dir != root:
                cur_dir = ontology_dict[cur_dir]['parent']
                CS1.append(cur_dir)
            cur_dir = j
            while cur_dir != root:
                if cur_dir in CS1:
                    break
                else:
                    cur_dir = ontology_dict[cur_dir]['parent']
            LCS = cur_dir
            
            score = 2 * find_depth(LCS)/(find_depth(i) + find_depth(j))
            scores.append(score)
    return max(scores)

def build_vocab(address):
    with open(address) as file:
        index = {}
        cur = 0
        data = file.read().split('\n')
        for word in data:
            index[word] = cur
            cur = cur + 1
    size = len(index)
    vocab = np.zeros([size, size])
    return index, vocab


def cal_vocab(address, vocab, index):
    with open(address) as file:
        sents = file.read().split('\n')
        for sent in sents:
            sent = sent.split(' ')
            for i in range(len(sent)):
                for j in range(1, 5):
                    if i - j >= 0:
                        try:
                            vocab[index[sent[i]], index[sent[i-j]]]  = vocab[index[sent[i]], index[sent[i-j]]] + 1
                        except:
                            continue
                    if i + j < len(sent):
                        try:
                            vocab[index[sent[i]], index[sent[i+j]]] = vocab[index[sent[i]], index[sent[i+j]]] + 1
                        except:
                            continue
        breakpoint()
    return vocab

def method3(index, vocab, word1, word2):
    word1_vec = vocab[index[word1], :]
    word2_vec = vocab[index[word2], :]
    top = np.dot(word1_vec.T, word2_vec)
    bottom = np.linalg.norm(word1_vec) * np.linalg.norm(word2_vec)
    score = top / bottom
    return score


    


def main():
    
    parser = argparse.ArgumentParser(description='CSC 247 HW2: Pinxin Liu')

    parser.add_argument('--input', required = False, type=str, help = 'the input file', default = 'input.csv')
    
    parser.add_argument('--output', required = False, type=str, help='the output file', default = 'out.csv')
    parser.add_argument('--score', required = False, type = str, help = "scores-file", default = 'res.csv')

    args = parser.parse_args()    
    filename1 = args.input
    filename2 = args.output
    filename3 = args.score
    
    index, vocab = build_vocab(address1)
    vocab = cal_vocab(address2, vocab, index)
    
    score = pd.DataFrame(columns = ['tripleid', 'word1', 'word2', 'word2vec-score', 'wu-palmer-score', 'brown-vector-score', 'your-novel-score'])
    
    input_file = pd.read_csv(filename1)
    for row in input_file.iterrows():
        word1 = row[1]['word1']
        word2 = row[1]['word2']
        word3 = row[1]['word3']
        simi_1_2_method1 = model.similarity(word1, word2)
        simi_1_2_method2 = palmer_score(word1, word2, dic)
        simi_1_2_method3 = method3(index, vocab, word1, word2)
        breakpoint()
        simi_1_2_method4 = 1/3 * simi_1_2_method1 + 1/3 * simi_1_2_method2 + 1/3 * simi_1_2_method3
        
        simi_1_3_method1 = model.similarity(word1, word3)
        simi_1_3_method2 = palmer_score(word1, word3, dic)
        simi_1_3_method3 = method3(index, vocab, word1, word3)
        simi_1_3_method4 = 1/3 * simi_1_3_method1 + 1/3 * simi_1_3_method2 + 1/3 * simi_1_3_method3
        
        simi_2_3_method1 = model.similarity(word2, word3)
        simi_2_3_method2 = palmer_score(word2, word3, dic)
        simi_2_3_method3 = method3(index, vocab, word2, word3)
        simi_2_3_method4 = 1/3 * simi_2_3_method1 + 1/3 * simi_2_3_method2 + 1/3 * simi_2_3_method3
        
        score.loc[len(score.index)] = [row[0], word1, word2, simi_1_2_method1, simi_1_2_method2, simi_1_2_method3, simi_1_2_method4]
        score.loc[len(score.index)] = [row[0], word1, word3, simi_1_3_method1, simi_1_3_method2, simi_1_3_method3, simi_1_3_method4]
        score.loc[len(score.index)] = [row[0], word2, word3, simi_2_3_method1, simi_2_3_method2, simi_2_3_method3, simi_2_3_method4]
        breakpoint()
        
    score.to_csv(filename3)
        
        
            
            
main()