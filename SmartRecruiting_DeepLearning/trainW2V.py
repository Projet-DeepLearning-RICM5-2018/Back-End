#! /usr/bin/env python

import tensorflow as tf
import numpy as np
import os
import pretraitement
import time
import datetime

from TextCNN import TextCNN

embedding_dim = 100
filter_sizes = "3,4,5"
num_filters = 128
l2 = 0.0
num_checkpoints = 5
# dropout_keep_prob = 0.5
checkpoint_every = 100
evaluate_every = 100
batch_size = 64
num_epochs = 200

#changeBegin
# Parameters
# ==================================================

# Data loading params
tf.flags.DEFINE_float("dev_sample_percentage", .1, "Percentage of the training data to use for validation")
tf.flags.DEFINE_string("positive_data_file", "./data/rt-polaritydata/rt-polarity.pos", "Data source for the positive data.")
tf.flags.DEFINE_string("negative_data_file", "./data/rt-polaritydata/rt-polarity.neg", "Data source for the negative data.")

# Model Hyperparameters
tf.flags.DEFINE_integer("embedding_dim", 128, "Dimensionality of character embedding (default: 128)")
tf.flags.DEFINE_string("filter_sizes", "3,4,5", "Comma-separated filter sizes (default: '3,4,5')")
tf.flags.DEFINE_integer("num_filters", 128, "Number of filters per filter size (default: 128)")
tf.flags.DEFINE_float("dropout_keep_prob", 0.5, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "L2 regularization lambda (default: 0.0)")

# Training parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_integer("num_epochs", 200, "Number of training epochs (default: 200)")
tf.flags.DEFINE_integer("evaluate_every", 100, "Evaluate model on dev set after this many steps (default: 100)")
tf.flags.DEFINE_integer("checkpoint_every", 100, "Save model after this many steps (default: 100)")
tf.flags.DEFINE_integer("num_checkpoints", 5, "Number of checkpoints to store (default: 5)")
# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

#changeEnd

base = pretraitement.init() #[(string,[[float]],string)]
#base.shape(59,) array([(,,),(),(),()*59])
x, y = [], []

def get_num(val) :
    if val=="GEO" :
        return [1,0,0]
    elif val == "RICM" :
        return [0,1,0]
    else :
        return [0,0,1]


for i in base:#[(text,preprocess(text),label)]
    x.append(np.array(i[1]))# liste descripteur
    y.append(np.array(get_num(i[2])))#base[:,2] #liste label
x = np.array(x)
y = np.array(y)
print(y)
print("try to find")
print(base[58][2])
# Randomly shuffle data
np.random.seed(10)
shuffle_indices = np.random.permutation(np.arange(len(y)))
#print(shuffle_indices)
x_shuffled = np.array(list(x))[shuffle_indices]
y_shuffled = np.array(list(y))[shuffle_indices]

#train/test
dev_sample_index = -1 * int(.1 * float(len(y)))
x_train, x_dev = x_shuffled[:dev_sample_index], x_shuffled[dev_sample_index:]
y_train, y_dev = y_shuffled[:dev_sample_index], y_shuffled[dev_sample_index:]
print("descriptor size: %s" % len(x_train[0]))
#cross validation
k = 10
cut_size = len(x_shuffled) / k
'''
for step in range(0,k) :
    cut = step * cut_size
    test_x,test_y = x_shuffled[cut:cut+cut_size],y_shuffled[cut:cut+cut_size]
    learn_x,learn_y = np.vstack((x_shuffled[0:cut], x_shuffled[cut+cut_size:size])),np.vstack((y_shuffled[0:cut], y_shuffled[cut+cut_size:size]))
'''
del x, y, x_shuffled, y_shuffled
print("Train/Dev split: {:d}/{:d}".format(len(y_train), len(y_dev)))

# Training
# ==================================================
FLAGS = tf.flags.FLAGS

