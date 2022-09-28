from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/')
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/adduser')
def adduser():
    return "<p>add user</p>"