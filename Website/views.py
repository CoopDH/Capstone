from flask import Blueprint, render_template

views = Blueprint('views', __name__)

#defineing the home page route and following pages
@views.route('/')
def home():
    return render_template("home.html")

@views.route('/ticket')
def ticket():
    return render_template("ticket.html")

@views.route('/admin')
def admin():
    return render_template("admin.html")