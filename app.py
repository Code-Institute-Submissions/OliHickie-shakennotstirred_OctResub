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
            return redirect(url_for("register"))

        if request.form.get("password") != request.form.get(
                    "confirm-password"):
            flash("Passwords do not match!")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get(
                "password"))
        }
        mongo.db.users.insert_one(register)
        flash("Successfully Registered!")

        # change to my recipes once built <----------------------
        return render_template("login.html")

    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
