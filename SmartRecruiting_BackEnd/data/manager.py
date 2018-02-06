"""
Manager to interact with the database

Created on Sun Feb 26 16:23:02 2017
@author: Julian
"""

from SmartRecruiting_BackEnd.data.models import Formation
from SmartRecruiting_BackEnd.data.database import initDb, dbSession as db
from sqlalchemy.orm import join


class DatabaseManager():
    
    def __init__(self):
        """
            initialize the database, creates tables if not exists
        """
        initDb()
        
    def getAllFormations(self):
        formations = Formation.query.all()
        f = formations[0]
        return [f.serialize() for f in formations]
