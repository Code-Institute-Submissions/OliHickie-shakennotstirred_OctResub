import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os. path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Pagination
"""
Code taken from
 https://betterprogramming.pub/simple-flask-pagination-example-4190b12c2e2e and
 https://github.com/alandoherty95/reciprocate-app
"""
PER_PAGE = 12
SPIRITS = ["vodka", "gin", "whiskey", "rum", "tequila"]


def paginate(recipes):
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    offset = page * PER_PAGE - PER_PAGE

    return recipes[offset: offset + PER_PAGE]


def pagination_args(recipes):
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    total = len(recipes)

    return Pagination(page=page, per_page=PER_PAGE, total=total)


# Routes

@app.route("/")
@app.route("/home")
def home():
    """
    Displays carousel of items
    Displays four seasonal recips
    Picks a random file on each apge load
    Returns number of recipes in database
    """
    carousel_items = [
        {
            # old fashioned card
            "url": "recipe",
            "cocktail_id": "60a6b327ccda71deb2cd57fa",
            "image": "/static/images/old-fashioned.jpg",
            "alt": "Old fashioned recipe"
        },
        {
            # login card
            "url": "login",
            "image": "/static/images/friends-join.png",
            "alt": "link to login"
        },
        {
            # classic mojito card
            "url": "recipe",
            "cocktail_id": "60abc1d55afe387784d624c1",
            "image": "/static/images/classicmojito.png",
            "alt": "mojito recipe"
        }
    ]
    seasonal_recipes = [
        {
            "cocktail_id": "60abd6b85afe387784d624c2",
            "image": "/static/images/spring.png",
            "alt": "img of southside cocktail"
        },
        {
            "cocktail_id": "60ab7d8dc47a342be1648ccc",
            "image": "/static/images/margarita.png",
            "alt": "img of margarita cocktail"
        },
        {
            "cocktail_id": "60abd77b5afe387784d624c3",
            "image": "/static/images/autumn.png",
            "alt": "img of manhattan cocktail"
        },
        {
            "cocktail_id": "60a6b605ccda71deb2cd57fc",
            "image": "/static/images/winter.png",
            "alt": "img of hot toddy cocktail"
        }
    ]

    random_file = mongo.db.recipes.aggregate([{"$sample": {"size": 1}}])
    number_of_recipes = mongo.db.recipes.count()
    return render_template('home.html', number_of_recipes=number_of_recipes,
                           carousel_items=carousel_items,
                           random_file=random_file,
                           seasonal_recipes=seasonal_recipes)


@app.route("/cocktail_list")
def cocktail_list():
    """
    Returns all recipes as a list and sorts alphabetically
    Paginates recipes - 12 per page
    """
    recipes = list(mongo.db.recipes.find().sort("cocktail_name", 1))

    # Pagination
    paginated_recipes = paginate(recipes)
    pagination = pagination_args(recipes)
    return render_template(
        'cocktail_list.html', spirits=SPIRITS, recipes=paginated_recipes,
        pagination=pagination)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    returns list of spirits
    Searches recipes and returns them as a list
    Paginates search results
    """
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    paginated_recipes = paginate(recipes)
    pagination = pagination_args(recipes)
    return render_template("cocktail_list.html", spirits=SPIRITS,
                           recipes=paginated_recipes,
                           pagination=pagination)


@app.route("/search/<spirit>")
def search_spirit(spirit):
    """
    Returns recipes depending on spirit category
    Paginates search results
    """
    recipes = list(mongo.db.recipes.find(
        {"category": spirit}).sort("cocktail_name", 1))
    paginated_recipes = paginate(recipes)
    pagination = pagination_args(recipes)
    return render_template('cocktail_list.html',
                           spirits=SPIRITS, recipes=paginated_recipes,
                           pagination=pagination)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Allows user to login to profile.
    Checks whether user exists and that passwords match
    password stored.
    Upon successful log in, user redirected to user profile page.
    """
    if request.method == "POST":
        # check if user exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # check password matches stored password
            if check_password_hash(existing_user["password"], request.form.get(
                    "password")):
                session["user"] = request.form.get("username").lower()

                return redirect(url_for(
                    "myrecipes", username=session["user"]))

            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/redirect_login")
