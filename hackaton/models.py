from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(Text)
    email_addr = Column(Text)
    pswd_hash = Column(Text)
    respect = Column(Integer)

class games(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    game_name = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Integer)

class game_tag_rel(Base):
    __tablename__ = 'game_tag_rel'
    game_id = Column(Integer, ForeignKey('games.id'), primary_key = True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key = True)

class game_user_rel(Base):
    __tablename__ = "game_user_rel"
    game_id = Column(Integer, ForeignKey('games.id'), primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key = True)

class tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key = True)
    tag = Column(Text)
    counter = Column(Integer)

class data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    value_1 = Column(Text)
    value_2 = Column(Text)

Index('tag_uniq', tags.tag, unique=True, mysql_length=25)
