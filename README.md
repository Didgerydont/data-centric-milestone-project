# Recipe Hub - Data Centric Milestone Project
The focus of this project is to display the CRUD principle of database orientated software development and design. 

## UX
The goal for the UX of this project was to keep the general layout straightforward and easy to use. 
Use this section to provide insight into your UX process, focusing on who this website is for, what it is that they want to achieve and how your project is the best way to help them achieve these things.

In particular, as part of this section we recommend that you provide a list of User Stories, with the following general structure:

#### User Stories
"As an avid cooking enthusiast, I am looking for a website that is easy to navigate and that allows me to keep recipes I encounter or create all in one easy to manage place."

"As a professional, I would like to be able to view other peoples recipes to take my inspiration from. "

"As a parent, Im stuck for time and want to be able to get to the recipes within a couple clicks without having to navigate through a mountain of options."

"As an advertising partner, I want my site to seem attractive to your end users and for them to be able to get to my site quickly from yours" 

#### Wireframes
Below are the original wireframes that I drew up before I began working on the project. Although the project has changed from these original wireframes,
the general idea has stayed along the same lines. Albeit, with a few differences. As work began on the project these original plans as the same outline and shape 
wouldnt have worked as the general project had to adapt to code that I was writing. 

![wireframe](https://github.com/Didgerydont/data-centric-milestone-project/blob/master/static/img/data_centric_wireframe_1.JPG "wireframe_1")
![wireframe](https://github.com/Didgerydont/data-centric-milestone-project/blob/master/static/img/data_centric_wireframe_2.JPG "wireframe_2")
![wireframe](https://github.com/Didgerydont/data-centric-milestone-project/blob/master/static/img/data_centric_wireframe_3.JPG "wireframe_3")

#### Database Schema
![schema](https://github.com/Didgerydont/data-centric-milestone-project/blob/master/static/img/data_centric_wireframe_schema.JPG "Schema")

#### Database in Action
##### Recipes
![recipes](https://github.com/Didgerydont/data-centric-milestone-project/blob/master/static/img/data_centric_wireframe_recipes.JPG "Recipes")

##### Users
The login and registration blocks use bcrypt to salt the users passwords for extra security
![users](https://github.com/Didgerydont/data-centric-milestone-project/blob/master/static/img/data_centric_wireframe_users.JPG "Users")

## Features
The project has multiple features based on the CRUD principle. 
As per the project requisits I have developed this project in [Python](https://www.python.org/) through the [Flask](https://flask.palletsprojects.com/) framework
in order to provide its back-end functionality. 

### Login, Registration and Session Cookies
The project allows users to login and register to the website. The user is never prompted to make a profile with the website
unless they try to access a function that allows edits to be made to the database.

#### Registration
The site uses WTForms and Flask-Wtf to do the backend of the forms functions. This involves setting up classes and using framework
to set the up the "username" and "password" fields. 

```python
class loginForm(FlaskForm):

    login_username = StringField('Username', validators=[InputRequired()])
    login_password = PasswordField('Password', validators=[InputRequired()])

class registrationForm(FlaskForm):
    register_username = StringField('Select a Username', validators=[InputRequired()])
    register_password = PasswordField('Select a Password', validators=[InputRequired()])

```


I then set up the registration system through my route. For this I used Bcrypt to protect the privacy and added security to users account information.

```python
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



```
#### Login
The login will take the details that the user has saved earlier. Re-salt them and allow then access if 
the password and username match


```python
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
```


#### Session Cookie
The site also makes use of session cookies to remember that the user is logged in in order to access our
functions that allow alterations to be made to the database. 




```python
#This is line appears in the previous lines of code and creates our cookie.
session['username'] = request.form['login_username']

#Then we check if the username has been confirmed in the session before allowing the user to make the alteration. 
#The add recipe is below an example
@app.route('/add_recipe')
def add_recipe():
    if 'username' in session:
        form = createRecipe(request.form)        
        return render_template('addrecipe.html', form=form)
    else:
        return render_template('sign_in_required.html')
```


### CRUD
I have 3 functions that follow this principle.

#### Read Recipe
This function reads all of the recipes that have been uploaded to the directory. Its shows all of the
previously input data. The recipes utilizes the [Materialize css](https://materializecss.com/) frameworks
built in accordian in order to display the recipes as individual cards. They also uses Materializes built
javascript to make tiles hover when the cursor is detected within the div.
```html
<div class="row">
<h2 class="center headers">Recipe Directory</h2> 
    {% for recipe in recipes %} 
    <div class="container find-recipe-container">
        <ul class="collapsible">
            <li>
                <div class="collapsible-header title-header hoverable">
                    <div class="row">
                        <div class="col s2 mt1em"><i class="material-icons">expand_more</i></div>
                        <div class="col s10 header-align"><h3 class="recipe-header browser-default headers">{{recipe.title}}</h3></div>
                    </div>
                </div>
                    <div class="collapsible-body">
                        <div class="row">
                            <div class="col s12">
                                <div class="card">
                                    <div class="card-image">
                                    </div>
                                    <div class="card-content recipe-description">
                                        <h4 class="recipe-header headers center-align">Description</h4>
                                        <p class="center-align">{{recipe.description}}</p>

                                    </div>
                                    <br>    
                                    <div class="card-content recipe-method">
                                        <h4 class="recipe-header headers center-align">Method</h4>
                                        <p class="center-align">{{recipe.method}}</p>

                                    </div>
                                    <br>
                                    <div class="card-content recipe-ingredients">
                                        <h4 class="recipe-header headers center-align">Ingredients</h4>
                                        <p class="center-align">{{recipe.ingredients}}</p>

                                    </div>
                                    <br>
                                    <div class="card-content recipe-meal">
                                        <h4 class="recipe-header headers center-align">Meal Type</h4>
                                        <p class="center-align">{{recipe.meal}}</p>

                                    </div>
                                    <br>
                                    <div class="card-content recipe-serves">
                                        <h4 class="recipe-header headers center-align">Servings</h4>
                                        <p class="center-align">{{recipe.serves}}</p>

                                    </div>
                                    <br>
                                    <div class="card-content recipe-prep-time">
                                        <h4 class="recipe-header headers center-align">Preperation Time</h4>
                                        <p class="center-align">{{recipe.prep_time}}</p>

                                    </div>
                                    <br>
                                    <div class="card-content recipe-cooking-time">
                                        <h4 class="recipe-header headers center-align">Cooking Time</h4>
                                        <p class="center-align">{{recipe.cooking_time}}</p>

                                    </div>
                                    <br>
                                    <div class="card-content recipe-country-of-origin">
                                        <h4 class="recipe-header headers center-align">Country of Origin</h4>
                                        <p class="center-align">{{recipe.country_of_origin}}</p>

                                    </div>
                                    <br>
                                    <div class="card-content recipe-user-name">
                                        <h4 class="recipe-header headers center-align">Uploaded by</h4>
                                        <p class="center-align">{{recipe.user_name}}</p>

                                    </div>
                                    <br>
                                    <div class="edit-delete-buttons-container edit-delete-buttons">
                                        <a href="{{ url_for('edit_recipe', recipe_id=recipe._id) }}" class="btn btn-primary btn-block green lighten-2 center">Edit</a>
                                        <a href="{{ url_for('delete_recipe', recipe_id=recipe._id) }}" class="btn btn-primary btn-block green lighten-2 center">Delete</a> 
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </li>
        </ul>
    </div>
    {% endfor %}

```

#### Edit Recipe
The edit recipe function is accessed via the previous read recipe function. This requires the user to be logged in
by use of a session cookie. The user will be asked to set up a page in order to make the edit. If the user is logged in
but is trying to edit someones elses recipes. They will be advised that they can only edit their own recipes.
This will be delivered by Flasks "Flash" function.

```python
@app.route('/edit_recipe/<recipe_id>', methods=['GET'])
def edit_recipe(recipe_id):
    if 'username' in session:
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        user_recipes = mongo.db.recipes.find({"user_name": session['username']})
        if recipe in user_recipes:
            form = editRecipe(request.form)
            form.recipe_title.data = recipe["title"]
            form.recipe_description.data = recipe["description"]
            form.recipe_ingredients.data = recipe["ingredients"]
            form.recipe_method.data = recipe["method"]
            form.recipe_meal_type.data = recipe["meal"]
            form.recipe_serves.data = recipe["serves"]
            form.recipe_preptime.data = recipe["prep_time"]
            form.recipe_cooktime.data = recipe["cooking_time"]
            form.recipe_origin.data = recipe["country_of_origin"]
            return render_template('edit_recipe.html', recipe=recipe, user_recipes=user_recipes, form=form)
        else:
            flash('You can only alter your own recipes')
            return render_template('sign_in_required.html')
    return render_template('sign_in_required.html')

@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    
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

    recipes.update({'_id': ObjectId(recipe_id)},
        {
        "title": recipe_title,
        "description": recipe_description,
        "method": recipe_method,
        "ingredients": recipe_ingredients,
        "meal": recipe_meal_type,
        "serves": recipe_serves, 
        "cooking_time": recipe_cooktime,
        "prep_time": recipe_preptime,
        "country_of_origin": recipe_origin,
        "last_modified": time.asctime(time.localtime(time.time())),
        "user_name": session['username']
        })

    
    return redirect(url_for('uploadconfirmation'))
```

The previous recipe information will be displayed to the user within the form that they are filling in so that 
they can alter the recipe whiles knowing what was in there previous. WTForms is used once again in order to
provide provide the backend classes and allowing us to display the previous information within the form.


```python
class editRecipe(FlaskForm):
    
    recipe_title = StringField('Title', validators=[InputRequired()])
    recipe_description = TextAreaField('Description', validators=[InputRequired()])        
    recipe_method = TextAreaField('Method', validators=[InputRequired()])
    recipe_ingredients = TextAreaField('Ingredients', validators=[InputRequired()])
    recipe_meal_type = StringField('Meal Type', validators=[InputRequired()])
    recipe_serves = Stringfield('Serves', validators=[InputRequired()])
    recipe_preptime = StringField('Preperation',validators=[InputRequired()])
    recipe_cooktime = StringField('Cooking Time', validators=[InputRequired()])
    recipe_origin = StringField('Country of Origin', validators=[InputRequired()])

```
```html
{% extends 'base.html' %}
{% block content %}
<div class="container">
    <div class="add-recipe-container">
        <form method="POST" action="{{ url_for('update_recipe', recipe_id=recipe._id) }}">
            {{ form.csrf_token }}
            <h4 class="headers center">You can edit your recipe below</h4>
            <br>
            <ul class="add-recipe-form">
                <li class="add-recipe-li">
                    <div><h5 class="headers">Title</h5></div>
                    {{ form.recipe_title }}
                </li>
                <br>
                <li class="add-recipe-li"> 
                    <div><h5 class="headers">Ingredients</h5></div>
                    {{ form.recipe_ingredients }}    
                </li>
                <br>
                <li class="add-recipe-li">
                    <div><h5 class="headers">Description</h5></div>
                    {{ form.recipe_description }}
                </li>
                <br>
                <li class="add-recipe-li">
                    <div><h5 class="headers">Method</h5></div>
                    {{ form.recipe_method }}
                </li>
                <br>
                <li class="add-recipe-li">
                    <div><h5 class="headers">Meal Type</h5></div>
                    {{ form.recipe_meal_type }}
                </li>
                <br>
                <li class="add-recipe-li">
                    <div><h5 class="headers">Servings</h5></div>
                    {{ form.recipe_serves }}
                </li>
                <br>
                <li class="add-recipe-li">
                    <div><h5 class="headers">Preperation Time</h5></div>
                    {{ form.recipe_preptime }}
                </li>
                <br>
                <li class="add-recipe-li">
                    <div><h5 class="headers">Cooking Time</h5></div>
                    {{ form.recipe_cooktime }}
                </li>
                <br>
                <li class="add-recipe-li">
                    <div><h5 class="headers">Country of Origin</h5></div>
                    {{ form.recipe_origin }}
                </li>
                <br>
                
            </ul>
            <div class="container">
                <div class="row">
                    <div class="col s6">
                        <button type="submit" class="btn btn-primary btn-block green lighten-2 center">Submit</button>
                    </div>
                    <div class="col s6">
                        <button type="reset" class="btn btn-primary btn-block red lighten-2 center">Reset</button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>


{% endblock %}
```

#### Delete
The delete function is fairly simple. The button is also location on the read recipe page and will delete the users recipe
once they are logged in. 

```python
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    if 'username' in session:
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        user_recipes = mongo.db.recipes.find({"user_name": session['username']})
        if recipe in user_recipes:
            mongo.db.recipes.delete_one({'_id': ObjectId(recipe_id)})
            flash('Recipe Deleted')
            return redirect(url_for('get_recipe'))
        else:
            flash('You can only alter your own recipes')
            return render_template('sign_in_required.html')
    return render_template('sign_in_required.html')
```

#### Product
The product that I have worked into my project is the [Fat Secret](fatsecret.com) api. 

Fat secret is a primarily app based service that users can check their food against the Fat Secrey database
to see exactly how many calories a meal or item of food will contain. The site also offers services
for creating a profile and tracking eating habits over a long period of time to help with health a weightloss goals. 
Links to Fatsecret exist on the footer of everypage and within the Fatsecret page itself and is also mentioned within the index page of the site.

The API for Fat Secret simply needs to pasted into its own div on the page and it is self maintained from Fatsecrets end.




#### Features Left to Implement
Within this project there was a few features that I had really wanted to implement but due to time constraints I must
move on with the course. 

The feature that I wanted to implement the most was a search bar that would check the database for words that matched the query
in the database. I had tried this but [MongoDB](MongoDB.com) requires a text index to installed via Mongo Shell but unfortuantely I have been unable to get this done through gitpod.
I had also tried to use "Full Text Search" through MongoDB but implementing this returned Jinja errors that I was unable to get around
with the time I had left to play with. 

I will return to this and install it in a future version. 



### Technologies Used
#### Languages

* Python
* HTML
* javascript
* css

#### Frameworks
* Flask
* Materialize Css

#### Imports
* From Pymongo - MongoClient
* From Flask - render_template, redirect, request, url_for, session, flash
* From Flask-pymongo - PyMongo
* From Bson.objectid - ObjectId
* Bcrypt
* Datetime
* From WTforms - StringField, IntegerField, PasswordField, SubmitField, BooleanField, TextAreaField
* From WTforms.validators - InputRequired, URL, ValidationError
* From Flask_wtf import FlaskForm

### Testing
The UX was designed using materialize CSS provides an extremely response layout to the page. 
The page has been tested on all of the following devices and is displaying/functioning correctly. 

##### Large Viewports
* Lenovo Think Pad T490
* Macbook Pro
* IMac
* HP 250

##### Small Viewports
* Huawei Y30
* Samsung a70
* Samsung s7
* Iphone SE 
* Samsung s9 
* Samsung s5
* Pixel 2 / XL
* Iphone 6/7/8
* Iphone 6/7/8 Plus
* Iphone X
* Ipad Pro


Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as

Deployment
This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:

Different values for environment variables (Heroku Config Vars)?
Different configuration files?
Separate git branch?
In addition, if it is not obvious, you should also describe how to run your code locally.

Credits
Content
The text for section Y was copied from the Wikipedia article Z
Media
The photos used in this site were obtained from ...
Acknowledgements
I received inspiration for this project from X