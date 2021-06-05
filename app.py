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


@app.route("/")
@app.route("/home")
def home():
    carousel_items = [
        {
            # old fashioned card
            "url": "recipe",
            "cocktail_id": "60a6b327ccda71deb2cd57fa",
            "image": "/static/images/old-fashioned.jpg"
        },
        {
            # login card
            "url": "login",
            "image": "/static/images/friends-join.png"
        },
        {
            # classic mojito card
            "url": "recipe",
            "cocktail_id": "60abc1d55afe387784d624c1",
            "image": "/static/images/classicmojito.png"
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
    spirits = mongo.db.spirits.find()
    recipes = list(mongo.db.recipes.find().sort("cocktail_name", 1))
    paginated_recipes = paginate(recipes)
    pagination = pagination_args(recipes)
    return render_template(
        'cocktail_list.html', spirits=spirits, recipes=paginated_recipes,
        pagination=pagination)


@app.route("/search", methods=["GET", "POST"])
def search():
    spirits = mongo.db.spirits.find()
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    paginated_recipes = paginate(recipes)
    pagination = pagination_args(recipes)
    return render_template("cocktail_list.html", spirits=spirits,
                           recipes=paginated_recipes,
                           pagination=pagination)


@app.route("/search/<spirit>")
def search_spirit(spirit):
    spirits = mongo.db.spirits.find()
    recipes = list(mongo.db.recipes.find(
        {"category": spirit}).sort("cocktail_name", 1))
    paginated_recipes = paginate(recipes)
    pagination = pagination_args(recipes)
    return render_template('cocktail_list.html',
                           spirits=spirits, recipes=paginated_recipes,
                           pagination=pagination)


@app.route("/login", methods=['GET', 'POST'])
def login():
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
                    "mycocktails", username=session["user"]))

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
    flash("Please log in to use this function")
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already in use!")
            return redirect(url_for("login"))

        # check if passwords match
        if request.form.get("password") != request.form.get(
                    "confirm-password"):
            flash("Passwords do not match!")
            return redirect(url_for("login"))

        # register user
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get(
                "password"))
        }
        mongo.db.users.insert_one(register)
        flash("Successfully Registered!")

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()

        # change to my recipes once built <----------------------
        return redirect(url_for("mycocktails", username=session["user"]))

    return render_template("login.html")


@app.route('/logout')
def logout():
    # remove user from session cookie
    flash('You have been logged out')
    session.pop('user')
    return redirect(url_for("login"))


@app.route('/mycocktails/<username>', methods=['GET', 'POST'])
def mycocktails(username):
    my_recipes = mongo.db.recipes.find()
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    paginated_recipes = paginate(my_recipes)
    pagination = pagination_args(my_recipes)
    if session['user']:
        return render_template(
            "mycocktails.html", username=username,
            my_recipes=paginated_recipes, pagination=pagination)


@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
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
        return redirect(url_for("mycocktails", username=username))

    return render_template('create_recipe.html')


@app.route('/edit_recipe/<cocktail_id>', methods=["GET", "POST"])
def edit_recipe(cocktail_id):
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
        return redirect(url_for('mycocktails', username=username))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(cocktail_id)})
    return render_template('edit_recipe.html', recipe=recipe)


@app.route("/delete_recipe/<cocktail_id>")
def delete_recipe(cocktail_id):
    mongo.db.recipes.remove({"_id": ObjectId(cocktail_id)})
    flash("Recipe Has Been Removed!")
    username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    return redirect(url_for('mycocktails', username=username))


@app.route("/recipe/<cocktail_id>")
def recipe(cocktail_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(cocktail_id)})
    reviews = list(mongo.db.reviews.find({
        "cocktail_id": ObjectId(cocktail_id)
    }))
    return render_template("recipe.html", recipe=recipe, reviews=reviews)


@app.route("/review/<cocktail_id>", methods=["GET", "POST"])
def review(cocktail_id):
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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
