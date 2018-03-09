# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.

"""

# import json
from flask import Flask, jsonify, request, json, session, g
from flask.json import jsonify
from flask import render_template, abort, request
from SmartRecruiting_BackEnd import app, dbManager
from SmartRecruiting_BackEnd.deeplearning.cnn.eval import FormationByOffer

from flask_cors import CORS, cross_origin
from functools import wraps
from bcrypt import gensalt, hashpw
from jwt import encode, decode, DecodeError, ExpiredSignature
from datetime import datetime, timedelta

from datetime import datetime
from SmartRecruiting_BackEnd.deeplearning.cnn.eval import load_eval


def createToken(user):
        """
            Create a token for a user with an expiration of 14 days
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
        Decorator for allowing a logged in user to access to the route
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Allow OPTIONS request
        if request.headers.get("Access-Control-Request-Headers") == "authorization":
            response = jsonify(message="ok")
            response.status_code = 200
            return response

        # Reject request with no header Authorization
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
        Decorator for allowing a logged in administrator to access to the route
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
    """
    Function to get all the users
    :return: {"user":{ "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str, "is_admin" : bool }}
    """
    return jsonify(dbManager.get_all_users()), 200

@app.route('/testCom')
@cross_origin()
def get_test_fields() :
    return jsonify("hello I am working :D"), 200


@app.route('/users/<int:id_user>')
@cross_origin()
@loginAdminRequired
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
@cross_origin()
@loginAdminRequired
def add_user():
    """
    METHOD : POST
    HEADER PARAM  : None
    BODY PARAMS : { "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str, "is_admin" : bool }
    """
    data = json.loads(request.data)
    role = data.get('role', None)
    if dbManager.add_user(data['name'], data['surname'], role, data['email'], data['password'], data['is_admin']):
        return '', 201
    else:
        abort(400)


@app.route('/users/<int:id_user>', methods=['PUT'])
@cross_origin()
@loginAdminRequired
def update_user(id_user):
    """
    METHOD : PUT
    HEADER PARAM  : id_user: int
    BODY PARAMS : { "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str,"is_admin" : bool }
    """
    data = json.loads(request.data)
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
    """
    METHOD : DELETE
    HEADER PARAM  : id_user: int
    """
    if dbManager.delete_user(id_user) is None:
        abort(404)
    else:
        return '', 200


@app.route('/offers')
@cross_origin()
@loginAdminRequired
def get_offers():
    """
    Function to get all the offers in the database
    :return: {"offer":{ "title" : str, "content" : str, "descriptor" : str, "id_user" : int }}
    """
    return jsonify(dbManager.get_all_offers()), 200

@app.route('/offers/page', methods=['POST'])
@cross_origin()
@loginAdminRequired
def recherche_page():
    """
    Function to get a page of the offers
    :METHOD : GET
    :HEADER PARAM  : none
    :BODY PARAMS : {"nb_offre": int ,"num_page":int}
    :return: number of the page, number total of page, a boolean to say
    if the page is the last, and the list of the offers
    """
    """
        Function to get the number of prediction between two date
        :return: int
        """
    data = json.loads(request.data)
    begin_date = data.get('begin_date', None)
    end_date = data.get('end_date', None)
    id_field = data.get('id_field', None)
    num_page_voulue, nb_pages, derniere_page, list_offre = dbManager.recherche(data['nb_offre'],
                                                                               data['num_page'],
                                                                               begin_date,
                                                                               end_date,
                                                                               id_field)
    if list_offre is None or derniere_page is None or nb_pages is None or num_page_voulue is None:
        abort(404)
    else:
        return jsonify({"page": num_page_voulue, "nb_pages": nb_pages, "is_last": derniere_page, "data": list_offre})

@app.route('/offers/<int:id_offer>')
@cross_origin()
@loginRequired
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
@cross_origin()
@loginAdminRequired
def add_offer():
    """
    METHOD : POST
    HEADER PARAM  : None
    BODY PARAMS : { "title" : str, "content" : str, "descriptor" : str, "id_user" : int }
    """
    data = json.loads(request.data)
    if dbManager.add_offer(data['title'], data['content'], data['descriptor'], data['id_user']):
        return '', 201
    else:
        abort(400)

@app.route('/offers/link', methods=['POST'])
@cross_origin()
@loginAdminRequired
def add_offer_link_field():
    """
    METHOD : POST
    HEADER PARAM  : None
    BODY PARAMS : { "title" : str, "content" : str, "id_user" : int, "id_field" : int, "inbase" : bool }
    """
    data = json.loads(request.data)
    id = dbManager.add_offer_link_field(data['title'], data['content'], data['id_user'], data['id_field'], data['inbase'])
    if id != -1 :
        return jsonify(id), 201
    else:
        abort(400)


