from flask import Blueprint, render_template, flash, request
from flask_login import  login_required, current_user
from sqlalchemy import null
from . import db
from sqlalchemy.sql import func
from .models import Ticket, Entry, User

views = Blueprint('views', __name__)

#defineing the home page route and following pages
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user, tickets=Ticket.query.all())


#If this page is pulled from the home page, specifically identifying a ticket to open
#it will load that tickets information, which will allow editing. Otherwise this is 
#all associated to getting the information from the form to open a ticket.
#--todo--
#add note saving for display 
@views.route('/ticket', defaults={'tkt' : 0}, methods=['GET', 'POST']) 
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
        user=current_user
              
        #validation
        if len(customer_name) < 1:
            flash('Please enter a customer.', category='error')
        elif len(customer_contact) < 7:
            flash('Please enter a contact for the customer.', category='error')
        elif len(short_description) < 5:
            flash('Please enter a short desciption of the problem.', category='error')
        #if there is a valid ticket id in the entry, you are editing a ticket
        elif ticketID:
            tickets=Ticket.query.filter_by(id=ticketID).first()
            
            #If the ticket status is getting changd, only an admin can do it
            if tickets.status != int(status) and user.user_status == 2:
                tickets.short_description=short_description
                tickets.customer_name=customer_name
                tickets.customer_contact=customer_contact
                tickets.status=status
                if int(status) == 0:
                    tickets.close_date=func.now()
                else:
                    pass#tickets.close_date=null 
                db.session.commit() 
            elif tickets.status != int(status) and user.user_status != 2:
                flash('Only an admin can change the status of a ticket.', category='error')
            else:
                #If just changing normal info, anyone can do it
                tickets.short_description=short_description
                tickets.customer_name=customer_name
                tickets.customer_contact=customer_contact
                db.session.commit()           
        else:
            #Adding a ticket
            new_ticket = Ticket(short_description=short_description,customer_name=customer_name, customer_contact=customer_contact,status=status, creation_date=func.now())
            db.session.add(new_ticket)
            db.session.commit()
            flash('Ticket ' + str(new_ticket.id) + ' added', category='success')
        return render_template("home.html", user=current_user, tickets=Ticket.query.all())
    return render_template("ticket.html", user=current_user, tickets=Ticket.query.filter_by(id=tkt).first())

#just needs to pass all of the users so it can display each user on this page
@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template("admin.html", user=current_user, users=User.query.all())