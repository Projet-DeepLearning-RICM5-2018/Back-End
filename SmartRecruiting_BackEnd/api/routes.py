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
    """
    Function to get all the users
    :return: {"user":{ "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str, "is_admin" : bool }}
    """
    return jsonify(dbManager.get_all_users()), 200


@app.route('/users/<int:id_user>')
def get_user(id_user):
    """
    Function to get the user in the database
    :param id_user: int
    :return: user :{ "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str, "is_admin" : bool }
    """
    user = dbManager.get_user_by_id(id_user)
    if user is None:
        abort(404)
    else:
        return jsonify(user), 200


@app.route('/users', methods=['POST'])
def add_user():
    """
    METHOD : POST
    HEADER PARAM  : None
    BODY PARAMS : { "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str, "is_admin" : bool }
    """
    data = request.form
    role = data.get('role', None)
    if dbManager.add_user(data['name'], data['surname'], role, data['email'], data['password'], data['is_admin']):
        return '', 201
    else:
        abort(400)


@app.route('/users/<int:id_user>', methods=['PUT'])
def update_user(id_user):
    """
    METHOD : PUT
    HEADER PARAM  : id_user: int
    BODY PARAMS : { "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str,"is_admin" : bool }
    """
    data = request.form
    name = data.get('name', None)
    surname = data.get('surname', None)
    role = data.get('role', None)
    email = data.get('email', None)
    password = data.get('password', None)
    is_admin = data.get('is_admin', None)
    response = dbManager.update_user(id_user, name, surname, role, email, password, is_admin)
    if response is None:
        abort(404)
    else:
        if response:
            return '', 200
        else:
            abort(400)


