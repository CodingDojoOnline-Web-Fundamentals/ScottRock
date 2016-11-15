import re
from flask import Flask, render_template, redirect, request, session, flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+[a-zA-Z]*$')
NAME_REGEX = re.compile(r'[a-zA-Z]*\d[a-zA-Z]*')
PWD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$')

app = Flask(__name__)
app.secret_key = "kjasclkiaesrjxfiurn"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods = ['POST'])
def add_user():
    # validate the form and give good message
    errors = []
    # check to make sure an email was entered and that it was valid
    if len(request.form['email']) < 1:
        # no email entered
        errors.append(("Email is a required field, it can't be empty", "email_error"))
    elif not EMAIL_REGEX.match(request.form['email']):
        # invalid email
        errors.append(("Invalid email address!", "email_error"))

    if len(request.form['first_name']) < 1:
        # no first entered
        errors.append(("First Name is a required field, it can't be empty", "fname_error"))
    elif NAME_REGEX.match(request.form['first_name']):
        # first name had a character other than a letter in it
        errors.append(("First name can not contain numbers", "fname_error"))
    # else:
    #     print NAME_REGEX.match(request.form['first_name'])

    if len(request.form['last_name']) < 1:
        # no last name entered
        errors.append(("Last Name is a required field, it can't be empty", "lname_error"))
    elif NAME_REGEX.match(request.form['last_name']):
        # last name had a character other than a letter in it
        errors.append(("Last name can not contain numbers", "lname_error"))

    # record all password errors on the first password
    if len(request.form['password1']) < 1:
        # no password entered
        errors.append(("Password is a required field, it can't be empty", "pwd_error"))
    elif not PWD_REGEX.match(request.form['password1']):
        # invalid password - must be at least 8 characters long
        # want to edit regex to add more validation
        errors.append(("Password must be at least 8 characters long and contain an upppercase letter and a number", "pwd_error"))
    elif request.form['password1'] != request.form['password2']:
        # passwords don't match
        errors.append(("Password confirmation does not match password", "pwd_error"))


    if errors:
        for message, category in errors:
            flash(message, category)
    else:
        flash("Thanks for submitting your information", "success")

    return redirect('/')

app.run(debug=True)
