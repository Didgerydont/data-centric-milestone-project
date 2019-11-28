import os
##import pymongo
from flask import Flask
#from flask_pymongo import PyMongo
#from bson.objectid import ObjectId

app = Flask(__name__)

#DBS_NAME = 'my_data_project'
#MONGO_URI = os.getenv('MONGO_URI')

#mongo = PyMongo(app)

app.route('/')
def hello():
    return "Hello World.... again!"


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)