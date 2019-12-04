import os
import pymongo
from flask import Flask, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

#DBS_NAME = 'my_data_project'
#app.config["MONGO_DBNAME"] = "my_data_project"
#MONGO_URI = os.getenv("MONGO_URI")

#mongo = PyMongo(app)

@app.route("/")
def hello():
    return "Hello World.... again!"
    
    


if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
        port=int(os.getenv('PORT')), 
        debug=False)