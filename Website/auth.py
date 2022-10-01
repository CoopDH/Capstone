from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        #takes username and password, confirms a user that matches the database exists, then checks passwords
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password_hash, password):
                flash('Log in Successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Log in failed', category='error')
        else:
            flash('User doesnt exist', category='error')
        
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    #injests from the form being filled out
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_status = request.form.get('user_status') #will return 'on' if enabled
        adminpassword = request.form.get('adminpassword')
        username = fname[0] + '.' + lname
        
        #determining elevated user status. If enabled, status will be 2. Normal user will be status 1. deactivated users will be status 0.
        if user_status == 'on':
            ustatus = 2
        else:
            ustatus = 1

        
        #confirming if the username already exists. Initialization conducts the search. If true, loops through a temp name with a number at the end.
        #if the temp username does not exist, it establishes the new username and estblishes the flag to get out
        user = User.query.filter_by(username=username).first()
        i=1
        while user:
            tempusername= username + str(i)
            tempuser = User.query.filter_by(username=tempusername).first()
            if not tempuser:
                username = username + str(i)
                user = User.query.filter_by(username=username).first()
            i=i+1
        
        #Entry validation
        if len(fname) < 2:
            flash('First name needs to be larger than 1 character.', category='error')
        elif len(lname) < 2:
            flash('Last name needs to be larger than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords need to match.', category='error')
        elif len(password1) < 7:
            flash('Password needs to be 7 characters or longer.', category='error')
        #elif adminpassword != current user password
        else:
            
            new_user = User(username=username,fname=fname, lname=lname,user_status=ustatus, password_hash=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User ' + username + ' added', category='success')
            

    return render_template("adduser.html", user=current_user)

@auth.route('/userpage')
@login_required
def userpage():
    return render_template("userpage.html", user=current_user)

@auth.route('/chng', defaults={'usr' : 0})
@auth.route('/chng/<int:usr>')
@login_required
def chng(usr):
    return render_template("chng.html", user=current_user, usr=User.query.filter_by(id=usr).first())
