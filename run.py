import math

from db_manager import DBManager
from feature_extraction import RatingFeatures
from constants import Constants

from regression_tree import RegressionTree
from wide_neural_network import WideNN
from gradient_descent_prediction import GDOptimizer

from predictions_estimator import PredictionsEstimator

def get_data(is_rating=True):
	movies = DBManager.get_movies()
	movies_count = len(movies)
	train_data_ratio = Constants.train_rating_data_ratio if is_rating else 0
	train_samples_count = math.floor(movies_count * train_data_ratio)

	features_model = RatingFeatures if is_rating else None

	train_features_model = features_model(movies[:train_samples_count])
	test_features_model = features_model(movies[train_samples_count:])

	return dict([
		('train', dict([('features', train_features_model.get_features()),
						('raitings', train_features_model.get_ratings())])),
		('test', dict([('features', test_features_model.get_features()),
						('raitings', test_features_model.get_ratings())]))
	])

def test_predictions(model, is_rating=True):
	data = get_data(is_rating)
	train_data, test_data = data['train'], data['test']
	estimator = PredictionsEstimator(model)

	train_predictions = estimator.train(train_data['features'], train_data['raitings'])
	test_predictions = estimator.predict(test_data['features'], test_data['raitings'])

	print('Train MSE: {0}	Test MSE: {1}'.format(train_predictions['mse'],
		test_predictions['mse']))

def main(model_name):
	models = {
        'gradient_descent': GDOptimizer(),
        'neural_network': WideNN(),
        'regression_tree': RegressionTree()
    }

	model = models.get(model_name)
	test_predictions(model)

main('gradient_descent')