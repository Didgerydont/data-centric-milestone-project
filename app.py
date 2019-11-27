import os
import pymongo
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

DBS_NAME = 'my_data_project'
MONGODB_URI = os.getenv("MONGO_URI")


app.route('/')
def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected")
        return conn
        
    except pymongo.errors.ConnectionFailure as e:
        print("could not connect to MongoDB: %s") % e

#mongo = PyMongo(app)







if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)