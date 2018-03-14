#! /usr/bin/env python

import tensorflow as tf
import numpy as np
import os
import time
import datetime
from SmartRecruiting_BackEnd.deeplearning.preprocess import pretraitement
from SmartRecruiting_BackEnd.deeplearning.cnn import textCnn
from tensorflow.contrib import learn
import csv
import pickle
from SmartRecruiting_BackEnd.deeplearning.cnn.train import get_data_from_database

def check_path():
    """
    Function to get the path of checkpoint
    :return:the path
    """
    check_path = open('./data/checkPath', "r").read()
    print(check_path)
    checkpoint_file = tf.train.latest_checkpoint(check_path)
    return checkpoint_file


def get_dic():
    with open('./data/dic','rb') as fichier:
        mypic = pickle.Unpickler(fichier)
        dic = mypic.load()
    return dic

def def_eval_flag() :
    tf.flags.DEFINE_string("checkpoint_dir", "./runs/", "Checkpoint directory from training run")
    tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

def FormationByOffer(text):
    """
    Function to compute the field for an offer
    :param text:
    :return:the field
    """
    # Eval Parameters

    FLAGS = tf.flags.FLAGS
    x_test = pretraitement.preprocess(text)
    #print(x_test)
    checkpoint_file=check_path()
    graph = tf.Graph()
    pred=[]
    s=1
    with graph.as_default():
        session_conf = tf.ConfigProto(
          allow_soft_placement=FLAGS.allow_soft_placement,
          log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
        # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

        # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

        # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]
            scores = graph.get_operation_by_name("output/scores").outputs[0]

        # Generate batches for one epoch
            pred, sc = sess.run([predictions,scores],{input_x:[x_test],dropout_keep_prob: 1.0})
            print(pred)#[2][0]
    ten = np.zeros(len(get_dic()), int)
    ten[pred[0]] = 1
    print(get_dic())
    #print(list(get_dic().keys())[list(get_dic().values()).index(ten)])
    for idf, arrf in get_dic().items():    # for name, age in list.items(): iteritems (for Python 3.x)
        if (arrf == ten).all():
            s=idf
            print(idf)
            print(s)
    return s


def eval_all(db_manager) :

    # Misc Parameters


    FLAGS = tf.flags.FLAGS
    x, y, dic, nb_classes = get_data_from_database(db_manager)
    y_test = y
    x_test = x

    print("\nEvaluating...\n")

    # Evaluation
    # ==================================================

    checkpoint_file = check_path()
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
          allow_soft_placement=FLAGS.allow_soft_placement,
          log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]
            scores = graph.get_operation_by_name("output/scores").outputs[0]

            # Generate batches for one epoch
            batches = [x_test]
            # TODO utiliser batch iter

            pred, sc = sess.run([predictions, scores], {input_x: x_test, dropout_keep_prob: 1.0})

            # Collect the predictions here
            all_predictions = []

            for x_test_batch in batches:
                batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                all_predictions = np.concatenate([all_predictions, batch_predictions])

    # Print accuracy if y_test is defined
    if y_test is not None:
        correct_predictions = 0.0
        for i in range(0, len(all_predictions)):
            print("predicion : {}".format(all_predictions[i]))
            print("y:.{}, {}".format(y_test[i], ind_1(y_test[i])))
            if all_predictions[i] == ind_1(y_test[i]):
                correct_predictions += 1
        nb_test = len(y_test)
        print("Total number of test examples: {}".format(nb_test))
        accuracy = correct_predictions/float(nb_test)
        print("Accuracy: {:g}".format(accuracy))
        print("correct_predictions: {}".format(correct_predictions))
    return nb_test, accuracy

def save_eval(nb_test, accuracy):
    with open('./data/eval', 'wb') as file:
        mon_pickler = pickle.Pickler(file)
        mon_pickler.dump(nb_test)
        mon_pickler.dump(accuracy)

def load_eval():
    with open('./data/eval', 'rb') as file:
        mon_pickler = pickle.Unpickler(file)
        nb_test = mon_pickler.load()
        accuracy = mon_pickler.load()
    return nb_test, accuracy


def ind_1(ten):
    ind =0
    for t in ten:
        if t==1: return ind
        else : ind += 1
    return ind
