from config import Config

class Constants:
	sqlalchemy_movie_connection = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
		user = Config.postgres_user,
		password = Config.postgres_password,
		host = Config.postgres_host,
		port = Config.postgres_port,
		database = Config.postgres_database)

	postgresql_movie_connection = 'pq://{user}:{password}@{host}:{port}/{database}'.format(
		user = Config.postgres_user,
		password = Config.postgres_password,
		host = Config.postgres_host,
		port = Config.postgres_port,
		database = Config.postgres_database)

	features_count = 8
	main_cast_count = 5
	train_rating_data_ratio = 0.7

	rating_features = {
		'youtube': False,
		'duration': False,
		'budget': False
	}