import os
import pymongo
import time
from flask import Flask, render_template, redirect, request, url_for, session
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
from datetime import datetime
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, URL, ValidationError
from flask_wtf import FlaskForm
if os.path.exists("env.py"):
    import env
#app configuration
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get('my_data_project')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
mongo = PyMongo(app)
login = LoginManager(app)
login.login_view = 'login'

#Flask-login config
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)



# find stored usernames
username = mongo.db.users.find()

user_present = False # remember if user has logged in.


#login class
class loginForm(FlaskForm):

    login_username = StringField('Username', validators=[InputRequired()])
    login_password = PasswordField('Password', validators=[InputRequired()])

class registrationForm(FlaskForm):
    register_username = StringField('Select a Username', validators=[InputRequired()])
    register_password = PasswordField('Select a Password', validators=[InputRequired()])

#create recipe class
class createRecipe(FlaskForm):
    
    recipe_title = StringField('Title', validators=[InputRequired()])
    recipe_description = StringField('Description', validators=[InputRequired()])        
    recipe_method = StringField('Method', validators=[InputRequired()])
    recipe_ingredients = StringField('Ingredients', validators=[InputRequired()])
    recipe_meal_type = StringField('Meal Type', validators=[InputRequired()])
    recipe_serves = IntegerField('Serves', validators=[InputRequired()])
    recipe_preptime = StringField('Preperation',validators=[InputRequired()])
    recipe_cooktime = StringField('Cooking Time', validators=[InputRequired()])
    recipe_origin = StringField('Country of Origin', validators=[InputRequired()])




# Home
@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')

# User login

@app.route('/login_landing')
def login_landing():
    form = loginForm(request.form) 
    return render_template('login.html', form=form)

@app.route("/login", methods=['POST'])
def logging_in():
    users=mongo.db.users
    user_login = users.find_one({'user_name': request.form['login_username']})

    if user_login:
        if bcrypt.hashpw(request.form['login_password'].encode('utf-8'), user_login['password']) == user_login['password']:
            session['username'] = request.form['login_username']
            
            return redirect(url_for('login_success'))

    return 'Invalid username/password combination'

@app.route("/login_success")
def login_success():
    if 'username' in session:
        return render_template('login_success.html')

# User registration

@app.route("/registration_landing")
def registration_landing():
    form = registrationForm(request.form) 
    return render_template('register.html', form=form)

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        
        users=mongo.db.users
        existing_user = users.find_one({'user_name': request.form['register_username']})

        if existing_user == None:
            hashpass = bcrypt.hashpw(request.form['register_password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'user_name' : request.form['register_username'], 'password' : hashpass})
            session['username'] = request.form['register_username']
            return redirect(url_for('login_success'))

        return 'Someone already uses that name. Try another'

    return render_template('register.html')

# -----> CRUD

# Create
@app.route('/add_recipe')
def add_recipe():
    form = createRecipe(request.form)        
    return render_template('addrecipe.html', form=form)

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():

    recipes = mongo.db.recipes

    recipe_title = request.form['recipe_title']
    recipe_description = request.form['recipe_description']
    recipe_method = request.form['recipe_method']
    recipe_ingredients = request.form['recipe_ingredients']
    recipe_meal_type = request.form['recipe_meal_type']
    recipe_serves = request.form['recipe_serves']
    recipe_cooktime = request.form['recipe_cooktime']
    recipe_preptime = request.form['recipe_preptime']
    recipe_origin = request.form['recipe_origin']
    # Still have to figure out how to keep the user logged in

    recipe_form = {
        "title": recipe_title,
        "description": recipe_description,
        "method": recipe_method,
        "ingredients": recipe_ingredients,
        "meal": recipe_meal_type,
        "serves": recipe_serves, 
        "cooking_time": recipe_cooktime,
        "prep_time": recipe_preptime,
        "country_of_origin": recipe_origin,
        "last_modified": time.asctime(time.localtime(time.time()))
        # Still have to figure out how to keep the user logged in
    }

    recipes.insert_one(recipe_form)
    return redirect(url_for('uploadconfirmation'))

@app.route('/uploadconfirmation')
def uploadconfirmation():
    return render_template('uploadconfirmation.html')


# Read --> Shows all recipes as a directory. 
@app.route('/readrecipe')
def get_recipe():
    return render_template('readrecipe.html', 
    recipes=mongo.db.recipes.find())
    


## Come back to Search, must find another as Mongo shell cant be used on this version of gitpod
# Search bar
#@app.route('/search_bar/', methods=["POST"])
#def search_bar():
#    search_term = request.form['search_text']
#    if (search_term != ""):
#        return redirect(url_for('search_results', search_text=search_term))
#    else:
#        return render_template("recipes.html", recipes=mongo.db.recipes.find())

#@app.route('/search_results/<search_text>')
#def search_results(search_text):
#    search_results = mongo.db.recipes.find(
#        {'$text': {'$search': search_text}})
  
  
   # return render_template("readrecipe.html", recipes=search_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=(os.environ.get('PORT')),
            debug=True)