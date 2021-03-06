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
from SmartRecruiting_BackEnd.deeplearning.cnn.train import train, def_flags
from SmartRecruiting_BackEnd.deeplearning.cnn.eval import eval_all, save_eval, def_eval_flag
from SmartRecruiting_BackEnd.deeplearning.preprocess.pretraitement import init, reinit, preprocess, descriptor_to_string
import datetime

from sqlalchemy.sql import func


class DatabaseManager():

    def __init__(self):
        """
            initialize the database, creates tables if not exists
        """
        print("Init BD")
        init_db()

        filter_sizes ="3,4,5"
        num_filters = 128
        l2 = 0.0
        batch_size = 64
        num_epochs = 200

        if(app.config['INIT']):
            if self.get_one_admin() is None:
                self.add_user("monsieur", "administrateur", "admin", "admin@", "root", 1)
            init(self)
            print ("init")
        elif (app.config['REINIT']):
            reinit(self)
            print("reinit")
        def_flags()
        if(app.config['INIT'] or app.config['REINIT']):
            print ("-------------------------------------train ----------------------------------------")
            train(self, filter_sizes, num_filters, l2, batch_size, num_epochs)
            def_eval_flag()
            nb_test, accuracy = eval_all(self)
            save_eval(nb_test, accuracy)
        else :
            def_eval_flag()

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
            try:
                for o in user.offers:
                    if o.prediction.inbase:
                        o.id_user = 1
                    else:
                        self.delete_offer(o.id)
                dB.delete(user)
                dB.commit()
                return True
            except Exception as e:
                dB.rollback()
                return False

    def delete_users(self):
        users = User.query.all()
        for user in users:
            self.delete_user(user.id)
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

    def add_offer(self, title, content, descriptor, id_user):
        offer = Offer(title, content, descriptor, id_user)
        dB.add(offer)
        try:
            dB.commit()
            return True
        except Exception as e:
            dB.rollback()
            return False

    def add_offer_v2(self, title, content, descriptor, id_user):
        offer = Offer(title, content, descriptor, id_user)
        dB.add(offer)
        try:
            dB.commit()
            return offer.id
        except Exception as e:
            dB.rollback()
            return -1

    def add_offer_link_field(self, title, content, id_user, id_field, inbase):
        descriptor = preprocess(content)
        descriptor = descriptor_to_string(descriptor)
        id_offer = self.add_offer_v2(title, content, descriptor, id_user)
        if id_offer != -1:
            id_prediction = self.add_prediction_v2(0, inbase, id_offer)
            if id_prediction != -1:
                self.add_team(id_prediction, id_field, 1)
                return id_offer
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
            prediction = Prediction.query.filter_by(id_offer=id_offer).first()
            if prediction is not None:
                team = Team.query.filter_by(id_prediction=prediction.id).first()
                if team is not None:
                    dB.delete(team)
                dB.delete(prediction)
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

    def update_prediction_by_id_offer(self, id_offer, id_field, in_base):
        offer = Offer.query.get(id_offer)
        if offer is None:
            return None
        else:
            try:
                prediction = offer.prediction
                if id_field != None :
                    teams = prediction.teams
                    for team in teams:
                        team.id_field = id_field
                if in_base != None :
                    prediction.inbase == in_base
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

    def update_prediction_by_id_offer(self, id_offer, id_field, in_base):
        offer = Offer.query.get(id_offer)
        if offer is None:
            return None
        else:
            try:
                prediction = offer.prediction
                if id_field != None :
                    teams = prediction.teams
                    for team in teams:
                        team.id_field = id_field
                if in_base != None :
                    prediction.inbase = (in_base == 1)
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
            try:
                teams = prediction.teams
                for t in teams:
                    self.delete_team(t.id)
                dB.delete(prediction)
                dB.commit()
                return True
            except Exception as e:
                dB.rollback()
                return False

    def get_all_teams(self):
        teams = Team.query.all()
        return [t.serialize() for t in teams]

    def get_team_by_prediction_and_field(self, id_prediction, id_field):
        team = Team.query.filter_by(id_prediction=id_prediction, id_field=id_field).first()
        return team.serialize()


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

    def delete_team(self, id_prediction, id_field):
        team = Team.query.filter_by(id_prediction=id_prediction, id_field=id_field).first()
        if team is None:
            return False
        else:
            dB.delete(team)
            dB.commit()
            return True


    def get_all_fields(self):
        fields = Field.query.all()
        return [p.serialize() for p in fields]

    def get_all_fields_name(self):
        fields = Field.query.with_entities(Field.id, Field.name).all()
        result = []
        for f in fields :
            result.append({'id': f[0], 'name': f[1].decode("utf-8")})
        return result

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
            return field.serialize()
        except Exception as e:
            dB.rollback()
            return None

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
        field = Field.query.get(id_field)
        if field is None:
            return None
        else:
            for contact in field.contacts:
                self.delete_contact(contact.id)
            for team in field.teams:
                prediction = Prediction.query.get(team.id_prediction)
                dB.delete(team)
                if prediction is not None:
                    dB.delete(prediction)
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
            return contact.serialize()
        except Exception as e:
            dB.rollback()
            return None

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
        fields = Field.query.with_entities(Field.id, Field.name, Prediction.inbase)\
            .join(Team, Team.id_field == Field.id)\
            .join(Prediction, Prediction.id == Team.id_prediction)\
            .filter(Prediction.id_offer == id_offer)
        return [self.serialize_field_in_base(f) for f in fields]

    def serialize_field_in_base(self,item):
        return {
            'id': item[0],
            'name': item[1].decode("utf-8"),
            'inbase': item[2]
        }

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

    def recherche(self, nboffre_par_page, num_page_voulue, begin_date, end_date, id_field):
        if nboffre_par_page not in range(0, 50):
            nboffre_par_page = 50
        offers = self.recherche_offers_by_date_and_id(begin_date, end_date, id_field)

        nb_offer = len(offers)
        if nb_offer % nboffre_par_page != 0 :
            nb_pages = int(nb_offer / nboffre_par_page)+1
        else :
            nb_pages = int(nb_offer / nboffre_par_page)
        ind_inf = (num_page_voulue - 1) * nboffre_par_page
        ind_sup = (num_page_voulue * nboffre_par_page)
        list_offre = offers[ind_inf: ind_sup]
        derniere_page = nb_offer < ind_sup #peut etre <=

        lis = [self.serialize_offer_and_field(item) for item in list_offre]
        return num_page_voulue, nb_pages, derniere_page, lis

    def serialize_offer_and_field(self,item):
        return {
            'offer': {
                'id'        : item[0],
                'id_user'   : item[1],
                'content'   : item[2].decode("utf-8"),
                'title'     : item[3].decode("utf-8"),
            },
            'field':{
                'id'  : item[4],
                'name': item[5].decode("utf-8")
            }
        }

    def recherche_offers_by_date_and_id(self, begin_date, end_date, id_field ):
        offers =Offer.query \
            .with_entities(Offer.id, Offer.id_user, Offer.content, Offer.title, Field.id, Field.name) \
            .join(Prediction, Prediction.id_offer == Offer.id) \
            .join(Team, Team.id_prediction == Prediction.id) \
            .join(Field, Field.id == Team.id_field) \
            .filter(Prediction.inbase == 1)
        if id_field is not None:
            offers = offers.filter(Team.id_field == id_field)
        if begin_date is not None and end_date is not None:
            offers = offers.filter(Prediction.date <= end_date, Prediction.date >= begin_date)

        return offers.order_by(Offer.id.desc()).all()
