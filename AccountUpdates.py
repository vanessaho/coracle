from flask import Flask, session, request
from flask import Blueprint, render_template, redirect, url_for
import MySQLdb
from Utils import *
import hashlib


account_update_functions = Blueprint('AccountUpdates', __name__)


@account_update_functions.route('/update_password', methods=['POST'])
def update_password():
	if 'username' in session:
		username = session['username']
		new_pw = request.form['newpass']
		confirm_pw = request.form['confirmnewpass']
		db = connect()
		cursor = db.cursor()
		#cursor.execute('SELECT Password FROM Accounts WHERE Username = \'' + username + '\'')
		#current_pw = cursor.fetchone()[0]
		if(new_pw != confirm_pw):
			# print an error here somehow
			print('passwords do not match')
			session['error'] = 'Passwords don\'t match'
			return redirect(url_for('trip.past_trips'))
			#return render_template('account.html', error = session['error'])
		else:
			new_pw = hashlib.sha256(str.encode(new_pw)).hexdigest()
			cursor.execute('UPDATE Accounts SET Password = \'' + new_pw + '\' WHERE Username = \'' + username + '\'')
			db.commit()
		close_connection(db, cursor)
		return redirect(url_for('index'))


@account_update_functions.route('/delete_account', methods=['POST'])
def delete_account():
	username = session['username']
	db = connect()
	cursor = db.cursor()
	cursor.execute('SELECT TripId FROM Trips WHERE Username = \'' + username + '\'')
	rows = cursor.fetchall()
	for row in rows:
		cursor.execute('DELETE FROM TripAttractions WHERE TripId = \'' + str(row[0]) + '\'')
		cursor.execute('DELETE FROM Trips WHERE TripId = \'' + str(row[0]) + '\'')

		# Don't delete payments because as a company we want to keep records of payments.
		#cursor.execute('DELETE FROM Payment WHERE Username = \'' + username + '\'')
	cursor.execute('SELECT ReviewId FROM WritesReview WHERE Username = \'' + username + '\'')
	reviews = cursor.fetchall()
	for review in reviews:
		cursor.execute('DELETE FROM WritesReview WHERE Username = \'' + username + '\'')
		cursor.execute('DELETE FROM Reviews WHERE ReviewId = \'' + str(review[0]) + '\'')
	cursor.execute('DELETE FROM Accounts WHERE Username = \'' + username + '\'')
	db.commit()
	close_connection(db, cursor)
	session.pop('username')
	return redirect(url_for('index'))


def connect():
	try:
		db = MySQLdb.connect(host = db_host, user = db_user, passwd = db_pass, db = db_name)
		return db
	except Exception as e:
		print('Database failure: \n\n' + e)
		success = False
		return;

def close_connection(db, cursor):
	cursor.close()
	db.close()
