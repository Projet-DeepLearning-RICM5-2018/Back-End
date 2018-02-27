"""
Routes and views for the flask application.
sudo apt-get install python3 python3-pip
sudo pip3 install flask sqlalchemy flask-sqlalchemy pymysql
python3 runserver.py
pip install cffi, bcrypt, PyJWT
"""



# from datetime import datetime
# import json
from flask import Flask, jsonify, request, json, session, g
from flask.json import jsonify
from flask import render_template, abort, request
from SmartRecruiting_BackEnd import app

from flask_cors import CORS, cross_origin
from functools import wraps
from bcrypt import gensalt, hashpw
from jwt import encode, decode, DecodeError, ExpiredSignature
from datetime import datetime, timedelta

from SmartRecruiting_BackEnd.data import DatabaseManager

dbManager = DatabaseManager()

def createToken(user):
        """
            Create a token for a user with an expiration of ...
        """
        payload = {
            'sub': user.email.decode('utf-8'),
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=14)
        }
        token = encode(payload, app.config['TOKEN_SECRET'])
        return token.decode('unicode_escape')

def parseToken(req):
    """
        Check if the token is correct
    """
    token = req.headers.get('Authorization').split()[1]
    return decode(token, app.config['TOKEN_SECRET'])

def loginRequired(f):
    """
        Decorator for use of token to have an access to a route
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #Allow OPTIONS request
        if request.headers.get("Access-Control-Request-Headers") == "authorization":
            response = jsonify(message="ok")
            response.status_code = 200
            return response

        #Reject request with no header Authorization
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parseToken(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_email = payload['sub']

        return f(*args, **kwargs)

    return decorated_function

def loginAdminRequired(f):
    """
        Decorator for use of token to have an access to a route
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #Allow OPTIONS request
        if request.headers.get("Access-Control-Request-Headers") == "authorization":
            response = jsonify(message="ok")
            response.status_code = 200
            return response

        #Reject request with no header Authorization
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parseToken(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response
        g.user_email = payload['sub']
        user = dbManager.get_user_by_email(g.user_email)
        if user and user.is_admin:
            return f(*args, **kwargs)
        else :
            response = jsonify(message='Not admin')
            response.status_code = 401
            return response
        

    return decorated_function

@app.route('/users')
@cross_origin()
@loginAdminRequired
def get_users():
    return jsonify(dbManager.get_all_users()), 200


@app.route('/users/<int:id_user>')
@cross_origin()
@loginAdminRequired
def get_user(id_user):
    user = dbManager.get_user_by_id(id_user)
    if user is None:
        abort(404)
    else:
        return jsonify(user), 200


@app.route('/users', methods=['POST'])
@cross_origin()
@loginAdminRequired
def add_user():
    data = request.form
    role = data.get('role', None)
    if dbManager.add_user(data['name'], data['surname'], role, data['email'], data['password'], data['is_admin']):
        return '', 201
    else:
        abort(400)


@app.route('/users/<int:id_user>', methods=['PUT'])
@cross_origin()
@loginAdminRequired
def update_user(id_user):
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
@cross_origin()
@loginAdminRequired
def delete_user(id_user):
    if dbManager.delete_user(id_user) is None:
        abort(404)
    else:
        return '', 200


@app.route('/offers')
@cross_origin()
@loginAdminRequired
def get_offers():
    return jsonify(dbManager.get_all_offers()), 200


@app.route('/offers/<int:id_offer>')
@cross_origin()
@loginRequired
def get_offer(id_offer):
    offer = dbManager.get_offer_by_id(id_offer)
    if offer is None:
        abort(404)
    else:
        return jsonify(offer), 200


@app.route('/offers', methods=['POST'])
@cross_origin()
@loginAdminRequired
def add_offer():
    data = request.form
    if dbManager.add_offer(data['title'], data['content'], data['descriptor'], data['id_user']):
        return '', 201
    else:
        abort(400)


@app.route('/offers/<int:id_offer>', methods=['PUT'])
@cross_origin()
@loginRequired
def update_offer(id_offer):
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
@cross_origin()
@loginRequired
def delete_offer(id_offer):
    if dbManager.delete_offer(id_offer) is None:
        abort(404)
    else:
        return '', 200


@app.route('/predictions')
@cross_origin()
@loginAdminRequired
def get_predictions():
    return jsonify(dbManager.get_all_predictions()), 200


@app.route('/predictions/<int:id_offer>')
@cross_origin()
@loginRequired
def get_prediction(id_offer):
    prediction = dbManager.get_prediction_by_id(id_offer)
    if prediction is None:
        abort(404)
    else:
        return jsonify(prediction), 200


@app.route('/predictions', methods=['POST'])
@cross_origin()
@loginAdminRequired
def add_prediction():
    data = request.form
    if dbManager.add_prediction(data['mark'], data['inbase'], data['id_offer']):
        return '', 201
    else:
        abort(400)


@app.route('/predictions/<int:id_prediction>', methods=['PUT'])
@cross_origin()
@loginAdminRequired
def update_prediction(id_prediction):
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
@cross_origin()
@loginAdminRequired
def delete_prediction(id_prediction):
    if dbManager.delete_prediction(id_prediction) is None:
        abort(404)
    else:
        return '', 200


@app.route('/teams')
@cross_origin()
@loginAdminRequired
def get_teams():
    return jsonify(dbManager.get_all_teams()), 200


@app.route('/fields')
@cross_origin()
@loginAdminRequired
def get_field():
    return jsonify(dbManager.get_all_fields()), 200


@app.route('/fields/<int:id_field>')
@cross_origin()
@loginRequired
def get_fields(id_field):
    field = dbManager.get_field_by_id(id_field)
    if field is None:
        abort(404)
    else:
        return jsonify(field), 200


@app.route('/fields', methods=['POST'])
@cross_origin()
@loginAdminRequired
def add_field():
    data = request.form
    if dbManager.add_field(data['name'], data['description'], data['descriptor'], data['website']):
        return '', 201
    else:
        abort(400)


@app.route('/fields/<int:id_field>', methods=['PUT'])
@cross_origin()
@loginAdminRequired
def update_field(id_field):
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
@cross_origin()
@loginAdminRequired
def delete_field(id_field):
    if dbManager.delete_field(id_field) is None:
        abort(404)
    else:
        return '', 200


@app.route('/contacts')
@cross_origin()
@loginAdminRequired
def get_contacts():
    return jsonify(dbManager.get_all_contacts()), 200


@app.route('/contacts/<int:id_contact>')
@cross_origin()
@loginRequired
def get_contact(id_contact):
    contact = dbManager.get_contact_by_id(id_contact)
    if contact is None:
        abort(404)
    else:
        return jsonify(contact), 200


@app.route('/contacts', methods=['POST'])
@cross_origin()
@loginAdminRequired
def add_contact():
    data = request.form
    email = data.get('email', None)
    phone = data.get('phone', None)
    role = data.get('role', None)
    if dbManager.add_contact(data['name'], data['surname'], email, phone, role, data['id_field']):
        return '', 201
    else:
        abort(400)


@app.route('/contacts/<int:id_contact>', methods=['PUT'])
@cross_origin()
@loginAdminRequired
def update_contact(id_contact):
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
@cross_origin()
@loginAdminRequired
def delete_contact(id_contact):
    if dbManager.delete_contact(id_contact) is None:
        abort(404)
    else:
        return '', 200

##############################AUTHETIFICATION
@app.route('/auth/signup', methods=['POST'])
@cross_origin()
def signup():
    data = json.loads(request.data)

    user = dbManager.get_user_by_email(data["email"])

    if user!=None:
        return jsonify(error="User already exist"), 404

    password = hashpw(data["password"].encode('utf-8'), gensalt())

    if dbManager.add_user(data["name"], data["surname"], data["role"], data['email'], password,False):
        session['logged_in'] = True
        user = dbManager.get_user_by_email(data["email"])
        return jsonify(user = user.serialize(), token=createToken(user)), 200
    else :
	    abort(400)

@app.route('/auth/login', methods=['POST'])
@cross_origin()
def login():
    data = json.loads(request.data)
    
    user = dbManager.get_user_by_email(data["emailUser"])

    if not user:
        return jsonify(error="No such user"), 404
    
    password = data["password"].encode('utf-8')
    
    if user.password== hashpw(password, user.password):
        session['logged_in'] = True    
        return jsonify(user = user.serialize(), token=createToken(user)), 200
    else:
        return jsonify(error="Wrong name or password"), 400


@app.route('/auth/logout', methods=['POST'])
@cross_origin()
@loginRequired
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'}), 200