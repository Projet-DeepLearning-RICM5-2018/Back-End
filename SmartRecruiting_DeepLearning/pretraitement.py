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
@param text : string, the input text
@return [string] the tokenized text without the stop words and punctuation as a list
"""
def tokenize(text) :
    words = text.split() # split into words by white space
    words = [w.lower() for w in words] # put to lowercase
    # remove punctuation
    punct = str.maketrans(dict.fromkeys(string.punctuation + "•" + "’")) # To use translate in Python 3 we need to use the function maketrans
    words = [w.translate(punct) for w in words] # translate removes characters
    words = list(filter(None,filter(lambda word: word not in stop_list, words))) # remove stop words
    return words


"""
Function to get the descriptor from a text
@param text : string, the input text
@return [[float]] the text's descriptor
"""
def preprocess(text) :
    cleaned = tokenize(text)
    model = Word2Vec.load("preprocessing_model")
    words = filter(lambda x: x in model.wv.vocab, cleaned)
    descriptor = [model.wv[w] for w in words]
    return descriptor

"""
Function to preprocess all the offer from a csv.
@param fileName : string, the name of the file containing the data to Process
@return [(string,[[float]],string)] list of all offers and their descriptors : (text,descriptor,label)
"""
def preprocessAll(file_name) :
    learning_base = []
    with open(file_name) as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row['Offre initiale '] # Get the text from the initial offer
            label = row['Formation']
            learning_base = learning_base + [(text,preprocess(text),label)] # All the text saved for preprocessing after building the model
    return learning_base

"""
Function to initialize the model and BDD
Has to be called before using the model for the first time or if the csv containing the base changed
@return the preprocessed descriptors
"""
def init() :
    # Input files #
    filename = 'Données_RICM_GEO_PRI7.csv'
    sentences = []
    base_text = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row['Offre initiale '] # Get the text from the initial offer
            cleaned = tokenize(text)
            sentences = sentences + [cleaned] #Sentences used to build the model's vocabulary
            base_text = base_text + [text] # All the text saved for preprocessing after building the model

    model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model.save("preprocessing_model")

    # TODO : Put everything in the DB for the first time"
    return preprocessAll(filename)

"""
To reinit the model, and calculate all the descriptors when the DB changed
So not taking data from the CSV but DB
"""
def reinit() :
    # TODO : Get all offers from dB"
    # Rebuild the model #
    # Recompute all descriptors and put them in the DB #
    blop = 2


# Tests #
#base = init()
#print(base[:2])
#text = open ( 'test.txt', 'r' ).read()
#print((text,preprocess(text)[:10]))
