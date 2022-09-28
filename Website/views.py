from flask import Blueprint

views = Blueprint('views', __name__)

#defineing the home page route and following pages
@views.route('/')
def home():
    return "<h1>Test</h1>"