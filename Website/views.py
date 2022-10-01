from flask import Blueprint, render_template, flash, request
from flask_login import  login_required, current_user
from . import db
from sqlalchemy.sql import func
from .models import Ticket, Entry, User

views = Blueprint('views', __name__)

#defineing the home page route and following pages
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user, tickets=Ticket.query.all())

@views.route('/ticket', defaults={'tkt' : 0}) 
@views.route('/ticket/<int:tkt>', methods=['GET', 'POST'])
@login_required
def ticket(tkt):
    if request.method == 'POST':
        ticketID = request.form.get('TicketID')
        short_description = request.form.get('short_description')
        customer_name = request.form.get('customer_name')
        customer_contact = request.form.get('customer_contact')
        status = request.form.get('status')
        note = request.form.get('note')
        
        #validation
        if len(customer_name) < 1:
            flash('Please enter a customer.', category='error')
        elif len(customer_contact) < 7:
            flash('Please enter a contact for the customer.', category='error')
        elif len(short_description) < 5:
            flash('Please enter a short desciption of the problem.', category='error')
        #elif status validation
        else:
            new_ticket = Ticket(short_description=short_description,customer_name=customer_name, customer_contact=customer_contact,status=status, creation_date=func.now())
            db.session.add(new_ticket)
            db.session.commit()
            flash('Ticket ' + str(new_ticket.id) + ' added', category='success')
        return render_template("home.html", user=current_user, tickets=Ticket.query.all())
    return render_template("ticket.html", user=current_user, tickets=Ticket.query.filter_by(id=tkt).first())

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template("admin.html", user=current_user, users=User.query.all())