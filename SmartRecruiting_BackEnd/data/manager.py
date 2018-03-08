# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Manager to interact with the database

Created on Sun Feb 26 16:23:02 2017
@author: Julian
"""

from SmartRecruiting_BackEnd.data.models import *
from SmartRecruiting_BackEnd.data.database import init_db, dbSession as dB
from SmartRecruiting_BackEnd import app
from SmartRecruiting_BackEnd.deeplearning.cnn.train import train
from SmartRecruiting_BackEnd.deeplearning.cnn.eval import eval_all, save_eval
from SmartRecruiting_BackEnd.deeplearning.preprocess.pretraitement import init, reinit, preprocess, descriptor_to_string
import datetime

from sqlalchemy.sql import func
# from sqlalchemy.orm import join


class DatabaseManager():

    def __init__(self):
        """
            initialize the database, creates tables if not exists
        """
        print("Init BD")
        init_db()
        if(app.config['INIT']):
            init(self)
            print ("init")
        elif (app.config['REINIT']):
            reinit(self)
            print("reinit")
        if(app.config['INIT'] or app.config['REINIT']):
            print ("-------------------------------------train ----------------------------------------")
            train(self)
            nb_test, accuracy = eval_all(self)
            save_eval(nb_test, accuracy)



    def get_all_users(self):
        users = User.query.all()
        return [u.serialize() for u in users]

    def get_user_by_id(self, id_user):
        user = User.query.get(id_user)
        if user is None:
            return None
        else:
            return user.serialize()

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()


    def get_one_admin(self):
        return User.query.filter_by(is_admin=1).first()
        """if user is None:
            return None
        else:
            return user.serialize()"""


    def add_user(self, name, surname, role, email, password, is_admin):
        user = User(name, surname, role, email, password, is_admin == 1)
        dB.add(user)
        try:
            dB.commit()
            return True
        except Exception as e:
            dB.rollback()
            return False

    def update_user(self, id_user, name, surname, role, email, password, is_admin):
        user = User.query.get(id_user)

        if user is None:
            return None
        else:
            try:
                if name is not None:
                    user.name = name
                if surname is not None:
                    user.surname = surname
                if role is not None:
                    user.role = role
                if email is not None:
                    user.email = email
                if password is not None:
                    user.password = password
                if is_admin is not None:
                    user.is_admin = is_admin == 1
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

    def add_offer(self, title, content, descriptor, id_user):
        offer = Offer(title, content, descriptor, id_user)
        dB.add(offer)
        try:
            dB.commit()
            return True
        except Exception as e:
            print(e)
            dB.rollback()
            return False

    def add_offer_v2(self, title, content, descriptor, id_user):
        offer = Offer(title, content, descriptor, id_user)
        dB.add(offer)
        try:
            dB.commit()
            return offer.id
        except Exception as e:
            print(e)
            dB.rollback()
            return -1

    def update_offer(self, id_offer, title, content, descriptor, id_user):
        offer = Offer.query.get(id_offer)
        if offer is None:
            return None
        else:
            try:
                if title is not None:
                    offer.title = title
                if content is not None:
                    offer.content = content
                if descriptor is not None:
                    offer.descriptor = descriptor
                if id_user is not None:
                    offer.id_user = id_user
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

    def get_all_predictions_with_field(self):
        predictions = Prediction.query.join(Team, Team.id_prediction == Prediction.id)
        return predictions

    def get_all_offers_with_field_in_base(self):
        offers = Offer.query\
            .with_entities(Offer.descriptor, Team.id_field)\
            .join(Prediction, Offer.id == Prediction.id_offer) \
            .filter_by(inbase=1)\
            .join(Team, Team.id_prediction == Prediction.id)

        return offers

    def get_prediction_by_id(self, id_prediction):
        prediction = Prediction.query.get(id_prediction)
        if prediction is None:
            return None
        else:
            return prediction.serialize()

    def add_prediction(self, mark, inbase, id_offer):
        date = datetime.datetime.now()
        prediction = Prediction(mark, inbase == 1, date, id_offer)
        dB.add(prediction)
        try:
            dB.commit()
            return True
        except Exception as e:
            dB.rollback()
            return False

    def add_prediction_v2(self, mark, inbase, id_offer):
        date = datetime.datetime.now()
        prediction = Prediction(mark, inbase == 1, date, id_offer)
        dB.add(prediction)
        try:
            dB.commit()
            return prediction.id
        except Exception as e:
            dB.rollback()
            return -1

    def update_prediction(self, id_prediction, mark, inbase, id_offer):
        prediction = Prediction.query.get(id_prediction)
        if prediction is None:
            return None
        else:
            try:
                if mark is not None:
                    prediction.mark = mark
                if inbase is not None:
                    prediction.inbase = inbase == 1
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

    def get_team_by_prediction_and_field(self, id_prediction, id_field):
        team = Team.query.filter_by(id_prediction=id_prediction, id_field=id_field).first()
        return team.serialize()


    "TODO: delete team"
    def add_team(self, id_prediction, id_field, nb_members):
        team = Team(id_prediction, id_field, nb_members)
        dB.add(team)
        try:
            dB.commit()
            return True
        except Exception as e:
            dB.rollback()
            return False

    def update_team(self, id_prediction, id_field, nb_members):
        "change la formation associe a une prediction "
        "on suppose qu'il y a une seule formation associe a une prediction dans un premier temps"
        team = Team.query.filter_by(id_prediction=id_prediction).first()
        if team is None:
            return None
        else:
            try:
                if id_field is not None:
                    team.id_field = id_field
                if nb_members is not None:
                    team.nb_members = nb_members
                dB.commit()
                return True
            except Exception as e:
                dB.rollback()
                return False


    def get_all_fields(self):
        fields = Field.query.all()
        return [p.serialize() for p in fields]

    def get_field_by_id(self, id_prog):
        field = Field.query.get(id_prog)
        if field is None:
            return None
        else:
            return field.serialize()

    def get_field_by_name(self, name):
        return Field.query.filter_by(name=name).first()

    def get_all_id_field(self):
        field = Field.query \
            .with_entities(Field.id)
        return field

    def add_field(self, name, description, descriptor, website):
        field = Field(name, description, descriptor, website)
        dB.add(field)
        try:
            dB.commit()
            return True
        except Exception as e:
            dB.rollback()
            return False

    def add_field_v2(self, name, description, descriptor, website):
        field = Field(name, description, descriptor, website)
        dB.add(field)
        try:
            dB.commit()
            return field.id
        except Exception as e:
            dB.rollback()
            return -1

    def update_field(self,id_field, name, description, descriptor, website):
        field = Field.query.get(id_field)
        if field is None:
            return None
        else:
            try:
                if name is not None:
                    field.name = name
                if description is not None:
                    field.description = description
                if descriptor is not None:
                    field.descriptor = descriptor
                if website is not None:
                    field.website = website
                dB.commit()
                return True
            except Exception as e:
                dB.rollback()
                return False

    def delete_field(self, id_field):
        "TODO : suprimer les contacts lié,team"
        field = Field.query.get(id_field)
        if field is None:
            return None
        else:
            dB.delete(field)
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

    def add_contact(self, name, surname, email, phone, role, id_field):
        contact = Contact(name, surname, email, phone, role, id_field)
        dB.add(contact)
        try:
            dB.commit()
            return True
        except Exception as e:
            dB.rollback()
            return False

    def update_contact(self, id_contact, name, surname, email, phone, role, id_field):
        contact = Contact.query.get(id_contact)
        if contact is None:
            return None
        else:
            try:
                if name is not None:
                  contact.name = name
                if surname is not None:
                    contact.surname = surname
                if email is not None:
                    contact.email = email
                if phone is not None:
                    contact.phone = phone
                if role is not None:
                    contact.role = role
                if id_field is not None:
                    contact.id_field = id_field
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

    def get_field_contacts(self, id_field):
        field = Field.query.get(id_field)
        return [c.serialize() for c in field.contacts]


    def add_contact_field(self, id_contact, id_field):
        field = Field.query.get(id_field)
        contact = Contact.query.get(id_contact)
        if field is None or contact is None:
            return False
        else :
            try:
                field.contacts.append(contact)
                dB.commit()
                return True
            except Exception as e:
                dB.rollback()
                return False

    def delete_contact_field(self, id_contact, id_field):
        field = Field.query.get(id_field)
        contact = Contact.query.get(id_contact)
        if field is None or contact is None:
            return False
        else:
            "TODO"

    def offers_by_field(self,id_field):
        "offre associes a une formation"
        "Idoffers = Prediction.query\
            .join(Team, Team.id_prediction == Prediction.id)\
            .filter(Team.id_field == id_field)"
        offers = Offer.query\
            .join(Prediction, Prediction.id_offer == Offer.id)\
            .join(Team, Team.id_prediction == Prediction.id)\
            .filter(Team.id_field == id_field)
        return [o.serialize() for o in offers]

    def fields_by_offer(self, id_offer):
        fields = Field.query\
            .join(Team, Team.id_field == Field.id)\
            .join(Prediction, Prediction.id == Team.id_prediction)\
            .filter(Prediction.id_offer == id_offer)
        return [f.serialize() for f in fields]

    def offers_by_user(self, id_user):
        offers = Offer.query\
            .filter(Offer.id_user == id_user)
        return [o.serialize() for o in offers]

    def average_mark(self, begin_date, end_date):
        average = Prediction\
            .query.with_entities(func.avg(Prediction.mark).label('average'))\
            .filter(Prediction.date <= end_date, Prediction.date >= begin_date)\
            .first()

        return average

    def nb_prediction(self, begin_date, end_date):
        nb_prediction = Prediction.query \
            .with_entities(func.count(Prediction.id).label('number')) \
            .filter(Prediction.date <= end_date, Prediction.date >= begin_date)\
            .first().number
        return nb_prediction
