from flask import Flask, session
from flask import Blueprint, render_template, redirect, url_for
import MySQLdb
from Utils import *

# Just for future reference, the string passed into the constructor of Blueprint() (in this case 'regFile')
# needs to be different for all blueprints. Otherwise, there is a collision in naming and an error.

class Trip:
	fromLocation = ''
	toLocation = ''
	startDate = ''
	endDate = ''
	transportationName = ''
	accommodationName = ''
	paymentAmount = ''
	paymentDate = ''
	attractions = []
trips_functions = Blueprint('trip', __name__)

@trips_functions.route('/past_trips')
def past_trips():
	if 'username' in session:
		trips = []
		username = session['username']
		db = connect();
		cursor = db.cursor();
		#print('SELECT * FROM Trips WHERE Username = \'' + username + '\'')
		cursor.execute('SELECT * FROM Trips WHERE Username = \'' + username + '\'')
		rows = cursor.fetchall()
		for row in rows:
			#0 - TripId INT,
			#1 - Username CHAR(50),
			#2 - FromLocationId INT,
			#3 - ToLocationId INT,
			#4 - StartDate DATE,
			#5 - EndDate DATE,
			#6 - TransportationId INT,
			#7 - AccommodationId INT,
			#8 - PaymentId INT,
			trip = Trip()

			#get from location names
			cursor.execute('SELECT CityName FROM Locations WHERE LocationId = \'' + str(row[2]) + '\'')
			trip.fromLocation = cursor.fetchone()[0]
			cursor.execute('SELECT CityName From Locations WHERE LocationId = \'' + str(row[3]) + '\'')
			trip.toLocation = cursor.fetchone()[0]
			#get dates
			trip.startDate = row[4]
			trip.endDate = row[5]
			#get transportation name
			cursor.execute('SELECT TransportationType FROM Transportation WHERE TransportationId = \'' + str(row[6]) + '\'')
			trip.transportationName = cursor.fetchone()[0]
			#get accomodation name
			cursor.execute('SELECT AccomodationType FROM Accommodation WHERE AccommodationId = \'' + str(row[7]) + '\'') 
			##
			## I misspelled accommocation in my local database, so that's why some of these are misspelled, 
			## make sure to change this
			##
			trip.accommodationName = cursor.fetchone()[0]
			#get date
			cursor.execute('SELECT Amount, PaymentDate FROM Payment WHERE PaymentId = \'' + str(row[8]) + '\'')
			paymentInfo = cursor.fetchone()
			trip.paymentAmount = paymentInfo[0]
			trip.paymentDate = paymentInfo[1]
			#get attractions
			cursor.execute('SELECT AttractionId FROM TripAttractions WHERE TripId = \'' + str(row[0]) + '\'')
			attractionRows = cursor.fetchall();
			visitedAttractions = []
			for attraction in attractionRows:
				cursor.execute('SELECT Name FROM Attractions WHERE AttractionId = \'' + str(attraction[0]) + '\'')
				visitedAttractions.append(cursor.fetchone()[0])
			trip.attractions = visitedAttractions
			trips.append(trip)
		close_connection(db, cursor)

		#return render_template('account.html', username=username, trips = trips)

		if 'error' in session:
			print('error in session')
			error = session['error']
			session.pop('error', None)
			return render_template('account.html', trips = trips, error = error)
		return render_template('account.html', trips = trips)



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
