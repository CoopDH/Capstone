from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


#This establishes the 3 database tables we need for user tracking and ticket management
#User contains all user information
#Ticket contains the metadata of the tickets
#Entry contains all of the notes that will be placed in the ticket and references who placed the entry  

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    note = db.Column(db.String(100))
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True) #automatically generated to f.lname
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    user_status = db.Column(db.Integer) #0 is deactivated, 1 is user, 2 is admin
    password_hash = db.Column(db.String(150))
    user_entries = db.relationship('Entry')

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_description = db.Column(db.String(200))
    customer_name = db.Column(db.String(200))
    customer_contact = db.Column(db.String(200))
    status = db.Column(db.Integer) #0 is closed, 1 is open
    creation_date = db.Column(db.DateTime(timezone=True), default=func.now())
    close_date = db.Column(db.DateTime(timezone=True))
    ticket_entries = db.relationship('Entry')
