import numpy
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler

from constants import Constants

class WideNN:
	def __init__(self, input_dim = Constants.features_count, hidden_layer_dim = 20,
		activation='relu', loss='mean_squared_error', optimizer='adam'):
		self.input_dim = input_dim
		self.hidden_layer_dim = hidden_layer_dim

		self.model = Sequential()
		self.model.add(Dense(self.hidden_layer_dim, input_dim=self.input_dim,
			kernel_initializer='normal', activation=activation))
		self.model.add(Dense(1, kernel_initializer='normal'))
		self.model.compile(loss=loss, optimizer=optimizer)

	def train(self, features, target_values, batch_size=10, epochs=100):
		self.scaler = StandardScaler().fit(features)
		normalized_features = self.scaler.transform(features)
		history = self.model.fit(normalized_features, target_values, batch_size=batch_size, epochs=epochs)

		return dict([('mse', history.history['loss'][-1])])

	def predict(self, test_features, test_target_values):
		normalized_test_features = self.scaler.transform(test_features)
		mse = self.model.evaluate(normalized_test_features, test_target_values)
		predictions = self.model.predict(normalized_test_features)

		return dict([ ('mse', mse),
			('predictions', [[real_value, predicted_value] for (real_value, predicted_value) 
			in zip(test_target_values, predictions)])])

	def predict_unknown(self, new_inputs):
		normalized_new_inputs = self.scaler.transform(new_inputs)
		predictions = self.model.predict(normalized_new_inputs)
		print(predictions)
		return predictions
		