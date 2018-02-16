# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created on 12th Feb 2018
@author: Qianqian
@description: preprocess the file CSV of PStage(Données_RICM_GEO_PRI7.csv), remove French stopwords and Special characters, into the file TXT size of 400(offres.txt)
"""

import string
import csv
import pandas as pd
from string import maketrans   # Required to call maketrans function.
import sys
ENCODING="iso-8859-15" # ce programme génère du latin-9 par défaut

if not sys.stdout.encoding: # pas d'encoding sur le flux de sortie standard
  sys.stdout = codecs.getwriter(ENCODING)(sys.stdout) # écrire du latin-9
if not sys.stderr.encoding: # pas d'encoding sur le flux d'erreur
  sys.stderr = codecs.getwriter(ENCODING)(sys.stderr) # écrire du latin-9

filename = 'Données_RICM_GEO_PRI7.csv'
stop_list =[word for line in open("stopwords_fr.txt", 'r') for word in line.split()]

#Entrée : une offre en format chaine de caractère
#Sortir : une liste de mot,taille 400
# remove characters and stoplist words
def pretraiter(text):
    # split into words by white space
    words = text.split()
    # remove punctuation from each word
    #table = maketrans(None, string.punctuation)
    stripped = [w.lower().translate(None, string.punctuation) for w in words]
    s=[st.translate(None,'•') for st in stripped]
    p=[sfin.translate(None,'·       ') for sfin in s]
    stemmed_text_data = [' '.join(filter(None,filter(lambda word: word not in stop_list, p)))]
    #print stemmed_text_data
    return stemmed_text_data
taille=400
fileHandle = open ( 'offres.txt', 'w' ) 
with open(filename) as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Offre initiale  as key
        max_temp = row['Offre initiale ']
        cleaned = pretraiter(max_temp)
        print len(cleaned[0].split())
        if(len(cleaned[0].split())>=taille):
           fileHandle.write(' '.join(cleaned[:taille]))
        else :
           fileHandle.write(' '.join(cleaned))
           for i in range(taille-len(cleaned[0].split())):
               fileHandle.write(' x')
        fileHandle.write ('\n')
fileHandle.close()
