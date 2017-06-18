import tensorflow as tf
import numpy as np
import math

from db_manager import DBManager
from feature_extraction import RatingFeatures
from constants import Constants

rating_features = RatingFeatures(DBManager.get_movies())
movies_count = rating_features.get_movies_count()
features = rating_features.get_features()
ratings = rating_features.get_ratings()


train_samples_count = math.floor(movies_count * 0.7)
train_features = features[:train_samples_count]
train_ratings = ratings[:train_samples_count]

test_features = features[train_samples_count:]
test_ratings = ratings[train_samples_count:]

tf_features = tf.placeholder(tf.float32, [train_samples_count, Constants.features_count])
tf_ratings = tf.placeholder(tf.float32, [train_samples_count, 1])

W = tf.Variable(tf.zeros([1, Constants.features_count], dtype=np.float32), name="weight")
b = tf.Variable(tf.zeros([1], dtype=np.float32), name="bias")

tf_rating_pred = tf.add(tf.multiply(tf_features, W), b)


tf_cost = tf.reduce_sum(tf.pow(tf_rating_pred - tf_ratings, 2)) / (2 * train_samples_count)

learning_rate = 0.01;

optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(tf_cost)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    display_every = 2
    num_training_iter = 1000

    for iteration in range(num_training_iter):
        sess.run(optimizer, feed_dict={tf_features: train_features, tf_ratings: train_ratings})

        if (iteration + 1) % display_every == 0:
            c = sess.run(tf_cost, feed_dict={tf_features: train_features, tf_ratings: train_ratings})
            print("iteration #: ", '%04d' % (iteration + 1), "cost = ", "{:.9f}".format(c), \
                "Weights = ", sess.run(W), "bias = ", sess.run(b))

    print("Optimization Finished!")
    training_cost = sess.run(tf_cost, feed_dict={tf_features: train_features, tf_ratings: train_ratings})
    print("Trained cost=", training_cost, "Weights = ", sess.run(W), "bias = ", sess.run(b), '\n')
