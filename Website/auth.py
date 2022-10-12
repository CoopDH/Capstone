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
            if check_password_hash(user.password_hash, password) and user.user_status != 0:
                flash('Log in Successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            elif user.user_status == 0:
                flash('User account disabled. Please contact an admin', category='error')
            else:
                flash('Log in failed', category='error')
        else:
            #Not exactly best security practice but best for troubleshooting
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
        elif not check_password_hash(current_user.password_hash, adminpassword) or current_user.user_status != 2:
            flash('You are not able to make this user. Please check your password or account', category='error')
        else:
            new_user = User(username=username,fname=fname, lname=lname,user_status=ustatus, password_hash=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User ' + username + ' added', category='success')
            

    return render_template("adduser.html", user=current_user)

@auth.route('/userpage',  methods=['GET', 'POST'])
@login_required
def userpage():
    if request.method == 'POST':
        currentpwd = request.form.get('currentpwd')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if check_password_hash(current_user.password_hash, currentpwd):
            if password1 == password2:
                current_user.password_hash=generate_password_hash(password1, method='sha256')
                db.session.commit()
                flash('Password successfully changed.', category='success')
            else:
                flash('New passwords did not match', category='error')
        else:
            flash('Incorrect password', category='error')
            
    return render_template("userpage.html", user=current_user)

@auth.route('/chng', defaults={'usr' : 0}, methods=['GET', 'POST'])
@auth.route('/chng/<int:usr>', methods=['GET', 'POST'])
@login_required
def chng(usr):
    if request.method == "POST":
        tempuser = User.query.filter_by(id=usr).first()
        currentpwd = request.form.get('currentpwd')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        status = request.form.get("status")
        
        #confirms password and if user is authorized to make changes. Then conducts whatever change needs to be done
        if check_password_hash(current_user.password_hash, currentpwd) and current_user.user_status == 2:
            if len(password1) > 0:
                if password1 == password2:
                    tempuser.password_hash=generate_password_hash(password1, method='sha256')
                    flash('Password successfully changed.', category='success')
                else:
                    flash('New passwords did not match', category='error')
            if tempuser.user_status != int(status):
                tempuser.user_status=status
                flash('User status updated', category='success')
            db.session.commit()
        else:
            flash('Check password or account', category='error')
        
        
    return render_template("chng.html", user=current_user, usr=User.query.filter_by(id=usr).first())
