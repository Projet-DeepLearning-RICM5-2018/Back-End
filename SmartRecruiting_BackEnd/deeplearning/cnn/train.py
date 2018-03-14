import tensorflow as tf
import numpy as np
import os
import pickle


import time
import datetime
from SmartRecruiting_BackEnd.deeplearning.cnn.textCnn import TextCNN
import SmartRecruiting_BackEnd.deeplearning.preprocess.pretraitement as pretraitement


def train(db_manager, filter_sizes, num_filters, l2, batch_size, num_epochs):
    """
    Train a convolutional neuronal network and save it in a file in /runs
    @:param: db_manager a manager
    @:return: a boolean
    """
    embedding_dim = 100
    #filter_sizes = "3,4,5"
    #num_filters = 128
    #l2 = 0.0
    num_checkpoints = 5
    # dropout_keep_prob = 0.5
    checkpoint_every = 100
    evaluate_every = 100
    #batch_size = 64
    #num_epochs = 200

    # embedding_dim = 100
    # filter_sizes = "3,4,5"
    # num_filters = 128
    # l2 = 0.0
    # dropout_keep_prob = 0.5
    # batch_size = 64
    # num_epochs = 200

    # get the data from the database
    x, y, dic_cores, nb_classes = get_data_from_database(db_manager)
    with open('./data/dic', 'wb') as file:
        mon_pickler = pickle.Pickler(file)
        mon_pickler.dump(dic_cores)

    # suffled the data
    x_shuffled, y_shuffled = randomly_shuffle_data(x, y)

    # break data in train and dev
    x_train, x_dev, y_train, y_dev = train_test(x_shuffled, y_shuffled, len(y))
    del x, y, x_shuffled, y_shuffled

    # Training
    # ==================================================
    FLAGS = tf.flags.FLAGS

    with tf.Graph().as_default():

        session_conf = tf.ConfigProto(
            allow_soft_placement=FLAGS.allow_soft_placement,
            log_device_placement=FLAGS.log_device_placement)

        with tf.Session(config=session_conf) as sess:
            cnn = TextCNN(
                sequence_length=pretraitement.max_size,
                num_classes=nb_classes,
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
            check_path="./runs/"+timestamp+"/checkpoints/"
            print(check_path)
            f = open('./data/checkPath', 'w')
            f.write(check_path)  # python will convert \n to os.linesep
            f.close()
            print("Writing to {}\n".format(out_dir))

            # Summaries for loss and accuracy
            dev_summary_writer, train_summary_writer, dev_summary_op, train_summary_op \
                = create_summaries(cnn, out_dir, sess)

            # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
            checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
            checkpoint_prefix = os.path.join(checkpoint_dir, "model")
            if not os.path.exists(checkpoint_dir):
                os.makedirs(checkpoint_dir)
            saver = tf.train.Saver(tf.global_variables(), max_to_keep=num_checkpoints)

            # Initialize all variables
            sess.run(tf.global_variables_initializer())

            # Generate batches
            batches = batch_iter(list(zip(x_train, y_train)), batch_size, num_epochs)

            # Training loop. For each batch...
            for batch in batches:
                x_batch, y_batch = zip(*batch)
                train_step(x_batch, y_batch, cnn, FLAGS
                           , sess, train_op, global_step, train_summary_op, train_summary_writer)
                current_step = tf.train.global_step(sess, global_step)
                if current_step % evaluate_every == 0:
                    print("\nEvaluation:")
                    dev_step(x_dev, y_dev, cnn, sess, global_step, dev_summary_op, writer=dev_summary_writer)
                    print("")
                if current_step % checkpoint_every == 0:
                    path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                    print("Saved model checkpoint to {}\n".format(path))

    return True


def get_data_from_database(db_manager):
    """
    Get the data for the training in the database, create a dictionaire for the
    correspondance between id_field in the database and the output of the cnn
    :param db_manager:
    :return:
    """
    print("data recuperation")
    predictions = db_manager.get_all_offers_with_field_in_base()
    x, y = [], []
    i = 0
    for p in predictions:
        #print(i)
        i += 1
        x.append(string_to_descripteur(p[0]))
        y.append(p[1])

    dic_cores, nb_classes = create_cores_id_field(db_manager)
    y = change_y(dic_cores, y)
    #print(dic_cores)
    del predictions
    return x, y, dic_cores, nb_classes


def string_to_descripteur(chaine):
    """
    Convert the chaine into a array of descriptor
    :param chaine: a string for the descriptor of an offers
    :return: the list of the descritor(array of float)
    """
    chaine = chaine\
        .decode("utf-8")\
        .replace("[", "")\
        .replace("]", "")\
        .replace("\n", "")\
        .replace("\r", "")\
        .replace("  ", " ")\
        .rstrip().split(',')

    list_descripteur = []
    for c in chaine:
        c = c.rstrip().split(' ')
        descripteur = []
        for vec in c:
            if not(vec == ""):
                f = float(vec)
                descripteur.append(f)
        list_descripteur.append(descripteur)
    return list_descripteur

def create_cores_id_field(db_manager):
    """
    Create a correspondance between id_field in the database and output of the cnn
    :param db_manager: manager
    :return: a dictionaire with the corepondance
    """
    id_field = db_manager.get_all_id_field()
    nb_classes = len(list(id_field))
    print(nb_classes)
    dic = dict()
    for i in range(0, nb_classes):
        ten = np.zeros(nb_classes, int)
        ten[i] = 1
        dic[id_field[i][0]] = ten
    return dic , nb_classes
#{1: array([0, 1, 0]), 2: array([0, 0, 1]), 3: array([1, 0, 0])}

def change_y(dic_cores, y):
    """
    :param dic_cores: dict
    :param y: list of int
    :return: list of descriptor
    """
    fields = []
    for field in y:
        fields.append(dic_cores[field])
    return fields


def train_step(x_batch, y_batch, cnn, FLAGS, sess, train_op, global_step, train_summary_op, train_summary_writer):
    """
    A single training step

    """
    feed_dict = {
        cnn.input_x: x_batch,
        cnn.input_y: y_batch,
        cnn.dropout_keep_prob: FLAGS.dropout_keep_prob

    }

    _, step, summaries, loss, accuracy = sess.run(
        [train_op, global_step, train_summary_op, cnn.loss, cnn.accuracy],
        feed_dict)
    time_str = datetime.datetime.now().isoformat()
   # print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))
    train_summary_writer.add_summary(summaries, step)


def dev_step(x_batch, y_batch, cnn, sess, global_step, dev_summary_op, writer=None):
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
    num_batches_per_epoch = int((len(data) - 1) / batch_size) + 1
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


def randomly_shuffle_data(x, y):
    """ Randomly shuffle data """
    np.random.seed(10)
    shuffle_indices = np.random.permutation(np.arange(len(y)))
    # print(shuffle_indices)
    x_shuffled = np.array(list(x))[shuffle_indices]
    y_shuffled = np.array(list(y))[shuffle_indices]
    return x_shuffled, y_shuffled


def train_test(x_shuffled, y_shuffled, len_y):
    """ train/test"""
    dev_sample_index = -1 * int(.1 * float(len_y))
    x_train, x_dev = x_shuffled[:dev_sample_index], x_shuffled[dev_sample_index:]
    y_train, y_dev = y_shuffled[:dev_sample_index], y_shuffled[dev_sample_index:]
    print("descriptor size: %s" % len(x_train[0]))
    # cross validation
    # k = 10
    # cut_size = len(x_shuffled) / k
    print("Train/Dev split: {:d}/{:d}".format(len(y_train), len(y_dev)))
    return x_train, x_dev, y_train, y_dev


def create_summaries(cnn, out_dir, sess):
    """ Summaries for loss and accuracy"""
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
    return dev_summary_writer, train_summary_writer, dev_summary_op, train_summary_op

def def_flags():
    """def the flags"""
    # Data loading params
    tf.flags.DEFINE_float("dev_sample_percentage", .1, "Percentage of the training data to use for validation")
    tf.flags.DEFINE_string("positive_data_file", "./data/rt-polaritydata/rt-polarity.pos",
                           "Data source for the positive data.")
    tf.flags.DEFINE_string("negative_data_file", "./data/rt-polaritydata/rt-polarity.neg",
                           "Data source for the negative data.")

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
