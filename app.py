import os
import pymongo
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "my_data_project"
MONGO_URI = os.environ.get('MONGO_URI') 
mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def hello():
    return render_template('index.html')


@app.route('/readrecipe')
def get_recipe():
    return render_template('readrecipe.html', 
    recipes=mongo.db.recipes.find())
    

if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
        port=int(os.getenv('PORT')), 
        debug=False)