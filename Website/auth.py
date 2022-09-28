from unicodedata import category
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/adduser', methods=['GET', 'POST'])
def adduser():
    #injests from the form being filled out
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_status = request.form.get('user_status') #will return 'on' if enabled
        adminpassword = request.form.get('adminpassword')

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
            flash('User added.', category='success')
            #create username
            #add user to database


    return render_template("adduser.html")