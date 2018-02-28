# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created on 27/02/2018
@author: alicia
@description: create a vocabulary file from a CSV
"""

import csv
import pretraitement
from gensim.models import Word2Vec

# Constants #
max_size = 400 # The maximal size that a text should have.
fname = "preprocessing_model"

# Input files #
filename = 'Données_RICM_GEO_PRI7.csv'
fileHandle = open ( 'vocabulary.txt', 'w' )
sentences = []

with open(filename) as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Offre initiale  as key
        max_temp = row['Offre initiale ']
        cleaned = pretraitement.removeStopWords(max_temp)
        print(cleaned)
        print("---------------------------------------------------------------")
        sentences = sentences + [cleaned[0].split()]
        #print(len(cleaned[0].split()))
        if(len(cleaned[0].split()) >= max_size):
           fileHandle.write(' '.join(cleaned[:taille]))
        else :
           fileHandle.write(' '.join(cleaned))
fileHandle.close()

print("Taille = " + str(len(sentences)))
print(sentences)
model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
print(model.wv['x'])
model.save(fname)
