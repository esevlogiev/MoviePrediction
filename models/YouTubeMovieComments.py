from sqlalchemy import UniqueConstraint, Table, Column, Integer, String, Float, ForeignKey
from models.Base import Base

class YouTubeMovieComments(Base):
    __tablename__ = 'YouTubeMovieComments'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    year = Column('year', Integer)
    text = Column('text', String)
    likeCount = Column('likeCount', Integer)
    totalReplyCount = Column('totalReplyCount', Integer)
    publishData = Column('publishData', String)

    def __init__(self, name, year, text, likeCount, totalReplyCount, publishData):
        self.name = name
        self.year = year
        self.text = text
        self.likeCount = likeCount
        self.totalReplyCount = totalReplyCount
        self.publishData = publishData