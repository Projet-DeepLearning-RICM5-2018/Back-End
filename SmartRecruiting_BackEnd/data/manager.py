"""
Manager to interact with the database

Created on Sun Feb 26 16:23:02 2017
@author: Julian
"""

from SmartRecruiting_BackEnd.data.models import *
from SmartRecruiting_BackEnd.data.database import init_db, dbSession as dB
# from sqlalchemy.orm import join


class DatabaseManager():

    def __init__(self):
        """
            initialize the database, creates tables if not exists
        """
        init_db()

    def get_all_users(self):
        users = User.query.all()
        return [u.serialize() for u in users]

    def get_user_by_id(self, id_user):
        user = User.query.get(id_user)
        if user is None:
            return None
        else:
            return user.serialize()

    def add_user(self, last_name, first_name, job, email, password, admin):
        user = User(last_name, first_name, job, email, password, admin ==1)
        dB.add(user)
        try:
            dB.commit()
            return True
        except Exception as e:
            dB.rollback()
            return False

    def update_user(self, id_user, last_name, first_name, job, email, password, admin):
        user = User.query.get(id_user)
        if user is None:
            return None
        else:
            try:
                if last_name is not None:
                    user.lastName = last_name
                if first_name is not None:
                    user.firstName = first_name
                if job is not None:
                    user.job = job
                if email is not None:
                    user.email = email
                if password is not None:
                    user.password = password
                if admin is not None:
                    user.admin = admin == 1
                dB.commit()
                return True
            except Exception as e:
                dB.rollback()
                return False

    def delete_user(self, id_user):
        user = User.query.get(id_user)
        if user is None:
            return None
        else:
            dB.delete(user)
            dB.commit()
            return True
        
    def get_all_offers(self):
        offers = Offer.query.all()
        return [o.serialize() for o in offers]

    def get_offer_by_id(self, id_offer):
        offer = Offer.query.get(id_offer)
        if offer is None:
            return None
        else:
            return offer.serialize()
        
    def get_all_predictions(self):
        predictions = Prediction.query.all()
        return [p.serialize() for p in predictions]

    def get_prediction_by_id(self, id):
        prediction = Prediction.query.get(id)
        if prediction is None:
            return None
        else:
            return prediction.serialize()
        
    def get_all_teams(self):
        teams = Team.query.all()
        return [t.serialize() for t in teams]

    def get_team_by_prediction_and_program(self, id_prediction, id_program):
        team = Team.query.filter_by(idPrediction=id_prediction, idProgram=id_program).first()
        return team.serialize()
    
    def get_all_programs(self):
        programs = Program.query.all()
        return [p.serialize() for p in programs]

    def get_program_by_id(self, id_prog):
        program = Program.query.get(id_prog)
        if program is None:
            return None
        else:
            return program.serialize()

    def get_all_contacts(self):
        contacts = Contact.query.all()
        return [c.serialize() for c in contacts]

    def get_contact_by_id(self, id_contact):
        contact = Contact.query.get(id_contact)
        if contact is None:
            return None
        else:
            return contact.serialize()

    def get_program_contacts(self, id_program):
        program = Program.query.get(id_program)
        return [c.serialize() for c in program.contacts]