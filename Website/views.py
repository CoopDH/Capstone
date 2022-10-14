from flask import Blueprint, render_template, flash, request
from flask_login import  login_required, current_user
from sqlalchemy import or_
from . import db
from sqlalchemy.sql import func
from .models import Ticket, Entry, User

views = Blueprint('views', __name__)

#defineing the home page route and following pages
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        ticketID = request.form.get('TicketID')
        start_date = request.form.get('start_date')
        end_date = request.form.get("end_date")
        status = request.form.get('status')
        query_filter = []
                
                
        #The query filter variable is a means to add specific variables that are needed
        #If a query section is filled, it will append the key search function to the 
        #query filter variable to then be ran        
        if ticketID:
            if "-" in ticketID:
                ticketLeft = ticketID.split("-")[0]
                ticketRight = ticketID.split("-")[1]
                query_filter.append(Ticket.id >= ticketLeft)
                query_filter.append(Ticket.id <= ticketRight)
            else:
                query_filter.append(Ticket.id == ticketID)
                       
        if int(status) != 2:
            query_filter.append(Ticket.status == status)
        
        if end_date:
            query_filter.append(Ticket.creation_date <= end_date)
        
        if start_date:
            query_filter.append(or_(Ticket.close_date >= start_date, Ticket.status == 1))
           
        tickets=Ticket.query.filter(*query_filter) 
     

                
        return render_template("home.html", user=current_user, tickets=tickets)


        
    return render_template("home.html", user=current_user, tickets=Ticket.query.filter(Ticket.status == 1))


#If this page is pulled from the home page, specifically identifying a ticket to open
#it will load that tickets information, which will allow editing. Otherwise this is 
#all associated to getting the information from the form to open a ticket.
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
            if tickets.short_description != short_description or tickets.customer_name != customer_name or tickets.customer_contact != customer_contact:
                if tickets.status == 1:
                    tickets.short_description=short_description
                    tickets.customer_name=customer_name
                    tickets.customer_contact=customer_contact
                    db.session.commit()
                else:
                    flash('You can not edit a closed ticket.', category='error')
            #If the ticket status is getting changd, only an admin can do it
            if tickets.status != int(status) and user.user_status == 2:
                if int(status) == 0:
                    tickets.status=status
                    tickets.close_date=func.now()
                    db.session.commit()
                else:
                    flash('You can not open a closed ticket.', category='error')
            elif tickets.status != int(status) and user.user_status != 2:
                flash('Only an admin can change the status of a ticket.', category='error')
                    
        else:
            #Adding a ticket
            #Checking status ensures that creating a ticket that is closed, does not break the home page trying to display it.
            if int(status) == 1:
                new_ticket = Ticket(short_description=short_description,customer_name=customer_name, customer_contact=customer_contact,status=status, creation_date=func.now())
            else:
                new_ticket = Ticket(short_description=short_description,customer_name=customer_name, customer_contact=customer_contact,status=status, creation_date=func.now(), close_date=func.now())
            db.session.add(new_ticket)
            db.session.commit()
            flash('Ticket ' + str(new_ticket.id) + ' added', category='success')
            
        #adding the a note to either the new ticket or current ticket    
        if len(note) > 1 and tickets.status == 1:
            if ticketID:
                new_entry = Entry(note=note, ticket_id=tickets.id, user_id=current_user.id)
            else:
                new_entry = Entry(note=note, ticket_id=new_ticket.id, user_id=current_user.id)
            db.session.add(new_entry)
            db.session.commit()
            flash('Entry added', category='success')
        elif len(note) > 1 and tickets.status == 0:
            flash('You can not create entries on a closed ticket.', category='error')
            
        return render_template("ticket.html", user=current_user, tickets=Ticket.query.filter_by(id=tkt).first())
    return render_template("ticket.html", user=current_user, tickets=Ticket.query.filter_by(id=tkt).first())



#just needs to pass all of the users so it can display each user on this page
@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == "POST":
        userid = request.form.get('UserID')
        user_status = request.form.get('user_status')
        fname = request.form.get("fname")
        lname = request.form.get('lname')
        query_filter = []
                
        #The query filter variable is a means to add specific variables that are needed
        #If a query section is filled, it will append the key search function to the 
        #query filter variable to then be ran          
                
        if userid:
            if "-" in userid:
                IDLeft = userid.split("-")[0]
                IDRight = userid.split("-")[1]
                query_filter.append(User.id >= IDLeft)
                query_filter.append(User.id <= IDRight)
            else:
                query_filter.append(User.id == userid)
         
        if int(user_status) == 3:
            query_filter.append(User.user_status != 0)
        elif int(user_status) < 3:
            query_filter.append(User.user_status == user_status)
        
        if fname:
            query_filter.append(User.fname.like(fname))
        
        if lname:
            query_filter.append(User.lname.like(lname))
           
        users=User.query.filter(*query_filter) 
                
        return render_template("admin.html", user=current_user, users=users)
    
    
    return render_template("admin.html", user=current_user, users=User.query.filter(User.user_status != 0))