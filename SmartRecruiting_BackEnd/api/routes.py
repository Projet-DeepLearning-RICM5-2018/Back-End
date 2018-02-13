"""
Routes and views for the flask application.
"""

# from datetime import datetime
# import json
from flask.json import jsonify
from flask import render_template, abort, request
from SmartRecruiting_BackEnd import app

from SmartRecruiting_BackEnd.data import DatabaseManager

dbManager = DatabaseManager()


@app.route('/users')
def get_users():
    return jsonify(dbManager.get_all_users()), 200


@app.route('/users/<int:id>')
def get_user(id_user):
    user = dbManager.get_user_by_id(id_user)
    if user is None:
        abort(404)
    else:
        return jsonify(user), 200


@app.route('/users', methods=['POST'])
def add_user():
    data = request.form
    job = data.get('job', None)
    if dbManager.add_user(data['lastName'], data['firstName'], job, data['email'], data['password'], data['admin']):
        return '', 201
    else:
        abort(400)


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id_user):
    data = request.form
    last_name = data.get('lastName', None)
    first_name = data.get('firstName', None)
    job = data.get('job', None)
    email = data.get('email', None)
    password = data.get('password', None)
    admin = data.get('admin', None)
    response = dbManager.update_user(id_user, last_name, first_name, job, email, password, admin)
    if response is None:
        abort(404)
    else:
        if response:
            return '', 200
        else:
            abort(400)


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id_user):
    if dbManager.delete_user(id_user) is None:
        abort(404)
    else:
        return '', 200


@app.route('/offers')
def get_offers():
    return jsonify(dbManager.get_all_offers()), 200


@app.route('/offers/<int:id>')
def get_offer(id_offer):
    offer = dbManager.get_offer_by_id(id_offer)
    if offer is None:
        abort(404)
    else:
        return jsonify(offer), 200


@app.route('/predictions')
def get_predictions():
    return jsonify(dbManager.get_all_predictions()), 200


@app.route('/predictions/<int:id>')
def get_prediction(id_offer):
    prediction = dbManager.get_prediction_by_id(id_offer)
    if prediction is None:
        abort(404)
    else:
        return jsonify(prediction), 200


@app.route('/teams')
def get_teams():
    return jsonify(dbManager.get_all_teams()), 200


@app.route('/programs')
def get_programs():
    return jsonify(dbManager.get_all_programs()), 200


@app.route('/programs/<int:id>')
def get_program(id_program):
    program = dbManager.get_program_by_id(id_program)
    if program is None:
        abort(404)
    else:
        return jsonify(program), 200


@app.route('/contacts')
def get_contacts():
    return jsonify(dbManager.get_all_contacts()), 200


@app.route('/contacts/<int:id>')
def get_contact(id_contact):
    contact = dbManager.get_contact_by_id(id_contact)
    if contact is None:
        abort(404)
    else:
        return jsonify(contact), 200