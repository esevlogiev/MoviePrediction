from sqlalchemy import UniqueConstraint, Table, Column, Integer, String, Float, ForeignKey
from models.Base import Base
from sqlalchemy.orm import relationship


class Tweet(Base):
  
  __tablename__ = 'tweets'
  id = Column('id', Integer, primary_key=True)
  name = Column('name', String)
  year = Column('year', Integer)
  text = Column('text', String)
  sentiment = Column('sentiment', String)

  def __repr__(self):
    return "<Tweet(name='%s', text='%s', sentiment='%s')>" % (
      self.name, self.text, self.sentiment)


  def __init__(self, name, year, text, sentiment):
    self.name = name
    self.year = year
    self.text = text
    self.sentiment = sentiment
