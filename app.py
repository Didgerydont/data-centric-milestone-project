import os
import pymongo
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get('my_data_project')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
mongo = PyMongo(app)

username = mongo.db.users.find()

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')

# User login
@app.route("/login", methods=['POST'])
def login():
    users=mongo.db.users
    user_login = users.find_one({'user_name': request.form['username']})
    if user_login:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), user_login['password'].encode('utf-8')) == user_login['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('login_successful'))

    return 'Invalid username/password combination'

@app.route("/login_successful")
def login_sucess():
    if 'username' in session:
        return "You are logged in as " + session['username']

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
            return redirect(url_for('index'))

        return 'Someone already uses that name. Try another'

    return render_template('register.html')


@app.route('/readrecipe')
def get_recipe():
    return render_template('readrecipe.html', 
    recipes=mongo.db.recipes.find())
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=(os.environ.get('PORT')),
            debug=True)