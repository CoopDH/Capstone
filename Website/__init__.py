from flask import Flask

#initializing flask and establishing a cookie functionality
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "SuperSecretKey"
    
    return app