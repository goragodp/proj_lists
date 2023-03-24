from cProfile import label
from pickletools import optimize
import sklearn

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
from numpy import argmax, genfromtxt
from sklearn import datasets

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score, f1_score

import pandas as pd
import matplotlib.pyplot as plt

import warnings
# warnings.filter("ignore")
np.set_printoptions(threshold=np.inf)

learning_rate = 0.001
IMG_W = 600
IMG_H = 600
n_class = 2
n_input = 600 * 600 * 3
n_epochs = 200000
batch_size = 128
display_step = 10

from PIL import Image
import glob

train = []
labels = []

#open image
files = sorted(glob.glob("x_train_data_resize*"))

for f in files:
    img = Image.open(f)
    img = np.array(img)
    print(img.shape)

    conv = img.reshape(img.shape[0] * img.shape[1] * img.shape[2])
    print(conv.shape)

    train.append(conv)
    labels.append(1)

# Getting Data
train = np.array(train, dtype="float32")
labels = np.array(labels, dtype="float32")

print(train.shape)
print(labels.shape)

x_all = train
labels_all = labels 

x_train, x_test, y_train, y_test = train_test_split(x_all, labels_all, test_size=0.20, random_state=42)



accuracy_score_list = []
precision_score_list = []
def print_stat_matrics(y_test, y_pred):
    print("Accuracy: %.2f" % accuracy_score(y_test, y_pred))
    accuracy_score_list.append(accuracy_score(y_test, y_pred))
    confmat = confusion_matrix(y_true=y_test, y_pred=y_pred)
    print("Confusion Matrix")
    print(confmat)

    print(pd.corsstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margin=True))
    precision_score_list.append(precision_score(y_true=y_test, y_pred=y_pred, average='weigth'))
    print("Precision: %.3f" % precision_score(y_true=y_test, y_pred=y_pred, average='weigth'))
    print("Recall: %.3f" % recall_score(y_true=y_test, y_pred=y_pred, average='weigth'))
    print("F1-score: %.3f" % f1_score(y_true=y_test, y_pred=y_pred, average='weigth'))

def plot_matrix_per_epoch():
    x_epochs = []
    y_epochs = []

    for i, val in enumerate(accuracy_score_list):
        x_epochs.append(i)
        y_epochs.append(val)

    plt.scatter(x_epochs, y_epochs, s=50, c="lightgreen", marker="s", label="score")
    plt.xlabel("Epochs")
    plt.ylabel("Score")
    plt.title("Score / Epochs")
    plt.legend()
    plt.grid()
    plt.show()

def conv2d(x, W, b, strides=1):
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)

def maxpool2d(x, k=2):
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1], padding='SAME')

def layer(input, weigth_shape, bias_shape):
    W = tf.Variable(tf.random_normal(weigth_shape))
    b = tf.Variable(tf.random_normal(bias_shape))
    mapping = tf.matmul(input, W)
    result = tf.add(mapping, b)
    return result

def conv_layer(input, weigth_shape, bias_shape):
    W = tf.Variable(tf.random_normal(weigth_shape))
    b = tf.Variable(tf.random_normal(bias_shape))
    conv = conv2d(input, W, b)
    conv_max = maxpool2d(conv, k = 2)
    return conv

def fully_connect_layer(conv_input, fc_weigth_shape, fc_bias_shape, dropout):
    new_shape = [-1, tf.Variable(tf.random_normal(fc_weigth_shape)).get_shape().as_list()[0]]
    fc = tf.reshape(conv_input, new_shape)
    mapping = tf.matmul(fc, tf.Variable(tf.random_normal(fc_weigth_shape)))
    fc = tf.add(mapping, tf.Variable(tf.random_normal(fc_bias_shape)))
    fc = tf.nn.relu(fc)
    fc = tf.nn.dropout(fc, dropout)
    return fc


def inference_conv_net2(x, dropout):
    #shape = [-1, w, h, ch] // [-1, 600, 600, 3]
    #batchsize = 128
    #input is [128, 600*600*3]
    x =  tf.reshape(x, shape=[1, IMG_W, IMG_H, 3])

    # Layer 1, filter size 5x5 3 input (ch) and 32 output
    # maxpool k = 2, reduce img from 600x600 to 300x300
    conv1 = conv_layer(x, [5, 5, 3, 36], [36])

    conv2 = conv_layer(conv1, [5, 5, 16, 36], [36])

    fc = fully_connect_layer(conv2, [150*150*36, 1024], [1024], dropout)

    output = layer(fc, [1024, n_class], [n_class])

    return output

def loss_deep_conv_net(output, y_tf):
    xentropy  = tf.nn.softmax_cross_entropy_with_logits(logits=output, labels=y_tf)
    loss = tf.reduce_mean(xentropy)
    return loss

def trainning(cost):
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
    training_op = optimize.minimize(cost)
    return training_op

def evaluate(output, y_tf):
    correct_prediction = tf.equal(tf.argmax(output, 1), tf.argmax(y_tf, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    return accuracy

x_tf = tf.placeholder(tf.float32, [None, n_input])
y_tf = tf.placeholder(tf.float32, [None, n_class])
keep_prob = tf.placeholder(tf.float32)

output = inference_conv_net2(x_tf, keep_prob)
cost = loss_deep_conv_net(output, y_tf)

train_op = trainning(cost)
eval_op = evaluate(output, y_tf)

y_p_metrics = tf.argmax(output, 1)

init = tf.initialize_all_variable()
sess = tf.session()
sess.run(init)


#one-hot
depth = 2
y_train_onehot = sess.run(tf.one_hot(y_train, depth))
y_test_onehot = sess.run(tf.one_hot(y_test, depth))

#Batch param
num_sample_train = len(y_train)
num_batches = int(num_sample_train / batch_size)

dropout = 0.75



# for i in range(n_epochs):
#     for batch_n in range(num_batches):
#         sta = batch_n * batch_size
#         end = sta + batch_size

#         sess.run(train_op, feed_dict={x_tf: x_train[sta:end,:], y_tf:y_train_onehot[sta:end,:], keep_prob:dropout})
#         loss, acc = sess.run([cost, eval_op], feed_dict={x_tf:x_train[sta:end, :], y_tf: y_train_onehot, keep_prob:dropout})

#         result = sess.run([eval_op, y_p_metrics], feed_dict={x_tf:x_test, y_tf:y_test_onehot, keep_prob:dropout})

#         print("test1 {} {}".format(i, result))
#         y_true = np,argmax(y_test_onehot, 1)
#         print(y_true)
#         print_stat_matrics(y_true, y_pred)

        