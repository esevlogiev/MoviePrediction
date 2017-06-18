from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.Base import Base
from models.Movie import Movie
from constants import Constants
print (Constants.sqlalchemy_movie_connection)
class DBManager:
	engine = create_engine(Constants.sqlalchemy_movie_connection)
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()

	def create_all_tables():
		Base.metadata.create_all(DBManager.engine)

	def insert_movie(**fields):
		movie = Movie(
			fields.get('id'),
		    fields.get('name'),
		    fields.get('year'),
		    fields.get('director'),
		    fields.get('duration'),
		    fields.get('rating'),
		    fields.get('users_votes'),
		    fields.get('budget'),
		    fields.get('opening_revenue'),
		    fields.get('total_revenue'),
		    fields.get('motion_picture_rating'),
		    fields.get('release_date'),
		    fields.get('genres'),
		    fields.get('studios'),
		    fields.get('cast'),
		    fields.get('countries'))

		DBManager.session.add(movie)
		DBManager.session.commit()

	def get_movies():
		return DBManager.session.query(Movie).all()

	def get_movies_by_actor(actor_name):
		return DBManager.session.query(Movie).filter(Movie.cast.any(actor_name)).all()

	def get_movies_by_director(director_name):
		return DBManager.session.query(Movie).filter(Movie.director == director_name).all()

	def get_all_genres():
		movies_genres = [movie.genres for movie in DBManager.session.query(Movie).all()]
		return list(set([genre for current_movie_genres in movies_genres for genre in current_movie_genres]))

	def get_movies_by_genre(genre):
		return DBManager.session.query(Movie).filter(Movie.genres.any(genre)).all()

	def get_movies_by_mpaa(mpaa):
		return DBManager.session.query(Movie).filter(Movie.motion_picture_rating == mpaa).all()
