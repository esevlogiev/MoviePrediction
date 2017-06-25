from sklearn import tree
from sklearn.preprocessing import StandardScaler

from constants import Constants

class RegressionTree:
	def __init__(self, features_dim=Constants.features_count):
		self.features_dim = features_dim
		self.regressionTree = tree.DecisionTreeRegressor()

	def mean_squared_error(self, predictions, real_values):
		predictions_len = len(predictions)

		return sum([(pred - real_value) ** 2 
			for (pred, real_value) in zip(predictions, real_values)]) / (2 * predictions_len)

	def train(self, train_features, train_target_values):
		self.scaler = StandardScaler().fit(train_features)
		normalized_train_features = self.scaler.transform(train_features)
		self.regressionTree = self.regressionTree.fit(normalized_train_features, train_target_values)

		return self.predict(train_features, train_target_values)
			
	def predict(self, new_inputs, new_target_values):
		normalized_new_inputs = self.scaler.transform(new_inputs)
		predictions = self.regressionTree.predict(normalized_new_inputs)

		return dict([ ('mse', self.mean_squared_error(predictions, new_target_values)),
			('predictions', [[real_value, predicted_value] for (real_value, predicted_value) 
			in zip(new_target_values, predictions)])])
		