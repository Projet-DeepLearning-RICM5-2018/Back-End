# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created on 27/02/2018
@author: alicia
@description: preprocessing of texts, using the removal of stop words and the Word2Vec to create descriptors
"""

import string
import csv
from gensim.models import Word2Vec

# Constants definition #
max_size = 400 # The maximal size that a text should have.
stop_list =[word for line in open("stopwords_fr.txt", 'r') for word in line.split()]

# Functions definition #

"""
Function to remove stop words and punctuation from a text
@param text, the input text
@return the text without the stop words and punctuation
"""
def removeStopWords(text) :
    # split into words by white space
    words = text.split()
    # remove punctuation from each word
    punct = str.maketrans(dict.fromkeys(string.punctuation + "•" + "’")) # To use translate in Python 3 we need to use the function maketrans
    no_punct = [w.lower().translate(punct) for w in words]

    #p=[sfin.translate(None,'·       ') for sfin in s]
    no_stop_words = [' '.join(filter(None,filter(lambda word: word not in stop_list, no_punct)))]
    return no_stop_words

"""
Function to initialize the model
"""
def init() :
    # Input files #
    filename = 'Données_RICM_GEO_PRI7.csv'
    fileHandle = open('vocabulary.txt','w')
    sentences = []
    learning_base = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Offre initiale  as key
            max_temp = row['Offre initiale ']
            cleaned = removeStopWords(max_temp)
            learning_base = learning_base + [preprocess(max_temp)]
            sentences = sentences + [cleaned[0].split()]
            #print(len(cleaned[0].split()))
            if(len(cleaned[0].split()) >= max_size):
               fileHandle.write(' '.join(cleaned[:taille]))
            else :
               fileHandle.write(' '.join(cleaned))
    fileHandle.close()
    model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model.save("preprocessing_model")
    return learning_base

"""
Function to rget the descriptor from a text
@param text, the input text
@return the text's descriptor
"""
def preprocess(text) :
    cleaned = removeStopWords(text)[0].split()
    model = Word2Vec.load("preprocessing_model")
    words = filter(lambda x: x in model.wv.vocab, cleaned)
    descriptor = [model.wv[w] for w in words]
    return descriptor

# Tests #
base = init()
text = open ( 'test.txt', 'r' ).read()
print(preprocess(text))
