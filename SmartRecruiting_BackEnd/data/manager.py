"""
Manager to interact with the database

Created on Sun Feb 26 16:23:02 2017
@author: Julian
"""

from SmartRecruiting_BackEnd.data.models import Program
from SmartRecruiting_BackEnd.data.database import initDb, dbSession as db
from sqlalchemy.orm import join


class DatabaseManager():
    
    def __init__(self):
        """
            initialize the database, creates tables if not exists
        """
        initDb()
        
    def getAllPrograms(self):
        programs = Program.query.all()
        return [p.serialize() for p in programs]

    def getProgramContacts(self, idProgram):
        program = Program.query.filter_by(id=idProgram).first()
        return [c.serialize() for c in program.contacts]