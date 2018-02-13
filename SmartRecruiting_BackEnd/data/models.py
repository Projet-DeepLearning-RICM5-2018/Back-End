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
    lastName = Column(String(100), unique=False, nullable=False)
    firstName = Column(String(100), unique=False, nullable=False)
    job = Column(String(100), unique=False, nullable=True)
    email = Column(String(100), unique=False, nullable=False)
    password = Column(String(100), unique=False, nullable=False)
    admin = Column(Boolean, unique=False, nullable=False)
    offers = relationship("Offer")

    def __init__(self, last_name, first_name, job, email, password, admin):
        self.lastName = last_name
        self.firstName = first_name
        self.job = job
        self.email = email
        self.password = password
        self.admin = admin


class Offer(Base):
    __tablename__ = 'offer'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), unique=False, nullable=False)
    description = Column(Text, unique=False, nullable=False)
    descriptor = Column(Text, unique=False, nullable=False)
    idUser = Column(Integer, ForeignKey('user.id'), unique=False, nullable=False)
    prediction = relationship("Prediction", uselist=False)


class Prediction(Base):
    __tablename__ = 'prediction'
    id = Column(Integer, primary_key=True, nullable=False)
    score = Column(Float, unique=False, nullable=False)
    learning = Column(Boolean, unique=False, nullable=False)
    idOffer = Column(Integer, ForeignKey('offer.id'), unique=False, nullable=False)
    teams = relationship("Team")


class Team(Base):
    __tablename__ = 'team'
    idPrediction = Column(Integer, ForeignKey('prediction.id'), primary_key=True, nullable=False)
    idProgram = Column(Integer, ForeignKey('program.id'), primary_key=True, nullable=False)
    nbMembers = Column(Integer, unique=False, nullable=False)


class Program(Base):
    __tablename__ = 'program'
    id = Column(Integer, primary_key=True, nullable=False)
    label = Column(String(100), unique=True, nullable=False)
    description = Column(Text, unique=False, nullable=True)
    descriptor = Column(Text, unique=False, nullable=False)
    site = Column(String(100), unique=False, nullable=True)
    teams = relationship("Team")
    contacts = relationship("Contact")


class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True, nullable=False)
    lastName = Column(String(100), unique=False, nullable=False)
    firstName = Column(String(100), unique=False, nullable=False)
    email = Column(String(100), unique=False, nullable=True)
    phone = Column(String(20), unique=False, nullable=True)
    position = Column(String(100), unique=False, nullable=True)
    idProgram = Column(Integer, ForeignKey('program.id'), unique=False, nullable=False)
