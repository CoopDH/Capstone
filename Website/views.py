from flask import Blueprint, render_template

views = Blueprint('views', __name__)

#defineing the home page route and following pages
@views.route('/')
def home():
    return render_template("home.html")