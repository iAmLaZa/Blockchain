#pip install flask
#pip install flask_mysqldb
#pip install passlib
#pip install wtforms


# 1st -----> create DATABASE crypto 

#import flask dependencies for web GUI
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps

#import other functions and classes
from sqlhelpers import *
from forms import *

#other dependencies
import time

#initialize the app
app = Flask(__name__)

#configure mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0000'
app.config['MYSQL_DB'] = 'crypto'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initialize mysql
mysql = MySQL(app)

#wrap to define if the user is currently logged in from session
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, please login.", "danger")
            return redirect(url_for('login'))
    return wrap

#log in the user by updating session
def log_in_user(username):
    users = Table("users", "name", "email", "username", "password","type")
    user = users.getone("username", username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')
    session['type'] = user.get('type')

#Registration page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("users", "name", "email", "username", "password","type")

    #if form is submitted
    if request.method == 'POST' and form.validate():
        #collect form data
        username = form.username.data
        email = form.email.data
        name = form.name.data
        type='simple'

        #make sure user does not already exist
        if isnewuser(username):
            #add the user to mysql and log them in
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(name,email,username,password,type)
            log_in_user(username)
            return redirect(url_for('dashboard'))
        else:
            flash('User already exists', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

#Login page
@app.route("/login", methods = ['GET', 'POST'])
def login():
    #if form is submitted
    if request.method == 'POST':
        #collect form data
        username = request.form['username']
        candidate = request.form['password']

        #access users table to get the user's actual password
        users = Table("users", "name", "email", "username", "password","type")
        user = users.getone("username", username)
        accPass = user.get('password')

        #if the password cannot be found, the user does not exist
        if accPass is None:
            flash("Username is not found", 'danger')
            return redirect(url_for('login'))
        else:
            #verify that the password entered matches the actual password
            if sha256_crypt.verify(candidate, accPass) :
                #log in the user and redirect to Dashboard page
                log_in_user(username)
                flash('You are now logged in.', 'success')
                return redirect(url_for('dashboard'))
            else:
                #if the passwords do not match
                flash("Invalid password", 'danger')
                return redirect(url_for('login'))

    return render_template('login.html')

#Verification page
@app.route("/Verification", methods = ['GET', 'POST'])
@is_logged_in
def Verification():
    form = VerificationForm(request.form)
    
     
    #balance = get_balance(session.get('username'))

    #if form is submitted
    if request.method == 'POST':
        try:
            #attempt to execute the Verification
            if (diplome_Verification(form.diplome.data)):
                flash("Diplome valide!", "success")
            else:
                flash("Diplome Non valide!", "danger")
        except Exception as e:
                flash(str(e), 'danger')

        return redirect(url_for('Verification'))
   

    return render_template('Verification.html', form=form, page='Verification')

#create and add diplome page
@app.route("/creatediplome", methods = ['GET', 'POST'])
@is_logged_in
def creatediplome():
    form = CreatediplomeForm(request.form)
    

    if request.method == 'POST':
        
        try:
            add_diplome("USTHB", form.matricule.data,form.mention.data)
            flash("ADD Successfully!", "success")
        except Exception as e:
            flash(str(e), 'danger')

        return redirect(url_for('dashboard'))

    return render_template('creatediplome.html', form=form, page='creatediplome')


#Addstudent page
@app.route("/addstudent", methods = ['GET', 'POST'])
@is_logged_in
def addstudent():
    
    form = AddstudentForm(request.form)
    students = Table("students", "familyname", "lastname","matricule","email","date","place","major")
    #if form is submitted
    if request.method == 'POST' :
        #collect form data
        familyname = form.familyname.data
        lastname= form.lastname.data
        matricule =form.matricule.data
        email = form.email.data
        date = form.date.data
        place= form.place.data
        major = form.major.data

        #make sure student does not already exist
        if isnewstudent(matricule):
            
            #add the student to mysql 
            students.insert(familyname,lastname,matricule,email,date,place,major)
            return redirect(url_for('addstudent'))
        else:
            
            flash('Student already exists', 'danger')
            return redirect(url_for('addstudent'))

    return render_template('addstudent.html', form=form)

#logout the user. Ends current session
@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("Logout success", "success")
    return redirect(url_for('login'))

#Dashboard page
@app.route("/dashboard")
@is_logged_in
def dashboard():
    blockchain = get_blockchain().chain
    print(blockchain[0])
    ct = time.strftime("%I:%M %p")
    return render_template('dashboard.html',  session=session, ct=ct, blockchain=blockchain, page='dashboard')


#Index page
@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

#Run app
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)
