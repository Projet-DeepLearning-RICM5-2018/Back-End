"""
Manager to interact with the database

Created on Sun Feb 26 16:23:02 2017
@author: Julian
"""

from SmartRecruiting_BackEnd.data.models import *
from SmartRecruiting_BackEnd.data.database import initDb, dbSession as db
from sqlalchemy.orm import join


class DatabaseManager():
    
    def __init__(self):
        """
            initialize the database, creates tables if not exists
        """
        initDb()
        
    def getAllUsers(self):
        users = User.query.all()
        return [u.serialize() for u in users]

    def getUserById(self, id):
        user = User.query.get(id)
        if user is None:
            return None
        else:
            return user.serialize()

    def addUser(self, lastName, firstName, job, email, password, admin):
        user = User(lastName, firstName, job, email, password, admin==1)
        db.add(user)
        try:
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            return False

    def updateUser(self, id, lastName, firstName, job, email, password, admin):
        user = User.query.get(id)
        if user is None:
            return None
        else:
            try:
                if lastName is not None:
                    user.lastName = lastName
                if firstName is not None:
                    user.firstName = firstName
                if job is not None:
                    user.job = job
                if email is not None:
                    user.email = email
                if password is not None:
                    user.password = password
                if admin is not None:
                    user.admin = admin==1
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                return False
        
    def getAllOffers(self):
        offers = Offer.query.all()
        return [o.serialize() for o in offers]

    def getOfferById(self, id):
        offer = Offer.query.get(id)
        if offer is None:
            return None
        else:
            return offer.serialize()
        
    def getAllPredictions(self):
        predictions = Prediction.query.all()
        return [p.serialize() for p in predictions]

    def getPredictionById(self, id):
        prediction = Prediction.query.get(id)
        if prediction is None:
            return None
        else:
            return prediction.serialize()
        
    def getAllTeams(self):
        teams = Team.query.all()
        return [t.serialize() for t in teams]

    def getTeamByPredictionAndProgram(self, idPrediction, idProgram):
        team = Team.query.filter_by(idPrediction=idPrediction, idProgram=idProgram).first()
        return team.serialize()
    
    def getAllPrograms(self):
        programs = Program.query.all()
        return [p.serialize() for p in programs]

    def getProgramById(self, id):
        program = Program.query.get(id)
        if program is None:
            return None
        else:
            return program.serialize()

    def getAllContacts(self):
        contacts = Contact.query.all()
        return [c.serialize() for c in contacts]

    def getContactById(self, id):
        contact = Contact.query.get(id)
        if contact is None:
            return None
        else:
            return contact.serialize()


    def getProgramContacts(self, idProgram):
        program = Program.query.get(idProgram)
        return [c.serialize() for c in program.contacts]