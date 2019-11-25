import os
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectId import ObjectId

app = Flask(__name__)

#app.config['MONGO_DBNAME'] = 'MongoDb project name when ready for wiring'
#app.config['MONGO_URI'] = 'This will be connection as provided by MongoDB'   // dont forget to hide password in bashrc and import from OS

#mongo = PyMongo(app)


app.route('/')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)