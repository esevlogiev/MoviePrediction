import tensorflow as tf
import numpy as np
from sklearn.preprocessing import StandardScaler

from constants import Constants

class GDOptimizer:
    def __init__(self, learning_rate=0.001, num_training_iter=500, features_dim=Constants.features_count):
        self.learning_rate = learning_rate
        self.num_training_iter = num_training_iter
        self.features_dim = features_dim
        self.W = tf.Variable(tf.random_uniform([Constants.features_count, 1], -1, 1, dtype=np.float32, seed=0),
            name="weight")
        self.b = tf.Variable(tf.random_uniform([1], -1, 1, dtype=np.float32, seed=0), name="bias")
        init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init)

    def train(self, train_features, train_target_values):
        self.scaler = StandardScaler().fit(train_features)
        normalized_train_features = self.scaler.transform(train_features)
        train_samples_count = len(train_features)

        tf_features = tf.placeholder(tf.float32, [train_samples_count, self.features_dim])
        tf_ratings = tf.placeholder(tf.float32, [train_samples_count, 1])

        tf_rating_pred = tf.add(tf.matmul(tf_features, self.W), self.b)
        tf_cost = tf.reduce_sum(tf.square(tf_rating_pred - tf_ratings)) / (2*train_samples_count)

        optimizer = tf.train.GradientDescentOptimizer(self.learning_rate).minimize(tf_cost)

        display_every = 2
        sess = self.sess

        for iteration in range(self.num_training_iter):
            sess.run(optimizer, feed_dict={tf_features: train_features, tf_ratings: train_target_values})

            if (iteration + 1) % display_every == 0:
                c = sess.run(tf_cost, feed_dict={tf_features: train_features, tf_ratings: train_target_values})
                print("iteration #: ", '%04d' % (iteration + 1), "cost = ", "{:.9f}".format(c), \
                    "Weights = ", sess.run(self.W), "bias = ", sess.run(self.b))#,

        print("Optimization Finished!")
        training_cost = sess.run(tf_cost, feed_dict={tf_features: train_features,
            tf_ratings: train_target_values})
        print("Training cost =", training_cost, "Weights = ", sess.run(self.W), "bias = ",
            sess.run(self.b), '\n')

        return dict([('mse', training_cost)])

    def predict(self, new_inputs, new_target_values):
        normalized_new_inputs = self.scaler.transform(new_inputs)
        predictions = []
        for (X, y) in zip(new_inputs, new_target_values):
            predict_X = np.array(X, dtype=np.float32).reshape((1, self.features_dim))
            predicted_value = tf.add(tf.matmul(predict_X, self.W), self.b)
            predictions.append([y, self.sess.run(predicted_value)])
            print('Predicted value: {0}  Real value: {1}'.format(self.sess.run(predicted_value), y))

        mse = sum([(real_value - pred) ** 2 
            for [real_value, pred] in predictions]) / (2 * len(predictions))

        return dict([ ('mse', mse),
            ('predictions', predictions)])