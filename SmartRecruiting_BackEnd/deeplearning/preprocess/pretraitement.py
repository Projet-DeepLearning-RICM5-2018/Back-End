# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created on 27/02/2018
@author: alicia
@description: preprocessing of texts, using the removal of stop words and the Word2Vec to create descriptors
"""
import sys
import string
import csv
import numpy as np
from gensim.models import Word2Vec

# Constants definition #
max_size = 400 # The maximal size that a text should have.
stop_list =[word for line in open("./data/stopwords_fr.txt",encoding='utf-8', mode="r") for word in line.split()]

########################
# FUNCTIONS DEFINITION #
########################
"""
Function to remove stop words and punctuation from a text
@param text : string, the input text
@return [string] the tokenized text without the stop words and punctuation as a list
"""
def tokenize(text) :
    words = text.split() # split into words by white space
    words = [w.lower() for w in words] # put to lowercase
    words = [''.join(letter for letter in word if letter.isalpha()) for word in words] # remove punctuation
    words = list(filter(None,filter(lambda word: word not in stop_list, words))) # remove stop words
    return words


"""
Function to get the descriptor from a text
@param text : string, the input text
@return [[float]] the text's descriptor
"""
def preprocess(text) :
    cleaned = tokenize(text)
    model = Word2Vec.load("./data/preprocessing_model")
    words = list(filter(lambda x: x in model.wv.vocab, cleaned))
    if(len(words) >= max_size) :
        words = words[:max_size]
    else :
        words = words + ['x']*(max_size-len(words))
    descriptor = [model.wv[w] for w in words]
    return descriptor

"""
Function to preprocess all the offer from a csv.
@param fileName : string, the name of the file containing the data to Process
@return [(string,[[float]],string)] list of all offers and their descriptors : (text,descriptor,label)
"""
def preprocessAll(file_name) :
    learning_base = []
    with open(file_name,encoding='utf-8', mode="r") as f:
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
def init(dbManager) :
    # Input files #
    filename = './data/Données_RICM_GEO_PRI7.csv'
    sentences = [['x','x','x','x','x']]
    with open(filename,encoding='utf-8', mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row['Offre initiale '] # Get the text from the initial offer
            cleaned = tokenize(text)
            sentences = sentences + [cleaned] #Sentences used to build the model's vocabulary
    model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model.save("./data/preprocessing_model")

    # Put everything in the DB for the first time"
    base = preprocessAll(filename)
    add_base_to_database(dbManager,base)


"""
To reinit the model, and calculate all the descriptors when the DB changed
So not taking data from the CSV but DB
"""
def reinit(dbManager) :
    # Get all offers from dB"
    offers = dbManager.get_all_offers()

    # Rebuild the model #
    sentences = [['x','x','x','x','x']]
    for o in offers :
        text = o['content']
        cleaned = tokenize(text)
        sentences = sentences + [cleaned] #Sentences used to build the model's vocabulary
    model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model.save("./data/preprocessing_model")#path root

    # Recompute all descriptors and put them in the DB #
    res  = recompute_all_descriptors(offers)
    update_all_offers(dbManager,res)

"""
Recompute descriptor for each offer given
@param offers : a list of offers
@return a list of (id, descriptors)
"""
def recompute_all_descriptors(offers) :
    res = []
    for o in offers :
        desc = preprocess(o['content'])
        id = o['id']
        res = res + [{'id':id,'desc':desc}]
    return res

###########################################
# FUNCTIONS REGARDING THE DATABASE ACCESS #
###########################################
"""
Add a preprocessed offer in the database
@param offer : (text,descriptor,label) the processed offer
@return id : int, id of the newly created offer
"""
def add_an_offer(dbManager, offer, idAdmin) :
    #Make title
    title = offer[0].split(' ')
    title = title[:5]
    title = ' '.join(title)

    #Make descriptor
    desc = (np.array2string(o, precision=5, separator=' ', suppress_small=False) for o in offer[1])
    desc = ','.join(desc)

    id = dbManager.add_offer_v2(title, offer[0], desc, idAdmin)
    return id

"""
Update the descriptor of an offer
@param dbManager
@param offer_id
@param descriptor
@return 1 if successful, -1 else.
"""
def update_descriptor_of_offer_by_id(dbManager,id,descriptor) :
    desc = (np.array2string(word_vector, precision=5, separator=' ', suppress_small=False) for word_vector in descriptor)
    desc = ','.join(desc)
    if dbManager.update_offer(id,None,None,desc,None) :
        return 1
    else :
        return -1

"""
Update all given offers by id (in the DB)
@param dbManager
@param list : list of (id, descriptors)
"""
def update_all_offers(dbManager,list) :
    for item in list :
        update_descriptor_of_offer_by_id(dbManager,item['id'],item['desc'])

"""
Add all preprocessed offer in the database
@param offer : list of (text,descriptor,label)
"""
def add_base_to_database(dbManager, base):
    adminId = dbManager.get_one_admin().id
    for offer in base :
        nameField = offer[2]
        idOffer = add_an_offer(dbManager, offer, adminId)
        if idOffer!=-1 :
            idPredic = dbManager.add_prediction_v2(10.0, True, idOffer)
            if idPredic!=-1:
                idField = get_id_field(dbManager,nameField)
                if idField!=-1 :
                    dbManager.add_team(idPredic , idField, 1)


"""
Add id of the named field or create the field and get the id if the field doesn't exist
@param offer : name of the field (string)
@return id of the offer if succesful, -1 if not
"""
def get_id_field(dbManager, name)  :
   field = dbManager.get_field_by_name(name)
   if field :
      return field.id
   else :
      id = dbManager.add_field_v2(name, "", "", "")
      if id!=-1:
         return id
      else :
         return -1