def redirect_login():
    """
    If user not logged in, redirects user to log in page
    and asks user to log in.
    """
    flash("Please log in to use this function")
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Allows user to register their username and passoword.
    Checks for existing user with matching username.
    Checks passwords match.
    Puts user into session.
    """
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("register-username").lower()})

        if existing_user:
            flash("Username already in use!")
            return redirect(url_for("login"))

        # check if passwords match
        if request.form.get("register-password") != request.form.get(
                    "register-confirm-password"):
            flash("Passwords do not match!")
            return redirect(url_for("login"))

        # register user
        register = {
            "username": request.form.get("register-username").lower(),
            "password": generate_password_hash(request.form.get(
                "register-password"))
        }
        mongo.db.users.insert_one(register)
        flash("Successfully Registered!")

        # put the new user into 'session' cookie
        session["user"] = request.form.get("register-username").lower()
        return redirect(url_for("myrecipes", username=session["user"]))

    return render_template("login.html")


@app.route('/logout')
def logout():
    """
    Logs user out.
    """
    flash('You have been logged out')
    session.pop('user')
    return redirect(url_for("login"))


@app.route('/myrecipes/<username>', methods=['GET', 'POST'])
def myrecipes(username):
    """
    Returns users cocktails
    """
    my_recipes = mongo.db.recipes.find()
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session['user']:
        return render_template(
            "myrecipes.html", username=username,
            my_recipes=my_recipes)


@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    """
    Allows user to create recipe.
    Stores recipe in database and returns user to profil page.
    """
    if request.method == "POST":
        # add recipe
        new_recipe = {
            "cocktail_name": request.form.get("cocktail_name").lower(),
            "difficulty": request.form.get("difficulty"),
            "category": request.form.get("category"),
            "ingredients": request.form.getlist("ingredients"),
            "method": request.form.get("method"),
            "image_url": request.form.get("image_url"),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(new_recipe)
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        flash("Successfully Added Recipe")
        return redirect(url_for("myrecipes", username=username))

    return render_template('create_recipe.html')


@app.route('/edit_recipe/<cocktail_id>', methods=["GET", "POST"])
def edit_recipe(cocktail_id):
    """
    Allows user to edit and update their own recipe.
    """
    if request.method == "POST":
        edit_recipe = {
            "cocktail_name": request.form.get("cocktail_name").lower(),
            "difficulty": request.form.get("difficulty"),
            "category": request.form.get("category"),
            "ingredients": request.form.getlist("ingredients"),
            "method": request.form.get("method"),
            "image_url": request.form.get("image_url"),
            "created_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(cocktail_id)}, edit_recipe)
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        flash('Recipe has been Updated')
        return redirect(url_for('myrecipes', username=username))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(cocktail_id)})
    return render_template('edit_recipe.html', recipe=recipe)


@app.route("/delete_recipe/<cocktail_id>")
def delete_recipe(cocktail_id):
    """
    Removes recipe from database.
    """
    mongo.db.recipes.remove({"_id": ObjectId(cocktail_id)})
    flash("Recipe Has Been Removed!")
    username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    return redirect(url_for('myrecipes', username=username))


@app.route("/recipe/<cocktail_id>")
def recipe(cocktail_id):
    """
    Returns recipe information.
    Returns user reviews that relate to that recipe.
    Find average rating for recipe
    """
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(cocktail_id)})
    reviews = list(mongo.db.reviews.find({
        "cocktail_id": ObjectId(cocktail_id)
    }))

    # find average rating
    ratings = list(mongo.db.reviews.find(
        {"cocktail_id": ObjectId(cocktail_id)}, {"rating": 1, "_id": 0}))
    numbers = [num['rating'] for num in ratings]
    try:
        average_rating = round(sum(numbers)/len(numbers), 1)

    except ZeroDivisionError:
        average_rating = "No Ratings"

    return render_template("recipe.html", recipe=recipe, reviews=reviews,
                           average_rating=average_rating)


@app.route("/review/<cocktail_id>", methods=["GET", "POST"])
def review(cocktail_id):
    """
    Allows users to review recipes.
    Add a rating and a comment and stores in database.
    """
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(cocktail_id)})
    if request.method == "POST":
        new_review = {
            "cocktail_id": ObjectId(cocktail_id),
            "comment": request.form.get("comment"),
            "rating": int(request.form.get("rating")),
            "user": session["user"]
        }
        mongo.db.reviews.insert_one(new_review)
        reviews = mongo.db.reviews.find()
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        flash('Review Successfully Added')
        return redirect(url_for('recipe', username=username,
                                recipe=recipe, reviews=reviews,
                                cocktail_id=cocktail_id))

    return render_template("review.html", recipe=recipe)


# ERRORS
"""
404 and 500 error pages
"""


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
