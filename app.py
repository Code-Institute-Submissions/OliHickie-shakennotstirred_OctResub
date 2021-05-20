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
@app.route("/recipes")
def recipes():
    spirits = mongo.db.spirits.find()
    return render_template('recipes.html', spirits=spirits)


@app.route("/login", methods=['GET', 'POST'])
def login():
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
        return redirect(url_for("recipes", username=session["user"]))

    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("login.html")


@app.route('/logout')
def logout():
    # remove user from session cookie
    flash('You have been logged out')
    session.pop('user')
    return redirect(url_for("login"))


@app.route('/mycocktails/<username>', methods=['GET', 'POST'])
def mycocktails(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session['user']:
        return render_template("mycocktails.html", username=username)


@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    if request.method == "POST":
        # add recipe
        new_recipe = {
            "cocktail_name": request.form.get("cocktail_name").lower(),
            "difficulty": request.form.get("difficulty"),
            "ingredients": request.form.getlist("ingredients"),
            "method": request.form.get("method").lower()
        }
        mongo.db.recipes.insert_one(new_recipe)
        flash("Successfully Added Recipe")
        return redirect(url_for("create_recipe"))

    return render_template('create_recipe.html')


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
