"""
Routes and views for the flask application.
"""

from datetime import datetime
import json
from flask.json import jsonify
from flask import render_template
from SmartRecruiting_BackEnd import app

from SmartRecruiting_BackEnd.data import Program, DatabaseManager

dbManager = DatabaseManager()

@app.route('/programs')
def getPrograms():
    return jsonify(dbManager.getAllPrograms()), 200