@app.route('/offers/<int:id_offer>', methods=['PUT'])
@cross_origin()
@loginRequired
def update_offer(id_offer):
    """
    METHOD : PUT
    HEADER PARAM  : id_offer :int
    BODY PARAMS : { "title" : str, "content" : str, "descriptor" : str, "id_user" : int }
    """
    data = json.loads(request.data)
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
#@loginRequired
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
@cross_origin()
@loginAdminRequired
def get_predictions():
    """
    Function to get all the prediction in the database
    :return: {"predictions":{"mark": int, "inbase": bool, "id_offer": int}}
    """
    return jsonify(dbManager.get_all_predictions()), 200


@app.route('/predictions/<int:id_offer>')
@cross_origin()
@loginRequired
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
@cross_origin()
@loginAdminRequired
def add_prediction():
    """
    Function to add a prediction in the database
    :METHOD : POST
    :HEADER PARAM  : None
    :BODY PARAMS :{"mark": int, "inbase": bool, "id_offer": int}
    """
    data = json.loads(request.data)
    if dbManager.add_prediction(data['mark'], data['inbase'], data['id_offer']):
        return '', 201
    else:
        abort(400)


@app.route('/predictions/<int:id_prediction>', methods=['PUT'])
@cross_origin()
@loginAdminRequired
def update_prediction(id_prediction):
    """
    Function to update a prediction in the database
    :METHOD : PUT
    :HEADER PARAM  : id_prediction : int
    :BODY PARAMS :{"mark": int, "inbase": bool, "id_offer": int}
    """
    "TODO la mise a jour de inbase ne fonctionne pas pour une raison obscure"
    data = json.loads(request.data)
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
@cross_origin()
@loginAdminRequired
def get_teams():
    """
    Function to get all the teams in the database
    :return: {"predictions":{"mark": int, "inbase": bool, "id_offer": int}}
    """
    return jsonify(dbManager.get_all_teams()), 200


@app.route('/teams', methods=['POST'])
def add_team():
    """
    Function to add a team in the database
    :METHOD : POST
    :HEADER PARAM  : None
    :BODY PARAMS :{"id_prediction": int, "id_field": int, "nb_members": int}
    """
    data = json.loads(request.data)
    if dbManager.add_team(data['id_prediction'], data['id_field'], data['nb_members']):
        return '', 201
    else:
        abort(400)


@app.route('/teams/<int:id_prediction>', methods=['PUT'])
def update_teams(id_prediction):
    """
    Function to update a team in the database
    :METHOD : PUT
    :HEADER PARAM  : id_prediction :int
    :BODY PARAMS :{"id_prediction": int, "id_field": int, "nb_members": int}
    """
    data = json.loads(request.data)
    id_field = data.get('id_field', None)
    nb_members = data.get('nb_members', None)
    response = dbManager.update_team(id_prediction, id_field, nb_members)
    if response is None:
        abort(404)
    else:
        if response:
            return '', 200
        else:
            abort(400)


@app.route('/fields')
@cross_origin()
#@loginAdminRequired
def get_fields():
    """
    Function to get all the field in the database
    :return: {"fields":{"name": str, "description": str, "descriptor": str,"website": str}}
    """
    def complete_field(f) :
        f['contacts'] = dbManager.get_field_contacts(f['id'])
        return f
    fields = dbManager.get_all_fields()
    if fields :
        fields = [complete_field(f) for f in fields]
    else :
        abort(404)
    return jsonify(fields), 200

@app.route('/fields/nameonly')
@cross_origin()
@loginAdminRequired
def get_fields_name():
    """
    Function to get all the field in the database
    :return: {"fields":{"name": str, "description": str, "descriptor": str,"website": str}}
    """
    return jsonify(dbManager.get_all_fields_name()), 200

@app.route('/fields/<int:id_field>')
@cross_origin()
def get_field(id_field):
    """
    Function to get a field in the database
    :param id_field: int
    :return: {"field":{"id": int, "name": str, "description": str, "descriptor": str,"website": str, "contacts":}}
    """
    field = dbManager.get_field_by_id(id_field)
    print(field)
    if field is None:
        abort(404)
    else:
        contacts = dbManager.get_field_contacts(field['id'])
        field["contacts"] = contacts
        return jsonify(field), 200


