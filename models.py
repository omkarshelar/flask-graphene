from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()

class Users(Base):
	__tablename__='users'
	id = Column(Integer, primary_key=True)
	firstName = Column(String)
	lastName = Column(String)
	username = Column(String)
	email = Column(String)

'''class Posts(Base):
	__tablename__='posts'
	id = Column(Integer, primary_key=True)
	title = Column(String)
	post_by = Column(Integer, ForeignKey('users.id'))
	content = Column(Text)'''

class Follows(Base):
	__tablename__='follows'
	id = Column(Integer, primary_key=True)
	follow_by = Column(Integer, ForeignKey('users.id'))
	follow_to = Column(Integer, ForeignKey('users.id'))
