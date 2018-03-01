# encoding: utf-8
# -*- coding: utf-8 -*-
"""
ORM representation of tables


Created on Fri Feb 24 22:44:09 2017

@author: Julian
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Text, Float
from sqlalchemy.orm import relationship
from SmartRecruiting_BackEnd.data.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=False, nullable=False)
    surname = Column(String(100), unique=False, nullable=False)
    role = Column(String(100), unique=False, nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), unique=False, nullable=False)
    is_admin = Column(Boolean, unique=False, nullable=False)
    offers = relationship("Offer")

    def __init__(self, name, surname, role, email, password, is_admin):
        self.name = name
        self.surname = surname
        self.role = role
        self.email = email
        self.password = password
        self.is_admin = is_admin


class Offer(Base):
    __tablename__ = 'offer'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), unique=False, nullable=False)
    content = Column(Text, unique=False, nullable=False)
    descriptor = Column(Text, unique=False, nullable=False)
    id_user = Column(Integer, ForeignKey('user.id'), unique=False, nullable=False)
    prediction = relationship("Prediction", uselist=False)

    def __init__(self, title, content, descriptor, id_user):
        self.title = title
        self.content = content
        self.descriptor = descriptor
        self.id_user = id_user


class Prediction(Base):
    __tablename__ = 'prediction'
    id = Column(Integer, primary_key=True, nullable=False)
    mark = Column(Float, unique=False, nullable=False)
    inbase = Column(Boolean, unique=False, nullable=False)
    date = Column(Date, unique=False, nullable=False)
    id_offer = Column(Integer, ForeignKey('offer.id'), unique=False, nullable=False)
    lunch_date = Column(Date, unique=False, nullable=False)
    teams = relationship("Team")

    def __init__(self, mark, inbase, date, id_offer):
        self.mark = mark
        self.inbase = inbase
        self.date = date
        self.id_offer = id_offer

class Team(Base):
    __tablename__ = 'team'
    id_prediction = Column(Integer, ForeignKey('prediction.id'), primary_key=True, nullable=False)
    id_field = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    nb_members = Column(Integer, unique=False, nullable=False)

    def __init__(self, id_prediction, id_field, nb_members):
        self.id_prediction = id_prediction
        self.id_field = id_field
        self.nb_members = nb_members

class Field (Base):
    __tablename__ = 'field'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, unique=False, nullable=True)
    descriptor = Column(Text, unique=False, nullable=False)
    website = Column(String(100), unique=False, nullable=True)
    teams = relationship("Team")
    contacts = relationship("Contact")

    def __init__(self, name, description, descriptor, website):
        self.name = name
        self.description = description
        self.descriptor = descriptor
        self.website = website

class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), unique=False, nullable=False)
    surname = Column(String(100), unique=False, nullable=False)
    email = Column(String(100), unique=False, nullable=True)
    phone = Column(String(20), unique=False, nullable=True)
    role = Column(String(100), unique=False, nullable=True)
    id_field = Column(Integer, ForeignKey('field.id'), unique=False, nullable=False)

    def __init__(self, name, surname, email, phone, role, id_field):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone
        self.role = role
        self.id_field = id_field
