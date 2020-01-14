import os
import pymongo
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
from datetime import datetime
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired, URL, ValidationError
from flask_wtf import FlaskForm
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get('my_data_project')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
mongo = PyMongo(app)

username = mongo.db.users.find()

class createRecipe(FlaskForm):
    recipe_title = StringField('title', validators=[InputRequired()])
    recipe_description = StringField('description', validators=[InputRequired()])
    recipe_method = StringField('method', validators=[InputRequired()])
    recipe_ingredients = StringField('ingredients', validators=[InputRequired()])
    recipe_meal_type = StringField('meal_type', validators=[InputRequired()])
    recipe_serves = IntegerField('serves', validators=[InputRequired()])
    recipe_preptime = SelectField('prep', choices=[('0-30m', '0-30 minutes'),
        ('30-60','30-60 minutes'), ('60-90', '60-90 minutes'),
        ('90+', '90+ minutes')] ,validators=[InputRequired()])
    recipe_cooktime = SelectField('cooking_time', choices=[('0-30', '0-30 minutes'),
        ('30-60','30-60 minutes'), ('60-90', '60-90 minutes'),
        ('90+', '90+ minutes')] ,validators=[InputRequired()])
    recipe_origin = StringField('origin', validators=[InputRequired()])


# Home
@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')

# User login

@app.route('/login_landing')
def login_landing():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login():
    users=mongo.db.users
    user_login = users.find_one({'user_name': request.form['username']})

    if user_login:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), user_login['password']) == user_login['password']:
            session['username'] = request.form['username']
            return redirect(url_for('login_success'))

    return 'Invalid username/password combination'

@app.route("/login_success")
def login_success():
    if 'username' in session:
        return render_template('login_success.html')

# User registration
@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users=mongo.db.users
        existing_user = users.find_one({'user_name': request.form['username']})

        if existing_user == None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'user_name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('login_success'))

        return 'Someone already uses that name. Try another'

    return render_template('register.html')

# -----> CRUD

# Create
@app.route('add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = createRecipe(request.form)
    return render_template('addrecipe.html', form=form)

# Read --> Shows all recipes as a directory. 
@app.route('/readrecipe')
def get_recipe():
    return render_template('readrecipe.html', 
    recipes=mongo.db.recipes.find())
    


## Come back to Search, must find another as Mongo shell cant be used on this version of gitpod
# Search bar
@app.route('/search_bar/', methods=["POST"])
def search_bar():
    search_term = request.form['search_text']
    if (search_term != ""):
        return redirect(url_for('search_results', search_text=search_term))
    else:
        return render_template("recipes.html", recipes=mongo.db.recipes.find())

@app.route('/search_results/<search_text>')
def search_results(search_text):
    search_results = mongo.db.recipes.find(
        {'$text': {'$search': search_text}})
  
  
    return render_template("readrecipe.html", recipes=search_results)







if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=(os.environ.get('PORT')),
            debug=True)