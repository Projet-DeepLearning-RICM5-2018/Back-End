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


@app.route('/users/<int:id_user>')
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
    if dbManager.add_user(data['last_name'], data['first_name'], job, data['email'], data['password'], data['admin']):
        return '', 201
    else:
        abort(400)


@app.route('/users/<int:id_user>', methods=['PUT'])
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


@app.route('/users/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    if dbManager.delete_user(id_user) is None:
        abort(404)
    else:
        return '', 200


@app.route('/offers')
def get_offers():
    return jsonify(dbManager.get_all_offers()), 200


@app.route('/offers/<int:id_offer>')
def get_offer(id_offer):
    offer = dbManager.get_offer_by_id(id_offer)
    if offer is None:
        abort(404)
    else:
        return jsonify(offer), 200


@app.route('/offers', methods=['POST'])
def add_offer():
    data = request.form
    if dbManager.add_offer(data['title'], data['description'], data['descriptor'], data['id_user']):
        return '', 201
    else:
        abort(400)


@app.route('/offers/<int:id_offer>', methods=['PUT'])
def update_offer(id_offer):
    data = request.form
    title = data.get('title', None)
    description = data.get('description', None)
    descriptor = data.get('descriptor', None)
    id_user = data.get('id_user', None)

    response = dbManager.update_offer(id_offer, title, description, descriptor, id_user)
    if response is None:
        abort(404)
    else:
        if response:
            return '', 200
        else:
            abort(400)


@app.route('/offers/<int:id_offer>', methods=['DELETE'])
def delete_offer(id_offer):
    if dbManager.delete_offer(id_offer) is None:
        abort(404)
    else:
        return '', 200


@app.route('/predictions')
def get_predictions():
    return jsonify(dbManager.get_all_predictions()), 200


@app.route('/predictions/<int:id_offer>')
def get_prediction(id_offer):
    prediction = dbManager.get_prediction_by_id(id_offer)
    if prediction is None:
        abort(404)
    else:
        return jsonify(prediction), 200


@app.route('/predictions', methods=['POST'])
def add_prediction():
    data = request.form
    if dbManager.add_prediction(data['score'], data['learning'], data['id_offer']):
        return '', 201
    else:
        abort(400)


@app.route('/predictions/<int:id_prediction>', methods=['PUT'])
def update_prediction(id_prediction):
    data = request.form
    score = data.get('score', None)
    learning = data.get('learning', None)
    id_offer = data.get('id_offer', None)
    response = dbManager.update_prediction(id_prediction, score, learning, id_offer)
    if response is None:
        abort(404)
    else:
        if response:
            return '', 200
        else:
            abort(400)


@app.route('/predictions/<int:id_prediction>', methods=['DELETE'])
def delete_prediction(id_prediction):
    if dbManager.delete_prediction(id_prediction) is None:
        abort(404)
    else:
        return '', 200


@app.route('/teams')
def get_teams():
    return jsonify(dbManager.get_all_teams()), 200


@app.route('/programs')
def get_programs():
    return jsonify(dbManager.get_all_programs()), 200


@app.route('/programs/<int:id_program>')
def get_program(id_program):
    program = dbManager.get_program_by_id(id_program)
    if program is None:
        abort(404)
    else:
        return jsonify(program), 200


@app.route('/programs', methods=['POST'])
def add_program():
    data = request.form
    if dbManager.add_program(data['label'], data['description'], data['descriptor'], data['site']):
        return '', 201
    else:
        abort(400)


@app.route('/programs/<int:id_program>', methods=['PUT'])
def update_program(id_program):
    data = request.form
    label = data.get('label', None)
    description = data.get('description', None)
    descriptor = data.get('descriptor', None)
    response = dbManager.update_program(id_program, label, description, descriptor)
    if response is None:
        abort(404)
    else:
        if response:
            return '', 200
        else:
            abort(400)


@app.route('/programs/<int:id_program>', methods=['DELETE'])
def delete_program(id_program):
    if dbManager.delete_prediction(id_program) is None:
        abort(404)
    else:
        return '', 200


@app.route('/contacts')
def get_contacts():
    return jsonify(dbManager.get_all_contacts()), 200


@app.route('/contacts/<int:id_contact>')
def get_contact(id_contact):
    contact = dbManager.get_contact_by_id(id_contact)
    if contact is None:
        abort(404)
    else:
        return jsonify(contact), 200


@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.form
    email = data.get('email', None)
    phone = data.get('phone', None)
    position = data.get('position', None)
    if dbManager.add_contact(data['last_name'], data['first_name'], email, phone, position, data['id_program']):
        return '', 201
    else:
        abort(400)


@app.route('/contacts/<int:id_contact>', methods=['PUT'])
def update_contact(id_contact):
    data = request.form
    last_name = data.get('last_name', None)
    first_name = data.get('first_name',None)
    email = data.get('email', None)
    phone = data.get('phone', None)
    position = data.get('position', None)
    id_program = data.get('id_program', None)
    response = dbManager.update_contact(id_contact, last_name, first_name, email, phone, position, id_program)
    if response is None:
        abort(404)
    else:
        if response:
            return '', 200
        else:
            abort(400)


@app.route('/contacts/<int:id_contact>', methods=['DELETE'])
def delete_contact(id_contact):
    if dbManager.delete_contact(id_contact) is None:
        abort(404)
    else:
        return '', 200
