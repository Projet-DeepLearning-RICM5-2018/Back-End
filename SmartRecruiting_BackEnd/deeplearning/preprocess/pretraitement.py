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
from SmartRecruiting_BackEnd import app

# Constants definition #
max_size = 400 # The maximal size that a text should have.
app.config['stop_list'] =[word for line in open("./data/stopwords_fr.txt",encoding='utf-8', mode="r") for word in line.split()]

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
    words = list(filter(None,filter(lambda word: word not in app.config['stop_list'], words))) # remove stop words
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
def preprocess_all(file_name) :
    learning_base = []
    with open(file_name,encoding='utf-8', mode="r") as f:
        reader = csv.DictReader(f)
        i = 1
        for row in reader:
            print('preprocess offer ' + str(i))
            i+=1
            text = row['Offre initiale'] # Get the text from the initial offer
            label = row['Formation']
            learning_base = learning_base + [(text,preprocess(text),label)] # All the text saved for preprocessing after building the model
    return learning_base

"""
Function to preprocess all the offer from a csv and add them in the database.
@param fileName : string, the name of the file containing the data to Process
"""
def preprocess_all_and_add_to_database(db_manager, file_name) :
    with open(file_name,encoding='utf-8', mode="r") as f:
        reader = csv.DictReader(f)
        i = 1
        for row in reader:
            print('preprocess offer ' + str(i))
            i+=1
            text = row['Offre initiale'] # Get the text from the initial offer
            label = row['Formation']
            add_offer_to_database(db_manager, (text,preprocess(text),label))

"""
Function to initialize the model and BDD
Has to be called before using the model for the first time or if the csv containing the base changed
@return the preprocessed descriptors
"""
def init(db_manager) :
    # Input files #
    filename = './data/offers.csv'
    sentences = [['x','x','x','x','x']]
    with open(filename,encoding='utf-8', mode="r") as f:
        reader = csv.DictReader(f)
        i = 1
        for row in reader:
            text = row['Offre initiale'] # Get the text from the initial offer
            print('init offer ' + str(i))
            i+=1
            cleaned = tokenize(text)
            sentences = sentences + [cleaned] #Sentences used to build the model's vocabulary
    model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model.save("./data/preprocessing_model")

    # Put everything in the DB for the first time"
    preprocess_all_and_add_to_database(db_manager, filename)

    # Add fields
    filename = './data/fields.csv'
    with open(filename,encoding='utf-8', mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            set_field_information(db_manager, row['name'], row['description'], row['website'])

    # Add contacts
    filename = './data/contacts.csv'
    with open(filename,encoding='utf-8', mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(db_manager, row['field'], row['name'], row['surname'], row['role'], row['email'], row['phone'])


"""
To reinit the model, and calculate all the descriptors when the DB changed
So not taking data from the CSV but DB
"""
def reinit(db_manager) :
    # Get all offers from dB"
    offers = db_manager.get_all_offers()

    # Rebuild the model #
    sentences = [['x','x','x','x','x']]
    i = 1
    for o in offers :
        print('reinit offer ' + str(i))
        i+=1
        text = o['content']
        cleaned = tokenize(text)
        sentences = sentences + [cleaned] #Sentences used to build the model's vocabulary
    model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model.save("./data/preprocessing_model")#path root

    # Recompute all descriptors and put them in the DB #
    res  = recompute_all_descriptors(offers)
    update_all_offers(db_manager,res)

"""
Recompute descriptor for each offer given
@param offers : a list of offers
@return a list of (id, descriptors)
"""
def recompute_all_descriptors(offers) :
    res = []
    i = 1
    for o in offers :
        print('recompute offer ' + str(i))
        i+=1
        desc = preprocess(o['content'])
        id = o['id']
        res = res + [{'id':id,'desc':desc}]
    return res

###########################################
# FUNCTIONS REGARDING THE DATABASE ACCESS #
###########################################

"""
Transforms a descriptor into a text
@param a descriptor [[float]]
@return str
"""
def descriptor_to_string(descriptor) :
    desc = (np.array2string(word_vector, precision=5, separator=' ', suppress_small=False) for word_vector in descriptor)
    desc = ','.join(desc)
    return desc


"""
Add a preprocessed offer in the database
@param offer : (text,descriptor,label) the processed offer
@return id : int, id of the newly created offer
"""
def add_an_offer(db_manager, offer, id_admin) :
    #Make title
    title = offer[0].split(' ')
    title = title[:5]
    title = ' '.join(title)

    #Make descriptor
    desc = descriptor_to_string(offer[1])

    id = db_manager.add_offer_v2(title, offer[0], desc, id_admin)
    return id

"""
Update the descriptor of an offer
@param db_manager
@param offer_id
@param descriptor
@return 1 if successful, -1 else.
"""
def update_descriptor_of_offer_by_id(db_manager,id,descriptor) :
    desc = descriptor_to_string(descriptor)
    if db_manager.update_offer(id,None,None,desc,None) :
        return 1
    else :
        return -1

"""
Update all given offers by id (in the DB)
@param db_manager
@param list : list of (id, descriptors)
"""
def update_all_offers(db_manager,list) :
    i = 1
    for item in list :
        print('update offer ' + str(i))
        i+=1
        update_descriptor_of_offer_by_id(db_manager,item['id'],item['desc'])

"""
Add all preprocessed offer in the database
@param offer : list of (text,descriptor,label)
"""
def add_base_to_database(db_manager, base):
    admin_id = db_manager.get_one_admin().id
    i = 1
    for offer in base :
        print('add to database offer ' + str(i))
        i+=1
        name_field = offer[2]
        id_offer = add_an_offer(db_manager, offer, admin_id)
        if id_offer!=-1 :
            id_predic = db_manager.add_prediction_v2(10.0, True, id_offer)
            if id_predic!=-1:
                id_field = get_id_field(db_manager,name_field)
                if id_field!=-1 :
                    db_manager.add_team(id_predic , id_field, 1)

"""
Add one preprocessed offer in the database
@param offer : list of (text,descriptor,label)
"""
def add_offer_to_database(db_manager, offer):
    admin_id = db_manager.get_one_admin().id
    name_field = offer[2]
    id_offer = add_an_offer(db_manager, offer, admin_id)
    if id_offer!=-1 :
        id_predic = db_manager.add_prediction_v2(10.0, True, id_offer)
        if id_predic!=-1:
            id_field = get_id_field(db_manager,name_field)
            if id_field!=-1 :
                db_manager.add_team(id_predic , id_field, 1)


"""
Add id of the named field or create the field and get the id if the field doesn't exist
@param offer : name of the field (string)
@return id of the offer if succesful, -1 if not
"""
def get_id_field(db_manager, name)  :
   field = db_manager.get_field_by_name(name)
   if field :
      return field.id
   else :
      id = db_manager.add_field_v2(name, "", "", "")
      if id!=-1:
         return id
      else :
         return -1

"""
Set information for the field name
@param name : name of the field to update
@param description
@param website
"""
def set_field_information(db_manager, name, description, website):
    id = get_id_field(db_manager, name)
    db_manager.update_field(id, name, description, None, website)

"""
Insert contact in the database
@param field_name
@param name
@param surname
@param role
@param email
@param phone
"""
def add_contact(db_manager, field_name, name, surname, role, email, phone):
    id_field = get_id_field(db_manager, field_name)
    db_manager.add_contact(name, surname, email, phone, role, id_field)
