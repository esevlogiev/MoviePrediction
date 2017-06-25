from services.GetDataFromYouTube import *
from services.TwitterClient import *
from models.Movie import Movie
from models.YouTubeMovieComments import YouTubeMovieComments
from models.YouTubeMovieTrailerInfo import YouTubeMovieTrailerInfo 
from models.Tweet import Tweet
import datetime
class MovieService:

  def __init__(self, you_tube_api_key, twitter_api_keys):
    self.you_tube_api = GetDataFromYouTube(you_tube_api_key)
    self.twitter_api = TwitterClient(*twitter_api_keys)
    self.twitter_apis = [self.twitter_api]
    self.current_twitter_api = self.twitter_api

  def get_data_for_movie(self, movie):
    release_date = datetime.datetime.strptime(movie.release_date, '%d %B %Y')
    published_before_date = datetime.date.strftime(release_date, "%Y-%m-%dT00:00:00Z")
    if movie.you_tube_trailer_info == None:
      you_tube_data = self.you_tube_api.get_info_for_movie(movie.name, movie.year, published_before_date)
      if you_tube_data:
        movie.you_tube_trailer_info = self.get_data_from_you_tube(movie, you_tube_data)
    # see original tweet
    # print(self.twitter_api.get_tweets(query = movie.name + ' Movie', count = 200))
    if not movie.tweets:
      movie.tweets = self.get_tweets_with_sentiment(movie)

    if not movie.tweets and not not movie.you_tube_trailer_info:
      print("There is a problem with " + movie.name + ' ' + str(movie.id))
    return movie

  def get_comments_from_you_tube(self, movie, you_tube_data):
    comments = []
    comments_from_you_tube = you_tube_data['comments'] 
    if not comments_from_you_tube:
      comments_from_you_tube = []
    for comment in comments_from_you_tube:
      comments.append(YouTubeMovieComments(
        movie.name,
        movie.year,
        comment['text'],
        comment['likeCount'],
        comment['totalReplyCount'],
        comment['publishedAt']
      ))
    return comments

  def get_data_from_you_tube(self, movie, you_tube_data):
    view_count = you_tube_data['video_data'].get('viewCount')
    you_tube_trailer_info = YouTubeMovieTrailerInfo(
      movie.name,
      movie.year,
      int(you_tube_data['video_data']['likeCount']),
      int(you_tube_data['video_data']['dislikeCount']),
      int(view_count if view_count else -1),
      int(you_tube_data['video_data']['commentCount']),
      str(you_tube_data)
    )
    you_tube_trailer_info.you_tube_comments_info = self.get_comments_from_you_tube(movie, you_tube_data)
    return you_tube_trailer_info

  def get_tweets_with_sentiment(self, movie):
    tweets = []
    data_from_tweeter = self.current_twitter_api.get_tweets(query = movie.name + ' Movie', count = 200)
    if not data_from_tweeter:
      for api in self.twitter_apis:
        self.current_twitter_api = api
        data_from_tweeter = self.current_twitter_api.get_tweets(query = movie.name + ' Movie', count = 200)
        if data_from_tweeter:
          break
    if not data_from_tweeter:
      data_from_tweeter = []
    for tweet in data_from_tweeter:
      tweets.append(Tweet(
        movie.name,
        movie.year,
        tweet['text'],
        tweet['sentiment']
      ))
    return tweets;






