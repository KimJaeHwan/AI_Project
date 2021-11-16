
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import tensorflow as tf

import numpy as np
import pandas as pd


class Classifiers():

	def __init__(self, X, Y):

 		self.x_train, self.x_test, self.y_train, self.y_test = \
 		train_test_split(X, Y, test_size=0.2, random_state=0)


	def do_svm(self):
		clf = SVC()
		clf.fit(self.x_train, self.y_train)
		y_pred = clf.predict(self.x_test)

		return accuracy_score(self.y_test, y_pred)

	def do_randomforest(self, mode):

		clf = RandomForestClassifier()
		clf.fit(self.x_train, self.y_train)

		if mode == 1:
			return clf.feature_importances_
		y_pred = clf.predict(self.x_test)

   		return accuracy_score(self.y_test, y_pred)

	def do_naivebayes(self):
		clf = clf = GaussianNB()
		clf.fit(self.x_train, self.y_train)
		y_pred = clf.predict(self.x_test)

		return accuracy_score(self.y_test, y_pred)


	def do_dnn(self):

		if "Series" in str(type(self.y_train)):
			self.y_train = self.y_train.to_frame()
			self.y_test = self.y_test.to_frame()
			input_len = len(self.x_train.columns)
		else:
			self.y_train = self.y_train.reshape(len(self.y_train), 1)
			self.y_test = self.y_test.reshape(len(self.y_test), 1)
			input_len = np.size(self.x_train, 1)

		learning_rate = 0.001
		batch_size = 128
		training_epochs = 50
		keep_prob = 0.5

		x_train = self.x_train
		y_train = self.y_train

		X = tf.placeholder(tf.float32, [None, input_len])
		Y = tf.placeholder(tf.float32, [None, 1])

		W1 = tf.Variable(tf.random_normal([input_len, 128]), name='weight1')
		b1 = tf.Variable(tf.truncated_normal([128]), name='bias1')
		L1 = tf.sigmoid(tf.matmul(X, W1) + b1)

		W2 = tf.Variable(tf.random_normal([128, 1024]), name='weight2')
		b2 = tf.Variable(tf.truncated_normal([1024]), name='bias2')
		L2 = tf.sigmoid(tf.matmul(L1, W2) + b2)
		L2 = tf.nn.dropout(L2, keep_prob)

		W3 = tf.Variable(tf.random_normal([1024, 1024]), name='weight2')
		b3 = tf.Variable(tf.truncated_normal([1024]), name='bias2')
		L3 = tf.sigmoid(tf.matmul(L2, W3) + b3)
		L3 = tf.nn.dropout(L3, keep_prob)

		W4 = tf.Variable(tf.random_normal([1024, 128]), name='weight4')
		b4 = tf.Variable(tf.truncated_normal([128]), name='bias4')
		L4 = tf.sigmoid(tf.matmul(L3, W4) + b4)

		W5 = tf.Variable(tf.random_normal([128, 1]), name='weight5')
		b5 = tf.Variable(tf.truncated_normal([1]), name='bias5')
		
		output = tf.sigmoid(tf.add(tf.matmul(L4, W5), b5))

		cost = -tf.reduce_mean(Y * tf.log(output) + (1 - Y) * tf.log(1 - output))
		train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

		predicted = tf.cast(output > 0.5, dtype=tf.float32)
		accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))

		with tf.Session() as sess:
			sess.run(tf.global_variables_initializer())

			for epoch in range(training_epochs):
				avg_cost = 0
				total_batch = int(len(x_train) / batch_size)

				for i in range(total_batch-1):
					batch_xs = x_train[i*batch_size:(i+1)*batch_size]
					batch_ys = y_train[i*batch_size:(i+1)*batch_size]

				feed_dict = {X: batch_xs, Y: batch_ys}
				_ , c =sess.run([train, cost], feed_dict=feed_dict)
				avg_cost += c / total_batch
				print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.9f}'.format(avg_cost))

			acc =  sess.run(accuracy, feed_dict={X: self.x_test, Y: self.y_test})

		return acc


	def do_all(self):
		rns = []

		rns.append(self.do_svm())
		rns.append(self.do_randomforest(0))
		rns.append(self.do_naivebayes())
		rns.append(self.do_dnn())

		return rns
