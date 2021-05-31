import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os. path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


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
    random_file = mongo.db.recipes.aggregate([{"$sample": {"size": 5}}])
    number_of_recipes = mongo.db.recipes.count()
    return render_template('home.html', number_of_recipes=number_of_recipes,
                           carousel_items=carousel_items,
                           random_file=random_file)


@app.route("/cocktail_list")
def cocktail_list():
    spirits = mongo.db.spirits.find()
    recipes = mongo.db.recipes.find().sort("cocktail_name", 1)
    return render_template(
        'cocktail_list.html', spirits=spirits, recipes=recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    spirits = mongo.db.spirits.find()
    query = request.form.get("query")
    recipes = mongo.db.recipes.find({"$text": {"$search": query}})
    return render_template("cocktail_list.html", spirits=spirits,
                           recipes=recipes)


@app.route("/search/<spirit>")
def search_spirit(spirit):
    spirits = mongo.db.spirits.find()
    recipes = mongo.db.recipes.find({"category": spirit})
    return render_template('cocktail_list.html',
                           spirits=spirits, recipes=recipes)


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
    if session['user']:
        return render_template(
            "mycocktails.html", username=username, my_recipes=my_recipes)


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


@app.route("/recipe/<cocktail_id>", methods=["GET", "POST"])
def recipe(cocktail_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(cocktail_id)})
    if request.method == "POST":
        new_review = {
            "cocktail_id": cocktail_id,
            "comment": request.form.get("comment"),
            "rating": request.form.get("rating"),
            "user": session["user"]
        }
        mongo.db.user_comments.insert_one(new_review)
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        return render_template("recipe.html", recipe=recipe,
                               username=username)

    return render_template("recipe.html", recipe=recipe)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
