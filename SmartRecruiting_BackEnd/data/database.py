"""
Initializes the connection with the remote database, creates tables if necessary
and generates the session.

Created on Fri Feb 24 22:44:09 2017
@author: Julian
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql


DB_NAME = "deeplearning1"

DB_CONFIG_DICT = { "database" : DB_NAME,
                   "user" : "root", 
                   "password" : "root", 
                   "host" : "localhost",
                   "port" : "3306" }

DB_CONN_FORMAT = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

DB_OPTIONS = "?charset=utf8&use_unicode=0"                     


engine = create_engine((DB_CONN_FORMAT+DB_OPTIONS).format(**DB_CONFIG_DICT), pool_recycle=60)

dbSession = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = dbSession.query_property()

def initDb():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)