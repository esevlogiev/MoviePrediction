from services.GetDataFromYouTube import *
from services.TwitterClient import *
from models.Movie import Movie
from models.YouTubeMovieComments import YouTubeMovieComments
from models.YouTubeMovieTrailerInfo import YouTubeMovieTrailerInfo 
from models.Tweet import Tweet

class MovieService:

  def __init__(self, you_tube_api_key, twitter_api_keys):
    self.you_tube_api = GetDataFromYouTube(you_tube_api_key)
    self.twitter_api = TwitterClient(*twitter_api_keys)

  def get_data_for_movie(self, movie):
    if movie.you_tube_trailer_info == None:
      you_tube_data = self.you_tube_api.get_info_for_movie(movie.name)
      if you_tube_data:
        movie.you_tube_trailer_info = self.get_data_from_you_tube(movie, you_tube_data)
    # see original tweet
    # print(self.twitter_api.get_tweets(query = movie.name + ' Movie', count = 200))
    if not movie.tweets:
      movie.tweets = self.get_tweets_with_sentiment(movie)

    if not movie.tweets and not not movie.you_tube_trailer_info:
      print("There is a problem with " + movie.name + ' ' + movie.id)
    return movie

  def get_comments_from_you_tube(self, movie, you_tube_data):
    comments = []
    for comment in you_tube_data['comments']:
      comments.append(YouTubeMovieComments(
        movie.name,
        movie.year,
        comment['text'],
        comment['likeCount'],
        comment['totalReplyCount']
      ))
    return comments

  def get_data_from_you_tube(self, movie, you_tube_data):
    you_tube_trailer_info = YouTubeMovieTrailerInfo(
      movie.name,
      movie.year,
      int(you_tube_data['video_data']['likeCount']),
      int(you_tube_data['video_data']['dislikeCount']),
      int(you_tube_data['video_data']['viewCount']),
      int(you_tube_data['video_data']['commentCount']),
      str(you_tube_data)
    )
    you_tube_trailer_info.you_tube_comments_info = self.get_comments_from_you_tube(movie, you_tube_data)
    return you_tube_trailer_info

  def get_tweets_with_sentiment(self, movie):
    tweets = []
    for tweet in self.twitter_api.get_tweets(query = movie.name + ' Movie', count = 200):
      tweets.append(Tweet(
        movie.name,
        movie.year,
        tweet['text'],
        tweet['sentiment']
      ))
    return tweets;






