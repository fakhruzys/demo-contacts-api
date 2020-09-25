# demo-contacts-api

All of the instructions are for Windows platform

## Instructions on setting up

The program is built using python 3.7.4 with the following packages:

* flask
* flask_pymongo
* bson
* marshmallow
* flask_request_validator

If you are using Anaconda you can install them using the following commands in your anaconda prompt:

* conda install -c anaconda flask
* pip install Flask-PyMongo
* conda install -c conda-forge bson
* conda install -c conda-forge marshmallow
* pip install flask_request_validator

If you are not using Anaconda then you can just use pip install <package>
    
Make sure also you have installed MongoDB on your local machine to run the program.

## Running the Program

1. Open up your anaconda prompt (windows command prompt also works if you have installed all the packages earlier on your python) and type : python Contacts_API.py . This should run the program.

2. To use the POST method, you can use the following command (insert the command on the anaconda/windows command prompt):

### POST/people
* curl -i -H "Content-Type: application/json" -X POST -d "{""name"":""Ultron"",""age"":22,""height"":144}" http://localhost:5000/people

When you insert the above command on the command prompt, it will tell you the id of the people inserted. Copy that id to be used for the following command

### POST/people/<:id>/contacts
* curl -i -H "Content-Type: application/json" -X POST -d "{""email"":""test@yahoo.com"",""number"":""0122223212""}" http://localhost:5000/people/5f6c9f5fe34392c85008d415/contacts

The id is different for each person, so be sure to save the id elsewhere if you are trying to add the contacts to a particular person

3. To use the GET method, you can also use the curl method:

### GET/contacts?q=<:query>

* curl -i http://localhost:5000/contactsq?=<:query>

or you can just type into the url which is easier:

* http://localhost:5000/contactsq?=<:query>

The sample commands can be found in the commands.txt file
