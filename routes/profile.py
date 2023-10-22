"""
Displays profile and handles deletion
"""

from flask import render_template, redirect, request, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash
from app import app
from db import db
def is_authenticated():
    """
    Helper function, checks for authentication
    """
    return 'username' in session

@app.route("/profile")
def profile():
    """
    This is the user profile, displays
    information on username, when joined
    and also gives the option of deleteing
    their account and logging out of course.
    """
    if not is_authenticated():
        return redirect("/")

    username = session["username"]

    # Fetch the user's join date
    user = db.session.execute(
        text("SELECT created_at FROM users WHERE username=:username"),
        {"username": username}
    ).fetchone()

    # Format the join, looks nicer.
    user_joined_date = user.created_at.strftime("%B %d, %Y")

    return render_template("profile.html", username=username, user_joined_date=user_joined_date)

@app.route("/confirm_delete", methods=["GET"])
def confirm_delete():
    """
    Just rendering the "confirm_delete.html" template
    """
    if not is_authenticated():
        return redirect("/")

    return render_template("confirm_delete.html")

@app.route("/delete_account", methods=["POST"])
def delete_account():
    """
    Used in the process of deleting a user account
    and handling the deletion confirmation form's submission.
    """
    if not is_authenticated():
        return redirect("/")

    # Validate the user's credentials
    username = session.get("username")
    password = request.form.get("password")

    user = db.session.execute(
        text("SELECT * FROM users WHERE username=:username"),
        {"username": username}
    ).fetchone()

    if user and check_password_hash(user.password, password):
        #Deleting kind of:
        db.session.execute(
            text("UPDATE users SET deleted = TRUE WHERE username = :username"),
            {"username": username}
        )
        db.session.commit()

        # Log the user out
        del session["username"]

        # Redirect to a confirmation page
        return redirect("/deleted_confirmation")

    error_message = "Incorrect password. Please try again."
    return render_template("confirm_delete.html", error_message=error_message)
