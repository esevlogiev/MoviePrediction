class PredictionsEstimator:
	def __init__(self, model):
		self.model = model

	def train(self, train_features, target_values):
		return self.model.train(train_features, target_values)

	def predict(self, test_features, target_values):
		return self.model.predict(test_features, target_values)