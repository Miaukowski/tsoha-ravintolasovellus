"""
Handles the front page, login and registering.
"""

import secrets
from datetime import datetime
from flask import render_template, redirect, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


from app import app
from db import db


# Define username and password requirements
USERNAME_MIN_LENGTH = 5
USERNAME_MAX_LENGTH = 20
USERNAME_ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
PASSWORD_MIN_LENGTH = 8
PASSWORD_COMPLEXITY = {"uppercase": 1, "lowercase": 1, "digit": 1, "special": 1}


# Function to check password complexity
def meets_complexity_requirements(password):
    """
    Helper function for checking if password is complex enough.
    """
    complexity_met = [
        sum(1 for char in password if char.isupper()) >= PASSWORD_COMPLEXITY['uppercase'],
        sum(1 for char in password if char.islower()) >= PASSWORD_COMPLEXITY['lowercase'],
        sum(1 for char in password if char.isdigit()) >= PASSWORD_COMPLEXITY['digit'],
        sum(1 for char in password if not char.isalnum()) >= PASSWORD_COMPLEXITY['special']
    ]
    return all(complexity_met)

@app.route("/")
def front():
    """
    The front page for non loggged users.
    If user already logged in, they are
    redirected to the dashboard.
    """
    if "username" in session:
        return redirect("/dashboard")
    restaurants = db.session.execute(
        text("SELECT r.id, r.name, AVG(re.rating) as average_rating "
             "FROM restaurants r "
             "LEFT JOIN reviews re ON r.id = re.restaurant_id "
             "GROUP BY r.id, r.name "
             "ORDER BY average_rating DESC "
             "LIMIT 5")
    ).fetchall()
    return render_template("front_page.html", restaurants=restaurants)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    The login page, also check here if account is deleted(deleted=TRUE)
    """
    error_message = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check username and password against the database, also if the
        # credentials have been deleted previously, so Deleted = True in that case
        # Else they are free to log in.

        if not username or not password:
            error_message= "Both username and password are required."
        else:
            user = db.session.execute(
                text("SELECT * FROM users WHERE username=:username AND deleted = FALSE"),
                {"username": username}
            ).fetchone()
            if user:
                if check_password_hash(user.password, password):
                    csrf_token = secrets.token_hex(16)
                    session["csrf_token"] = csrf_token
                    # Login successful -> store the username in the session
                    # Redirect to dashboard
                    session["username"] = username
                    return redirect("/dashboard")
                else:
                    error_message = "Invalid username or password. Please try again."
            else:
                error_message = "Invalid username or password. Please try again."

    #fetching the actual login and error message in case of fault
    return render_template("login.html", error_message=error_message)


@app.route("/register", methods=["GET", "POST"])
def register():
    error_message = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not (USERNAME_MIN_LENGTH <= len(username) <= USERNAME_MAX_LENGTH):
            error_message = f"Username must be between {USERNAME_MIN_LENGTH} and {USERNAME_MAX_LENGTH} characters."
        elif not all(char in USERNAME_ALLOWED_CHARACTERS for char in username):
            error_message = "Username contains invalid characters."
        elif not (PASSWORD_MIN_LENGTH <= len(password)):
            error_message = f"Password must be at least {PASSWORD_MIN_LENGTH} characters long."
        elif not meets_complexity_requirements(password):
            error_message = "Password must meet complexity requirements."

        if error_message:
            return render_template("register.html", error_message=error_message)

        # Check if the username already exists in the database
        existing_user = db.session.execute(
            text("SELECT id FROM users WHERE username=:username"),
            {"username": username}
        ).fetchone()

        if existing_user:
            error_message = "Username already exists. Please choose a different one."
        else:
            hash_value = generate_password_hash(password)
            created_at = datetime.now()

            # Insert the new user into the database
            sql = text("INSERT INTO users (username, password, created_at) VALUES (:username, :password, :created_at)")
            db.session.execute(sql, {"username": username, "password": hash_value, "created_at": created_at})
            db.session.commit()

            # Redirect to the login page if registration is successful
            return redirect("/login")

    return render_template("register.html", error_message=error_message)


