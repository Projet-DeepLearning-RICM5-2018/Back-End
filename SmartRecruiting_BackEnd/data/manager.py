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

    def delete_users(self):
        users = User.query.all()
        for user in users:
            dB.delete(user)
            dB.commit()
        
    def get_all_offers(self):
        offers = Offer.query.all()
        return [o.serialize() for o in offers]

    def get_offer_by_id(self, id_offer):
        offer = Offer.query.get(id_offer)
        if offer is None:
            return None
        else:
            return offer.serialize()

    def add_offer(self, title, description, descriptor, id_user):
        offer = Offer(title, description, descriptor, id_user)
        dB.add(offer)
        try:
            dB.commit()
            return True
        except Exception as e:
            dB.rollback()
            return False

    def update_offer(self, id_offer, title, description, descriptor, id_user):
        offer = Offer.query.get(id_offer)
        if offer is None:
            return None
        else:
            try:
                if title is not None:
                    offer.title = title
                if description is not None:
                    offer.description = description
                if descriptor is not None:
                    offer.descriptor = descriptor
                if id_user is not None:
                    offer.idUser = id_user
                dB.commit()
                return True
            except Exception as e:
                dB.rollback()
                return False

    def delete_offer(self, id_offer):
        offer = Offer.query.get(id_offer)
        if offer is None:
            return None
        else:
            dB.delete(offer)
            dB.commit()
            return True
        
    def get_all_predictions(self):
        predictions = Prediction.query.all()
        return [p.serialize() for p in predictions]

    def get_prediction_by_id(self, id):
        prediction = Prediction.query.get(id)
        if prediction is None:
            return None
        else:
            return prediction.serialize()

    def add_prediction(self, score, learning, id_offer):
        prediction = Prediction(score, learning == 1, id_offer)
        dB.add(prediction)
        try:
            dB.commit()
            return True
        except Exception as e:
            dB.rollback()
            return False

    def update_prediction(self,id_prediction, score, learning, id_offer):
        prediction = Prediction.query.get(id_prediction)
        if prediction is None:
            return None
        else:
            try:
                if score is not None:
                    prediction.score = score
                if learning is not None:
                    prediction.learning = learning
                if id_offer is not None:
                    prediction.idOffer = id_offer
                dB.commit()
                return True
            except Exception as e:
                dB.rollback()
                return False

    def delete_prediction(self, id_prediction):
        prediction = Prediction.query.get(id_prediction)
        if prediction is None:
            return None
        else:
            dB.delete(prediction)
            dB.commit()
            return True
        
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

    def add_program(self, label, description, descriptor, site):
        program = Program(label, description, descriptor, site)
        dB.add(program)
        try:
            dB.commit()
            return True
        except Exception as e:
            dB.rollback()
            return False

    def update_program(self,id_program, label, description, descriptor, site):
        program = Program.query.get(id_program)
        if program is None:
            return None
        else:
            try:
                if label is not None:
                    program.label = label
                if description is not None:
                    program.description = description
                if descriptor is not None:
                    program.descriptor = descriptor
                if site is not None:
                    program.site = site
                dB.commit()
                return True
            except Exception as e:
                dB.rollback()
                return False

    def delete_program(self, id_program):
        program = Program.query.get(id_program)
        if program is None:
            return None
        else:
            dB.delete(program)
            dB.commit()
            return True

    def get_all_contacts(self):
        contacts = Contact.query.all()
        return [c.serialize() for c in contacts]

    def get_contact_by_id(self, id_contact):
        contact = Contact.query.get(id_contact)
        if contact is None:
            return None
        else:
            return contact.serialize()

    def add_contact(self, last_name, first_name, email, phone, position, id_program):
        contact = Contact(last_name, first_name, email, phone, position, id_program)
        dB.add(contact)
        try:
            dB.commit()
            return True
        except Exception as e:
            dB.rollback()
            return False

    def update_contact(self, id_contact, last_name, first_name, email, phone, position, id_program):
        contact = Contact.query.get(id_contact)
        if contact is None:
            return None
        else:
            try:
                if last_name is not None:
                  contact.lastName = last_name
                if first_name is not None:
                    contact.firstName = first_name
                if email is not None:
                    contact.email = email
                if phone is not None:
                    contact.phone = phone
                if position is not None:
                    contact.position = position
                if id_program is not None:
                    contact.idProgram = id_program
                dB.commit()
                return True
            except Exception as e:
                dB.rollback()
                return False

    def delete_contact(self, id_contact):
        contact = Contact.query.get(id_contact)
        if contact is None:
            return None
        else:
            dB.delete(contact)
            dB.commit()
            return True

    def get_program_contacts(self, id_program):
        program = Program.query.get(id_program)
        return [c.serialize() for c in program.contacts]