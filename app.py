import os
import pymongo
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

#DBS_NAME = 'my_data_project'
app.config["MONGO_DBNAME"] = "my_data_project"
MONGODB_URI = os.getenv("MONGO_URI")

#mongo = PyMongo(app)

app.route('/')
def hello():
    return "Hello World.... again!"


if __name__ == '__main__':
    app.run(host='0.0.0.0',
    port=int('8080'),
    debug=True)