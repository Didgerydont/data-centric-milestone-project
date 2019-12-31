import os
import pymongo
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get('my_data_project')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
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
    app.run(host='0.0.0.0',
            port=(os.environ.get('PORT')),
            debug=True)