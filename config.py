from os import environ

class Config:
	postgres_user = environ.get('postgres_user')
	postgres_password = environ.get('postgres_password')
	postgres_host = environ.get('postgres_host')
	postgres_port = environ.get('postgres_port')
	postgres_database = environ.get('postgres_database')
