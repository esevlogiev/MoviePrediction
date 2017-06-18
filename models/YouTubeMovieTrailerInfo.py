from sqlalchemy import UniqueConstraint, Column, Integer, String, Float, ForeignKey
from models.Base import Base
from models.YouTubeMovieComments import YouTubeMovieComments
from sqlalchemy.orm import relationship

class YouTubeMovieTrailerInfo(Base):
    __tablename__ = 'YouTubeMovieTrailerInfo'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    year = Column('year', Integer)
    likeCount = Column('likeCount', Integer)
    dislikeCount = Column('dislikeCount', Integer)
    viewCount = Column('viewCount', Integer)
    commentCount = Column('commentCount', Integer)
    url = Column('urlOfMovieTrailer', String)
   
    __table_args__ = (UniqueConstraint('name', 'year', name='name_year_unique'),)
    you_tube_comments_info = relationship('YouTubeMovieComments', uselist=True, lazy='joined', foreign_keys=[name,year],
            primaryjoin='YouTubeMovieComments.name == YouTubeMovieTrailerInfo.name and YouTubeMovieComments.year == YouTubeMovieTrailerInfo.year')

    def __init__(self, name, year, likeCount, dislikeCount, viewCount, commentCount, urlOfMovieTrailer):
        self.name = name
        self.year = year
        self.likeCount = likeCount
        self.dislikeCount = dislikeCount
        self.viewCount = viewCount
        self.commentCount = commentCount
        self.url = urlOfMovieTrailer





    def __repr__(self):
        return "<YouTubeMovieTrailerInfo(name='%s', likesCount='%d', viewCount='%d'), dislikeCount='%d' >" % (
            self.name, self.likeCount, self.viewCount, self.dislikeCount)        
    