@app.route('/users/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    """
    METHOD : DELETE
    HEADER PARAM  : id_user: int
    """
    if dbManager.delete_user(id_user) is None:
        abort(404)
    else:
        return '', 200


@app.route('/offers')
def get_offers():
    """
    Function to get all the offers in the database
    :return: {"offer":{ "title" : str, "content" : str, "descriptor" : str, "id_user" : int }}
    """
    return jsonify(dbManager.get_all_offers()), 200


@app.route('/offers/<int:id_offer>')
def get_offer(id_offer):
    """
    Get the offer of id id_offer
    :param id_offer: int
    :return: offer:{ "title" : str, "content" : str, "descriptor" : str, "id_user" : int }
    """
    offer = dbManager.get_offer_by_id(id_offer)
    if offer is None:
        abort(404)
    else:
        return jsonify(offer), 200


@app.route('/offers', methods=['POST'])
def add_offer():
    """
    METHOD : POST
    HEADER PARAM  : None
    BODY PARAMS : { "title" : str, "content" : str, "descriptor" : str, "id_user" : int }
    """
    data = request.form
    if dbManager.add_offer(data['title'], data['content'], data['descriptor'], data['id_user']):
        return '', 201
    else:
        abort(400)


@app.route('/offers/<int:id_offer>', methods=['PUT'])
def update_offer(id_offer):
    """
    METHOD : PUT
    HEADER PARAM  : id_offer :int
    BODY PARAMS : { "title" : str, "content" : str, "descriptor" : str, "id_user" : int }
    """
    data = request.form
    title = data.get('title', None)
    content = data.get('content', None)
    descriptor = data.get('descriptor', None)
    id_user = data.get('id_user', None)

    response = dbManager.update_offer(id_offer, title, content, descriptor, id_user)
    if response is None:
        abort(404)
    else:
        if response:
            return '', 200
        else:
            abort(400)


@app.route('/offers/<int:id_offer>', methods=['DELETE'])
def delete_offer(id_offer):
    """
    METHOD : DELETE
    HEADER PARAM  : id_offer :int
    """
    if dbManager.delete_offer(id_offer) is None:
        abort(404)
    else:
        return '', 200


@app.route('/predictions')
def get_predictions():
    """
    Function to get all the prediction in the database
    :return: {"predictions":{"mark": int, "inbase": bool, "id_offer": int}}
    """
    return jsonify(dbManager.get_all_predictions()), 200


@app.route('/predictions/<int:id_offer>')
def get_prediction(id_offer):
    """
    Function to get a prediction in the database
    :param id_offer: int
    :return: {"predictions":{"mark": int, "inbase": bool, "id_offer": int}}
    """
    prediction = dbManager.get_prediction_by_id(id_offer)
    if prediction is None:
        abort(404)
    else:
        return jsonify(prediction), 200


@app.route('/predictions', methods=['POST'])
def add_prediction():
    """
    Function to add a prediction in the database
    :METHOD : POST
    :HEADER PARAM  : None
    :BODY PARAMS :{"mark": int, "inbase": bool, "id_offer": int}
    """
    data = request.form
    if dbManager.add_prediction(data['mark'], data['inbase'], data['id_offer']):
        return '', 201
    else:
        abort(400)


@app.route('/predictions/<int:id_prediction>', methods=['PUT'])
def update_prediction(id_prediction):
    """
    Function to update a prediction in the database
    :METHOD : PUT
    :HEADER PARAM  : id_prediction : int
    :BODY PARAMS :{"mark": int, "inbase": bool, "id_offer": int}
    """
    "TODO la mise a jour de inbase ne fonctionne pas pour une raison obscure"
    data = request.form
    mark = data.get('mark', None)
    inbase = data.get('inbase', None)
    id_offer = data.get('id_offer', None)
    response = dbManager.update_prediction(id_prediction, mark, inbase, id_offer)
    if response is None:
        abort(404)
    else:
        if response:
            return '', 200
        else:
            abort(400)


@app.route('/predictions/<int:id_prediction>', methods=['DELETE'])
def delete_prediction(id_prediction):
    """
    Function to delete a prediction in the database
    :METHOD : DELETE
    :HEADER PARAM  : id_prediction : int
    :BODY PARAMS :{"mark": int, "inbase": bool, "id_offer": int}
    """
    if dbManager.delete_prediction(id_prediction) is None:
        abort(404)
    else:
        return '', 200


@app.route('/teams')
def get_teams():
    """
    Function to get all the teams in the database
    :return: {"predictions":{"mark": int, "inbase": bool, "id_offer": int}}
    """
    return jsonify(dbManager.get_all_teams()), 200


@app.route('/fields')
def get_fields():
    """
    Function to get all the field in the database
    :return: {"fields":{"name": str, "description": str, "descriptor": str,"website": str}}
    """
    return jsonify(dbManager.get_all_fields()), 200


@app.route('/fields/<int:id_field>')
def get_field(id_field):
    """
    Function to get a field in the database
    :param id_field: int
    :return: {"field":{"mark": int, "inbase": bool, "id_offer": int}}
    """
    field = dbManager.get_field_by_id(id_field)
    if field is None:
        abort(404)
    else:
        return jsonify(field), 200


@app.route('/fields', methods=['POST'])
def add_field():
    """
    Function to add a field in the database
    :METHOD : POST
    :HEADER PARAM  : None
    :BODY PARAMS :{"name": str, "description": str, "descriptor": str,"website": str}
    """
    data = request.form
    if dbManager.add_field(data['name'], data['description'], data['descriptor'], data['website']):
        return '', 201
    else:
        abort(400)


@app.route('/fields/<int:id_field>', methods=['PUT'])
def update_field(id_field):
    """
    Function to update a field in the database
    :METHOD : PUT
    :HEADER PARAM  : id_field : int
    :BODY PARAMS :{"name": str, "description": str, "descriptor": str,"website": str}
    """
    data = request.form
    name = data.get('name', None)
    description = data.get('description', None)
    descriptor = data.get('descriptor', None)
    website = data.get('website',None)
    response = dbManager.update_field(id_field, name, description, descriptor, website)
    if response is None:
        abort(404)
    else:
        if response:
            return '', 200
        else:
            abort(400)


@app.route('/fields/<int:id_field>', methods=['DELETE'])
def delete_field(id_field):
    """
    Function to delete a field in the database
    :METHOD : DELETE
    :HEADER PARAM  : id_field : int
    """
    if dbManager.delete_field(id_field) is None:
        abort(404)
    else:
        return '', 200


@app.route('/contacts')
def get_contacts():
    """
    Function to get all the contact in the database
    :return: {"contact":{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int}}
    """
    return jsonify(dbManager.get_all_contacts()), 200


@app.route('/contacts/<int:id_contact>')
def get_contact(id_contact):
    """
    Function to get a contact in the database
    :param id_contact: int
    :return: {"contact":{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int}}
    """
    contact = dbManager.get_contact_by_id(id_contact)
    if contact is None:
        abort(404)
    else:
        return jsonify(contact), 200


@app.route('/contacts', methods=['POST'])
def add_contact():
    """
    Function to add a contact in the database
    :METHOD : POST
    :HEADER PARAM  : None
    :BODY PARAMS :{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int}
    """

    data = request.form
    email = data.get('email', None)
    phone = data.get('phone', None)
    role = data.get('role', None)
    if dbManager.add_contact(data['name'], data['surname'], email, phone, role, data['id_field']):
        return '', 201
    else:
        abort(400)


@app.route('/contacts/<int:id_contact>', methods=['PUT'])
def update_contact(id_contact):
    """
    Function to update a contact in the database
    :METHOD : PUT
    :HEADER PARAM  : id_contact : int
    :BODY PARAMS :{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int}
    """
    data = request.form
    name = data.get('name', None)
    surname = data.get('surname',None)
    email = data.get('email', None)
    phone = data.get('phone', None)
    role = data.get('role', None)
    id_field = data.get('id_field', None)
    response = dbManager.update_contact(id_contact, name, surname, email, phone, role, id_field)
    if response is None:
        abort(404)
    else:
        if response:
            return '', 200
        else:
            abort(400)


@app.route('/contacts/<int:id_contact>', methods=['DELETE'])
def delete_contact(id_contact):
    """
    Function to delete a contact in the database
    :METHOD : DELETE
    :HEADER PARAM  : id_contact : int
    :BODY PARAMS :{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int}
    """

    if dbManager.delete_contact(id_contact) is None:
        abort(404)
    else:
        return '', 200
