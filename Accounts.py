from flask import Flask, session, request
from flask import Blueprint, render_template, redirect, url_for
import MySQLdb
from Utils import *
import hashlib



# Just for future reference, the string passed into the constructor of Blueprint() (in this case 'regFile')
# needs to be different for all blueprints. Otherwise, there is a collision in naming and an error.
accounts_functions = Blueprint('Accounts', __name__)

# This is meant for displaying the actual signup page.
@accounts_functions.route("/signup")
def signup():
	if 'username' in session:
		return redirect(url_for('index'), username=session['username'])
	return render_template('register.html')

# This is meant for handling the signup form after user clicks "submit"
@accounts_functions.route("/process_registration", methods=['POST'])
def createAccount():
	success = True
	# GET DATA USES: request.args
	# POST DATA USES: request.form

	email = request.form['email']
	username = request.form['username']
	password = request.form['password']
	confirmpassword = request.form['confirmpassword']

	print(request.form['terms'])
	print(request.form['privacy'])

	# Basic checks on the information
	if not email or not username or not password or not confirmpassword:
		success = False
	if password != confirmpassword or len(password) < 1 or len(confirmpassword) < 1:
		success = False
		print('Pass is not the same')
	if email.find('@') == -1 or len(email) < 3:
		success = False
	if not request.form.get('terms'):
		success = False
	if not request.form.get('privacy'):
		success = False

	if success:
		# Check database for previous emails or usernames. If they exist, fail. Else, add user and succeed.
		try:
			db = MySQLdb.connect(host = db_host, user=db_user, passwd=db_pass, db=db_name)
			cursor = db.cursor()

			password = hashlib.sha256(str.encode(password)).hexdigest()
			cursor.execute("INSERT INTO Accounts VALUES (\'" + username + "\', \'" + password + "\', \'" + email + "\');")
			db.commit()
			cursor.close()
			db.close()
		except Exception as e:
			print('Database failure: \n\n' + str(e))
			success = False
			
	# If successfully registered, redirect to home page with logged in status.
	# Else, return to signup page and potentially add message with reason for fail.
	if success:
		return redirect(url_for('index'))
	else:
		print('Error')
		return redirect(url_for('Accounts.signup'))


# This is meant for displaying the actual login page.
@accounts_functions.route("/login")
def login():
	if 'error' in session:
		error = session['error']
		session.pop('error')
		return redirect(url_for('login'))
	if 'username' in session:
		return redirect(url_for('index'))
	return render_template('login.html')


# This is meant for handling the login form after user clicks "submit"
# Let user input enter the username or email along with password.
@accounts_functions.route("/process_login", methods=['POST'])
def validate_login():
	success = True

	username = request.form['username']
	password = request.form['password']
	try:
		db = MySQLdb.connect(host = db_host, user=db_user, passwd=db_pass, db=db_name)
		cursor = db.cursor()

		password = hashlib.sha256(str.encode(password)).hexdigest()
		# Check to see if email/username match and password match with record in database.
		cursor.execute('SELECT * FROM Accounts WHERE Username = \'' + username + '\' AND Password=\'' + password + '\';')

		# Failed to authenticate if exactly 1 row isn't returned. No tuple with matching username and password.
		if cursor.rowcount != 1: # Failed
			success = False

		cursor.close()
		db.close()
	except Exception as e:
		print('Database failure: \n\n' + str(e))
		success = False

	if success:
		session['username'] = request.form['username']
		return redirect(url_for('index'))
	else:
		return redirect(url_for('Accounts.login'))

# Handle logout here. Simply redirect to home page at the end. No need for special logout page.
@accounts_functions.route("/logout")
def logout():
	# Remove username from session
	session.pop('username', None)
	return redirect(url_for('index'))