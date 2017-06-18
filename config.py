from os import environ

class Config:
	postgres_user = environ.get('postgres_user')
	postgres_password = environ.get('postgres_password')
	postgres_host = environ.get('postgres_host')
	postgres_port = environ.get('postgres_port')
	postgres_database = environ.get('postgres_database')
	
	# Twitter api keys
	consumer_key = environ.get('consumer_key')
	consumer_secret = environ.get('consumer_secret')
	access_token = environ.get('access_token')
	access_token_secret = environ.get('access_token_secret')

	# YouTube api keys
	youtube_api_key = environ.get('youtube_api_key')
