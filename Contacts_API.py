# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:06:53 2020

@author: Dell
"""

from flask import Flask, request, abort, jsonify, make_response
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'contactdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/contactdb'
app.config['JSON_SORT_KEYS'] = False

mongo = PyMongo(app)


@app.route('/')
def index():
    return "Contact API for Air Asia Assesment!"

@app.route('/contacts', methods=['GET'])
def get_contacts():
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
    contact = mongo.db.contact
    person = {
            'name': request.json['name'],
            'age': request.json['age'],
         'height': request.json['height']
              }
    contact_id = contact.insert_one(person).inserted_id
    #people.append(person)
    return "Inserted Successfully with the id {}".format(contact_id), 201

@app.route('/people/<string:id>/contacts', methods=['POST'])
def add_contacts(id):
    if not request.json:
        abort(400)
    contact = mongo.db.contact
    additional_contact = {
           #'_id' : id,
         'email' : request.json['email'],
         'number': request.json['number']
               }
    contact.update_one({"_id":ObjectId(id)},{ "$set" : {"contacts" : additional_contact}})
    return "Inserted Successfully at {}".format(id), 201
            

if __name__ == "__main__":
    app.run(debug=True)