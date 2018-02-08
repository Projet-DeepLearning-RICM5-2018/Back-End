"""
Routes and views for the flask application.
"""

from datetime import datetime
import json
from flask.json import jsonify
from flask import render_template
from SmartRecruiting_BackEnd import app

from SmartRecruiting_BackEnd.data import DatabaseManager

dbManager = DatabaseManager()

@app.route('/users')
def getUsers():
    return jsonify(dbManager.getAllUsers()), 200

@app.route('/offers')
def getOffers():
    return jsonify(dbManager.getAllOffers()), 200

@app.route('/predictions')
def getPredictions():
    return jsonify(dbManager.getAllPredictions()), 200

@app.route('/teams')
def getTeams():
    return jsonify(dbManager.getAllTeams()), 200

@app.route('/programs')
def getPrograms():
    return jsonify(dbManager.getAllPrograms()), 200

@app.route('/contacts')
def getContacts():
    return jsonify(dbManager.getAllContacts()), 200