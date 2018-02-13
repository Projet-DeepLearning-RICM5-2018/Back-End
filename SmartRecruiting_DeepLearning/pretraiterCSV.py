# encoding: utf-8
# -*- coding: utf-8 -*-
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

def pretraiter(text):
    # split into words by white space
    words = text.split()
    # remove punctuation from each word
    #table = maketrans(None, string.punctuation)
    stripped = [w.lower().translate(None, string.punctuation) for w in words]
    return stripped

fileHandle = open ( 'offres.txt', 'w' ) 
with open(filename) as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Reasonforprotest as key
        max_temp = row['Offre initiale ']
        cleaned = pretraiter(max_temp)
        fileHandle.write(' '.join(cleaned[:250]))
        fileHandle.write ('\n')
fileHandle.close()