@app.route('/fields', methods=['POST'])
@cross_origin()
#@loginAdminRequired
def add_field():
    """
    Function to add a field in the database
    :METHOD : POST
    :HEADER PARAM  : None
    :BODY PARAMS :{"name": str, "description": str, "descriptor": str,"website": str, "contacts":
        [{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int}, ...]
    }
    """
    data = json.loads(request.data)
    print(data['contacts'])
    field = dbManager.add_field(data['name'], data['description'], data['descriptor'], data['website'])
    if field != None:
        field['contacts'] = []
        for contact in data['contacts'] :
            created_contact = dbManager.add_contact(contact['name'],contact['surname'],contact['email'],contact['phone'],contact['role'],field['id'])
            if created_contact :
                field['contacts'].append(created_contact)
            else :
                abort(400)
        return jsonify(field), 201
    else:
        abort(400)


@app.route('/fields/<int:id_field>', methods=['PUT'])
@cross_origin()
#@loginAdminRequired
def update_field(id_field):
    """
    Function to update a field in the database
    :METHOD : PUT
    :HEADER PARAM  : id_field : int
    :BODY PARAMS :{"name": str, "description": str, "descriptor": str,"website": str}
    """
    data = json.loads(request.data)
    name = data.get('name', None)
    description = data.get('description', None)
    descriptor = data.get('descriptor', None)
    website = data.get('website', None)
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
#@loginAdminRequired
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
@cross_origin()
@loginAdminRequired
def get_contacts():
    """
    Function to get all the contact in the database
    :return: {"contact":{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int}}
    """
    return jsonify(dbManager.get_all_contacts()), 200


@app.route('/contacts/<int:id_contact>')
@cross_origin()
@loginRequired
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
@cross_origin()
#@loginAdminRequired
def add_contact():
    """
    Function to add a contact in the database
    :METHOD : POST
    :HEADER PARAM  : None
    :BODY PARAMS :{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int}
    """

    data = json.loads(request.data)
    email = data.get('email', None)
    phone = data.get('phone', None)
    role = data.get('role', None)
    contact = dbManager.add_contact(data['name'], data['surname'], email, phone, role, data['id_field'])
    if contact != None :
        return jsonify(contact), 201
    else:
        abort(400)


@app.route('/contacts/<int:id_contact>', methods=['PUT'])
@cross_origin()
#@loginAdminRequired
def update_contact(id_contact):
    """
    Function to update a contact in the database
    :METHOD : PUT
    :HEADER PARAM  : id_contact : int
    :BODY PARAMS :{"name": str, "surname": str, "email": str,"phone": str,"role": str,"id_field": int}
    """
    data = json.loads(request.data)
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
#@loginAdminRequired
def delete_contact(id_contact):
    """
    Function to delete a contact in the database
    :METHOD : DELETE
    :HEADER PARAM  : id_contact : int
    """

    if dbManager.delete_contact(id_contact) is None:
        abort(404)
    else:
        return '', 200


@app.route('/searchOffersByField/<int:id_field>', methods=['GET'])
def offers_by_field(id_field):
    """
    Function to get all the offers who correspond to a field
    :METHOD : GET
    :HEADER PARAM  : id_field : int
    :BODY PARAMS : none
    :return: {"offer":{ "title" : str, "content" : str, "descriptor" : str, "id_user" : int }}
    """

    offers = dbManager.offers_by_field(id_field)
    if offers is None:
        abort(404)
    else:
        return jsonify(offers), 200


@app.route('/searchFieldsByOffer/<int:id_offer>', methods=['GET'])
def fields_by_offer(id_offer):
    """
    Function to get all the field who correspond to an offer
    :METHOD : GET
    :HEADER PARAM  : id_offer : int
    :BODY PARAMS : none
    :return: {"fields":{"id": int,"name": str,"inbase": boolean}}
    """
    fields = dbManager.fields_by_offer(id_offer)
    if fields is None:
        abort(404)
    else:
        return jsonify(fields), 200


@app.route('/generatePrediction', methods=['POST'])
@cross_origin()
def generatePrediction():
    """
    METHOD : POST
    HEADER PARAM  : None
    BODY PARAMS : { "title" : str, "content" : str, "descriptor" : str, "id_user" : int }
    RETURNS :
        {
            "field": { "name": str, "description": str, "descriptor": str, "website": str }
        }
    """
    data = json.loads(request.data)
    print ("-------------------------------------JSON data ----------------------------------------")
    print(data['content'])
    idfield=FormationByOffer(data['content'])

    field = dbManager.get_field_by_id(idfield)
    if field is None:
        abort(404)
    else:
        return jsonify(field), 200


@app.route('/SaveGeneratePrediction', methods=['POST'])
@cross_origin()
@loginRequired
def generatePrediction_save():
    '''
    not data.descriptor
    '''
    data = json.loads(request.data)
    idfield = FormationByOffer(data['content'])
    #ten = np.zeros(3, int)
    #ten[idfield] = 1
    field = dbManager.get_field_by_id(idfield)
    dbManager.add_offer(data['title'], data['content'], data['descriptor'], data['id_user'])
    if field is None:
        abort(404)
    else:
        return jsonify(field), 200


