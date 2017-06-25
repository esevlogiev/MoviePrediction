from config import Config
from services.MovieService import MovieService
from db_manager import DBManager


class FeedTwitterAndYoutubeData:
  
  def feed():
    movieService = MovieService(Config.youtube_api_key, [
      Config.consumer_key,
      Config.consumer_secret,
      Config.access_token,
      Config.access_token_secret])
    return [movieService.get_data_for_movie(movie) for movie in DBManager.get_movies()[:3]]


