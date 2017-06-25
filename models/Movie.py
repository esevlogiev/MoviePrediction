from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, ARRAY, SMALLINT
from models.Base import Base
from sqlalchemy.orm import relationship
from models.Tweet import Tweet

class Movie(Base):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    year = Column(SMALLINT, nullable=False)
    director = Column(String(100), nullable=False)
    duration = Column(SMALLINT, nullable=False)
    rating = Column(Float, nullable=False)
    users_votes = Column(Integer, nullable=False)
    budget = Column(String(50), nullable=False)
    opening_revenue = Column(String(50), nullable=False)
    total_revenue = Column(String(50), nullable=False)
    motion_picture_rating = Column(String(20), nullable=False)
    release_date = Column(String(20), nullable=False)
    genres = Column(ARRAY(String(20), dimensions=1), nullable=False)
    studios = Column(ARRAY(String(100), dimensions=1), nullable=False)
    cast = Column(ARRAY(String(100), dimensions=1), nullable=False)
    countries = Column(ARRAY(String(50), dimensions=1), nullable=False)

    # you_tube_trailer_info = relationship('YouTubeMovieTrailerInfo', foreign_keys=[name,year],
    #         primaryjoin='Movie.name == YouTubeMovieTrailerInfo.name and Movie.year == YouTubeMovieTrailerInfo.year')

    # tweets = relationship('Tweet', uselist=True, lazy='joined', foreign_keys=[name,year],
    #         primaryjoin='Tweet.name == Movie.name and Movie.year == Tweet.year')

    # def __repr__(self):
    #     return "<User(name='%s', fullname='%d', password='%s')>" % (
    #         self.name, self.year, self.genres)

    def __init__(self, id, name, year, director, duration, rating,
        users_votes, budget, opening_revenue, total_revenue, motion_picture_rating,
        release_date, genres, studios, cast, countries):
        self.id = id
        self.name = name
        self.year = year
        self.director = director
        self.duration = duration
        self.rating = rating
        self.users_votes = users_votes
        self.budget = budget
        self.opening_revenue = opening_revenue
        self.total_revenue = total_revenue
        self.motion_picture_rating = motion_picture_rating
        self.release_date = release_date
        self.genres = genres
        self.studios = studios
        self.cast = cast
        self.countries = countries

