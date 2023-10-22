"""
Handles all confirmation pages
"""
from flask import render_template, redirect, session
from app import app
@app.route("/successful_logout")
def successful_logout():
    """
    Rendering the confirmation message.
    """
    return render_template("successful_logout.html")


@app.route("/logout")
def logout():
    """
    User logout powerhorse.
    """
    del session["username"]
    return redirect("/successful_logout")



@app.route("/deleted_confirmation")
def deleted_confirmation():
    """
    Rendering the "deleted_confirmation.html" template
    """
    return render_template("deleted_confirmation.html")
