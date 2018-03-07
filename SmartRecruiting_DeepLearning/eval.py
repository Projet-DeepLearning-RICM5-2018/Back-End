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


def checkPath():
    """
    Function to get the path of checkpoint
    :return:the path
    """
    checkPath = open('checkPath', "r").read()
    print(checkPath)
    checkpoint_file = tf.train.latest_checkpoint(checkPath)
    return checkpoint_file


def getDic():
    with open('./data/dic','rb') as fichier:
        mypic = pickle.Unpickler(fichier)
        dic = mypic.load()
    return dic


def FormationByOffer(text):
    """
    Function to compute the field for an offer
    :param text:
    :return:the field
    """
    def_flags()
    FLAGS = tf.flags.FLAGS
    x_test = pretraitement.preprocess(text)
    checkpoint_file=checkPath()
    graph = tf.Graph()
    pred=[]
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
        # input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

        # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]
            scores = graph.get_operation_by_name("output/scores").outputs[0]

        # Generate batches for one epoch
            pred, sc = sess.run([predictions,scores],{input_x:x_test,dropout_keep_prob: 1.0})
            #print(pred)#[2][0]
    return pred[0]


def eval_all(db_manager) :

    def_flags()
    FLAGS = tf.flags.FLAGS
    x, y, dic = get_data_from_database(db_manager)
    y_test = y
    x_test = x

    print("\nEvaluating...\n")

    # Evaluation
    # ==================================================
    
    checkpoint_file = checkPath()
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
            input_y = graph.get_operation_by_name("input_y").outputs[0]
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
        #correct_predictions = float(sum(all_predictions == y_test))
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


def def_flags():
    # Eval Parameters
    # tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")#
    tf.flags.DEFINE_string("checkpoint_dir", "./runs/", "Checkpoint directory from training run")
    tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

    # Misc Parameters
    tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")#
    tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")#

def ind_1(ten):
    ind =0
    for t in ten:
        if t==1: return ind
        else : ind += 1
    return ind