with tf.Graph().as_default():
    #changebegin
    session_conf = tf.ConfigProto(
        allow_soft_placement=FLAGS.allow_soft_placement,
        log_device_placement=FLAGS.log_device_placement)
    #changeEnd

    with tf.Session(config=session_conf) as sess:
        cnn = TextCNN(
            sequence_length=pretraitement.max_size,
            num_classes=3, #TODO a recuperer dans la BD
            vocab_size=len(x_train[0]),
            embedding_size=embedding_dim,
            filter_sizes=list(map(int, filter_sizes.split(","))),
            num_filters=num_filters,
            descriptor_size=embedding_dim,
            l2_reg_lambda=l2)
        # Define Training procedure
        global_step = tf.Variable(0, name="global_step", trainable=False)
        optimizer = tf.train.AdamOptimizer(1e-3)
        grads_and_vars = optimizer.compute_gradients(cnn.loss)
        train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

        # Output directory for models and summaries
        timestamp = str(int(time.time()))
        out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
        print("Writing to {}\n".format(out_dir))

        # Summaries for loss and accuracy
        loss_summary = tf.summary.scalar("loss", cnn.loss)
        acc_summary = tf.summary.scalar("accuracy", cnn.accuracy)

        # Train Summaries
        train_summary_op = tf.summary.merge([loss_summary, acc_summary])
        train_summary_dir = os.path.join(out_dir, "summaries", "train")
        train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)

        # Dev summaries
        dev_summary_op = tf.summary.merge([loss_summary, acc_summary])
        dev_summary_dir = os.path.join(out_dir, "summaries", "dev")
        dev_summary_writer = tf.summary.FileWriter(dev_summary_dir, sess.graph)


        # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
        checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
        checkpoint_prefix = os.path.join(checkpoint_dir, "model")
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=num_checkpoints)



        # Initialize all variables
        sess.run(tf.global_variables_initializer())

        def train_step(x_batch, y_batch):
            """
            A single training step

            """

            x_batch2 = np.array(x_batch)
            y_batch2 = np.array(y_batch)
            print("x_bach:")
            print(type(x_batch2))
            print(len(x_batch2))
            print(type(x_batch2[0]))

            print(len(x_batch2[0]))
            print(type(x_batch2[0][0]))
            print(type(x_batch2[0][0][0]))
            print(type(y_batch2))
            print(type(y_batch2[0]))



            feed_dict = {
              cnn.input_x: x_batch2,
              cnn.input_y: y_batch2,
              cnn.dropout_keep_prob: FLAGS.dropout_keep_prob

            }
            print(type(feed_dict))


            _, step, summaries, loss, accuracy = sess.run(
                [train_op, global_step, train_summary_op, cnn.loss, cnn.accuracy],
                feed_dict)
            time_str = datetime.datetime.now().isoformat()
            print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))
            train_summary_writer.add_summary(summaries, step)

        def dev_step(x_batch, y_batch, writer=None):
            """
            Evaluates model on a dev set
            """
            feed_dict = {
              cnn.input_x: x_batch,
              cnn.input_y: y_batch,
              cnn.dropout_keep_prob: 1.0
            }
            step, summaries, loss, accuracy = sess.run(
                [global_step, dev_summary_op, cnn.loss, cnn.accuracy],
                feed_dict)
            time_str = datetime.datetime.now().isoformat()
            print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))
            if writer:
                writer.add_summary(summaries, step)

        def batch_iter(data, batch_size, num_epochs, shuffle=True):
            """
            Generates a batch iterator for a dataset.
            """
            data = np.array(data)
            data_size = len(data)
            num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
            for epoch in range(num_epochs):
            # Shuffle the data at each epoch
                if shuffle:
                    shuffle_indices = np.random.permutation(np.arange(data_size))
                    shuffled_data = data[shuffle_indices]
                else:
                    shuffled_data = data
                for batch_num in range(num_batches_per_epoch):
                    start_index = batch_num * batch_size
                    end_index = min((batch_num + 1) * batch_size, data_size)
                    yield shuffled_data[start_index:end_index]

        # Generate batches
        batches = batch_iter(
            list(zip(x_train, y_train)), batch_size, num_epochs)
        # Training loop. For each batch...
        for batch in batches:
            x_batch, y_batch = zip(*batch)
            train_step(x_batch, y_batch)
            current_step = tf.train.global_step(sess, global_step)
            if current_step % evaluate_every == 0:
                print("\nEvaluation:")
                dev_step(x_dev, y_dev, writer=dev_summary_writer)
                print("")
            if current_step % checkpoint_every == 0:
                path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                print("Saved model checkpoint to {}\n".format(path))
