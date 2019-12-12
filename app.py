import os
import pymongo
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "my_data_project"
app.config["MONGODB_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def hello():
    return render_template('index.html')


@app.route('/readrecipe')
def get_recipe():
    return render_template('readrecipe.html', 
    recipes=mongo.db.dish_names.find())
    

if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
        port=int(os.getenv('PORT')), 
        debug=False)