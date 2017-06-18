import postgresql
from db_manager import DBManager
from constants import Constants

def generate_select_query():
	fields = [
		'id', 'name', 'year', 'director', 'duration',
		'rating', 'users_votes', 'budget', 'opening_revenue',
		'total_revenue', 'motion_picture_rating', 'release_date',
		'genres', 'studios', 'cast_names', 'countries']

	return 'SELECT {0} FROM movies WHERE {1} IS NOT NULL'.format(
		', '.join(fields), ' || '.join(fields))

def migrate():
	conn = postgresql.open(Constants.postgresql_movie_connection)
	query = conn.prepare(generate_select_query())
	entries = query()

	for entry in entries:
		DBManager.insert_movie(
			id = entry[0],
		    name = entry[1],
		    year = entry[2],
		    director = entry[3],
		    duration = entry[4],
		    rating = entry[5],
		    users_votes = entry[6],
		    budget = entry[7],
		    opening_revenue = entry[8],
		    total_revenue = entry[9],
		    motion_picture_rating = entry[10],
		    release_date = entry[11],
		    genres = entry[12].split(';'),
		    studios = entry[13].split(';'),
		    cast = entry[14].split(';'),
		    countries = entry[15].split(';'))


migrate()