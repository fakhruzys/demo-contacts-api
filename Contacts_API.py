# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:06:53 2020

@author: Dell
"""

from flask import Flask, request, abort, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from marshmallow import Schema, fields, ValidationError
from flask_request_validator import (Param, GET, validate_params)

def validate_id(n):
    contact = mongo.db.contact
    if ObjectId.is_valid(n):
            if contact.count_documents({ '_id': ObjectId(n) }, limit = 1) > 0:
                return True
            else:
                abort(400, "Id does not exist")
    else:
        abort(400,"Id not valid")

class PeopleSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)
    height = fields.Integer(required=True)

class ContactsSchema(Schema):
    email = fields.Email(required=True)
    number = fields.String(required=True)

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'contactdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/contactdb'
app.config['JSON_SORT_KEYS'] = False

mongo = PyMongo(app)


@app.route('/')
def index():
    return "Contact API for Air Asia Assesment!"

@app.route('/contacts', methods=['GET'])
@validate_params(Param('q', GET, str, required=True))
def get_contacts(query):
    query = request.args.get('q')
    contact = mongo.db.contact

    if "@" in query:
        find = contact.find_one({'contacts.email': query})
        if find:
            result = {'name': find['name'], 'age': find['age'], 'height': find['height']}
            return result
        else:
            return "No data"
    elif query.isdigit():
        find = contact.find_one({'contacts.number': query})
        if find:
            result = {'name': find['name'], 'age': find['age'], 'height': find['height']}
            return result
        else:
            return "No data"
    else:    
        find = contact.find_one({'name': query})
        if find:
            result = {'name': find['name'], 'age': find['age'], 'height': find['height']}
            return result
        else:
            return "No data"


@app.route('/people', methods=['POST'])
def add_person():
    if not request.json:
        abort(400)
    schema = PeopleSchema()
    try:
        schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    contact = mongo.db.contact
    person = {
            'name': request.json['name'],
            'age': request.json['age'],
         'height': request.json['height']
              }
    contact_id = contact.insert_one(person).inserted_id
    return "Inserted Successfully with the id {}".format(contact_id), 201

@app.route('/people/<string:id>/contacts', methods=['POST'])
def add_contacts(id):
    if not request.json:
        abort(400)
    validate_id(id)
    contact = mongo.db.contact
    schema = ContactsSchema()
    try:
        schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    additional_contact = {
         'email' : request.json['email'],
         'number': request.json['number']
               }
    contact.update_one({"_id":ObjectId(id)},{ "$set" : {"contacts" : additional_contact}})
    return "Inserted Successfully at {}".format(id), 201
            

if __name__ == "__main__":
    app.run(debug=True)