@app.route('/searchOffersByUser/<int:id_user>', methods=['GET'])
def offers_by_user(id_user):
    """
    Function to get all the offers who correspond to an user
    :METHOD : GET
    :HEADER PARAM  : id_user : int
    :BODY PARAMS : none
    :return: {"offer":{ "title" : str, "content" : str, "descriptor" : str, "id_user" : int }}
    """
    offers = dbManager.offers_by_user(id_user)
    if offers is None:
        abort(404)
    else:
        return jsonify(offers), 200


@app.route('/averageMark/', methods=['GET'])
def average_mark():
    """
    Function to get the average of the prediction mark between to date
    :METHOD : GET
    :HEADER PARAM  : {"begin_date": date,"end_date":date}
    :BODY PARAMS : none
    :return: int
    """
    begin_date = request.args.get('begin_date')
    begin_date = datetime.strptime(begin_date, "%Y-%m-%d").date()
    end_date = request.args.get('end_date')
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    mark = dbManager.average_mark(begin_date, end_date)
    if mark is None:
        abort(404)
    else:
        return jsonify(mark), 200


@app.route('/nbPrediction/', methods=['GET'])
@cross_origin()
@loginAdminRequired
def nb_prediction():
    """
    Function to get the number of prediction between two date
    :METHOD : GET
    :HEADER PARAM  : {"begin_date": date,"end_date":date}
    :BODY PARAMS : none
    :return: int
    """
    begin_date = request.args.get('begin_date')
    begin_date = datetime.strptime(begin_date, "%Y-%m-%d").date()
    end_date = request.args.get('end_date')
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    number = dbManager.nb_prediction(begin_date, end_date)
    if number is None:
        abort(404)
    else:
        return jsonify(number), 200

@app.route('/accuracy', methods=['GET'])
@cross_origin()
@loginAdminRequired
def get_accuracy():
    nb_test, accuracy = load_eval()

    if nb_test is None or accuracy is None:
        abort(404)
    else:
        return jsonify(nb_test, accuracy), 200


##############################AUTHETIFICATION
@app.route('/update_prediction_by_id_offer', methods=['POST'])
@cross_origin()
@loginAdminRequired
def update_prediction_by_id_offer():
    data = json.loads(request.data)
    in_base = data.get('in_base', None)
    id_field = data.get('in_base', None)
    if dbManager.update_prediction_by_id_offer(data['id_offer'], id_field, in_base):
        return '', 201
    else:
        abort(400)



# #############################AUTHETIFICATION


@app.route('/auth/signup', methods=['POST'])
@cross_origin()
def signup():
    """
    METHOD : POST
    HEADER PARAM  : None
    BODY PARAMS : { "name" : str, "surname" : str, "role" : str, "email" : str, "password" : str }
    RETURNS :
        {
            "token": str,
            "user": { "email": str, "id": int, "is_admin": boolean, "name": str, "password": str, "role": str, "surname": str }
        }
    """
    data = json.loads(request.data)

    user = dbManager.get_user_by_email(data["email"])

    if user != None:
        return jsonify(error="User already exist"), 404

    password = hashpw(data["password"].encode('utf-8'), gensalt())

    if dbManager.add_user(data["name"], data["surname"], data["role"], data['email'], password, False):
        session['logged_in'] = True
        user = dbManager.get_user_by_email(data["email"])
        return jsonify(user = user.serialize(), token=createToken(user)), 200
    else:
        abort(400)


@app.route('/auth/login', methods=['POST'])
@cross_origin()
def login():
    """
    METHOD : POST
    HEADER PARAM  : None
    BODY PARAMS : { "emailUser" : str, "password" : str}
    RETURNS :
        {
            "token": str,
            "user": { "email": str, "id": int, "is_admin": boolean, "name": str, "password": str, "role": str, "surname": str }
        }
    """
    data = json.loads(request.data)

    user = dbManager.get_user_by_email(data["emailUser"])

    if not user:
        return jsonify(error="No such user"), 404

    password = data["password"].encode('utf-8')

    if user.password == hashpw(password, user.password):
        session['logged_in'] = True
        return jsonify(user = user.serialize(), token=createToken(user)), 200
    else:
        return jsonify(error="Wrong name or password"), 400


@app.route('/auth/logout', methods=['POST'])
@cross_origin()
@loginRequired
def logout():
    """
    METHOD : POST
    HEADER PARAM  : {Authorization : Bearer token}
    BODY PARAMS : None
    RETURNS : { 'result': 'success' }
    """
    session.pop('logged_in', None)
    return jsonify({'result': 'success'}), 200
