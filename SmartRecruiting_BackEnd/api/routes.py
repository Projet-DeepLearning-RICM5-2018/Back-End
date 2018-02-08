"""
Routes and views for the flask application.
"""

from datetime import datetime
import json
from flask.json import jsonify
from flask import render_template, abort
from SmartRecruiting_BackEnd import app

from SmartRecruiting_BackEnd.data import DatabaseManager

dbManager = DatabaseManager()

@app.route('/users')
def getUsers():
    return jsonify(dbManager.getAllUsers()), 200

@app.route('/users/<int:id>')
def getUser(id):
    user = dbManager.getUserById(id)
    if user is None:
        abort(404)
    else:
        return jsonify(user)

@app.route('/offers')
def getOffers():
    return jsonify(dbManager.getAllOffers()), 200

@app.route('/offers/<int:id>')
def getOffer(id):
    offer = dbManager.getOfferById(id)
    if offer is None:
        abort(404)
    else:
        return jsonify(offer)

@app.route('/predictions')
def getPredictions():
    return jsonify(dbManager.getAllPredictions()), 200

@app.route('/predictions/<int:id>')
def getPrediction(id):
    prediction = dbManager.getPredictionById(id)
    if prediction is None:
        abort(404)
    else:
        return jsonify(prediction)

@app.route('/teams')
def getTeams():
    return jsonify(dbManager.getAllTeams()), 200

@app.route('/programs')
def getPrograms():
    return jsonify(dbManager.getAllPrograms()), 200

@app.route('/programs/<int:id>')
def getProgram(id):
    program = dbManager.getProgramById(id)
    if program is None:
        abort(404)
    else:
        return jsonify(program)

@app.route('/contacts')
def getContacts():
    return jsonify(dbManager.getAllContacts()), 200

@app.route('/contacts/<int:id>')
def getContact(id):
    contact = dbManager.getContactById(id)
    if contact is None:
        abort(404)
    else:
        return jsonify(contact)