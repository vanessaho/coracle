from flask import Flask, session
from flask import Blueprint, render_template, redirect, url_for, request
import MySQLdb
import json
from flask import jsonify
from Utils import *
from datetime import datetime
from urllib.parse import unquote


# Just for future reference, the string passed into the constructor of Blueprint() (in this case 'regFile')
# needs to be different for all blueprints. Otherwise, there is a collision in naming and an error.
booking_functions = Blueprint('Booking', __name__)



@booking_functions.route("/booking")
def booking():
	if 'username' in session:
		if 'error' in session:
			errorMessage = session['error']
			session.pop('error', None)
			return render_template('booking.html', username=session['username'], error = errorMessage)
		return render_template('booking.html', username=session['username'])
	return redirect(url_for('index'))

@booking_functions.route("/booking2", methods=['POST'])
def booking2():
	if 'username' in session:
		
		fromCity = request.form['from']
		toCity = request.form['to']
		startDate = request.form['start']
		endDate = request.form['end']
		print(startDate)
		print(endDate)
		numTickets = request.form['tickets']

		if int(numTickets) <= 0:
			print("WRONG NUM TICKETS")
			session['error'] = 'Invalid number of tickets!'
			return redirect(url_for('Booking.booking'))
		modeOfTransport = request.form['transportation']
		accommodation = request.form['accommodation']
		transportationId = 0
		accommodationId = 0
		totalCost = 0

		if modeOfTransport == 'Plane':
			transportationId = 1
		elif modeOfTransport == 'Cruise':
			transportationId = 2
		elif modeOfTransport == 'Train':
			transportationId = 3
		elif modeOfTransport == 'Car':
			transportationId = 4

		if accommodation == 'Hotel':
			accommodationId = 1
		elif accommodation == 'Airbnb':
			accommodationId = 2

		try:
			db = MySQLdb.connect(host = db_host, user=db_user, passwd=db_pass, db=db_name)
			cursor = db.cursor()
			cursor2 = db.cursor()

			attractions = []

			cursor.execute("SELECT LocationId FROM Locations WHERE CityName='" + toCity + "';")
			LId = cursor.fetchone()[0]
			cursor.execute("SELECT * FROM Attractions WHERE LocationId = " + str(LId) + ";")
			
			for row in cursor.fetchall():
				a = Attraction()
				a.name = row[1]
				a.description = row[3]
				if row[1].find('Zoo') != -1:
					a.attractionType = 'Zoo'
				elif row[1].find('Museum') != -1:
					a.attractionType = 'Museum'
				elif row[1].find('Restaurant') != -1:
					a.attractionType = 'Restaurant'
				elif row[1].find('University') != -1:
					a.attractionType = 'University'
				elif row[1].find('Market') != -1:
					a.attractionType = 'Market'
				else:
					print("Invalid attraction type.")
					return redirect( url_for('index') )

				# attrName = unquote(a.name)
				temp = a.name.replace("'", "\\'") # Use this variable for database queries and anything that requires "\" for special characters.
				print(a.name)
				print("SELECT AttractionId FROM Attractions WHERE Name='" + temp + "';")
				cursor2.execute("SELECT AttractionId FROM Attractions WHERE Name='" + temp + "';")
				a.Id = cursor2.fetchone()[0]
				print("A.ID: " + str(a.Id))
				attractions.append(a)

			accommodationType = request.form['accommodation']
			print("HERE1")
			numPeople = request.form['tickets']
			print("HERE2")
			transportationType = request.form['transportation']
			print("HERE3")
			cursor.execute('SELECT RatePerNight FROM Accommodation WHERE AccomodationType = \'' 
				+ accommodationType + '\';')
			nightlyRate = cursor.fetchone()[0]
			print("nightlyrate" + str(nightlyRate))
			cursor.execute('SELECT Cost FROM Transportation WHERE TransportationId = ' + 
				str(transportationId) + ';')
			cost = cursor.fetchone()[0]
			print("COST: " + str(cost))
			totalCost = float(cost) * float(numPeople) + float(nightlyRate)

			totalCost = int(totalCost)

			cursor.close()
			cursor2.close()
			db.close()
		except Exception as e:
			print(e)
			print('There was an error somewhere in processing the booking form!!!!!!!!!')

		return render_template('booking2.html', username=session['username'], fromCity=fromCity, toCity=toCity, startDate=startDate, endDate=endDate, numtickets=numTickets, trans=transportationId, accom=accommodationId, attractions=attractions, cost=totalCost)
	return render_template('booking2.html')

@booking_functions.route("/Process_Booking", methods=['POST'])
def process_booking():
	success = True
	if 'username' in session:
		fromCity = request.form['from']
		toCity = request.form['to']
		startDate = request.form['start']
		endDate = request.form['end']
		numtickets = request.form['numtickets']
		transportationId = request.form['transport']
		accommodationId = request.form['accommodation']
		cost = request.form['cost']

		# attractions will be an array
		attractions = request.form.getlist('attractions[]')
		print(attractions)
		print("HERE1")
		cardNum = request.form['cardnum']
		cardSecurityCode = request.form['cvv']
		cardExpirationDate = request.form['expiration'] + '-01'
		cardName = request.form['cardholdername']

		paymentAmount = cost
		# paymentAmount = request.form['amount']
		payDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		if startDate == "" or endDate == "":
			session['error'] = 'Invalid dates!'
			return redirect(url_for(Booking.booking))

		try:
			db = MySQLdb.connect(host = db_host, user=db_user, passwd=db_pass, db=db_name)
			cursor = db.cursor()
			print("HERE2")

			# cursor.execute("INSERT INTO Payment (CardNumber, CardSecurityCode, Amount, ExpirationDate, PaymentDate, CardName) VALUES (" + cardNum + ", " + cardSecurityCode + ", " + paymentAmount + ", '" + cardExpirationDate + "', '" + payDate + "', '" + cardName + "');")
			paymentInsert = "INSERT INTO Payment (CardNumber, CardSecurityCode, Amount, ExpirationDate,"
			paymentInsert += ("PaymentDate, CardName) VALUES (" + str(cardNum) + ", " + str(cardSecurityCode) + ", " + str(paymentAmount))
			paymentInsert += (", '" + cardExpirationDate + "', '" + payDate + "', '" + cardName + "');")
			cursor.execute(paymentInsert)
			db.commit()

			cursor.execute("SELECT LocationId FROM Locations WHERE CityName = '" + fromCity + "';")
			fromLId = cursor.fetchone()[0]
			cursor.execute("SELECT LocationId FROM Locations WHERE CityName = '" + toCity + "';")
			toLId = cursor.fetchone()[0]

			cursor.execute("SELECT COUNT(*) FROM Trips;")
			numTrips = cursor.fetchone()[0]
			numTrips += 1

			cursor.execute("SELECT COUNT(*) FROM Payment;")
			numPayments = cursor.fetchone()[0]

			# Insert into trips
			# comTrip = "INSERT INTO Trips (TripId, Username, FromLocationId, ToLocationId, StartDate, EndDate,"
			# comTrip += "TransportationId, AccommodationId, PaymentId, NumPeople) VALUES ("
			comTrip = "INSERT INTO Trips VALUES ("
			comTrip += (str(numTrips) + ", '" + session['username'] + "', " + str(fromLId) + ", " + str(toLId) + ", '" + startDate)
			comTrip += ("', '" + endDate + "', " + str(transportationId) + ", " + str(accommodationId) + ", " + str(numPayments))
			comTrip += (", " + str(numtickets) + ");")
			print(comTrip)
			cursor.execute(comTrip)
			db.commit()

			# Insert into TripAttractions
			for i in attractions:
				cursor.execute('INSERT INTO TripAttractions (TripId, AttractionId) VALUES (' + str(numTrips) + ', ' + i + ');')
				db.commit()

			# Insert into payment
			# paymentInsert = "INSERT INTO Payment (CardNumber, CardSecurityCode, Amount, ExpirationDate,"
			# paymentInsert += ("PaymentDate, CardName) VALUES (" + cardNum + ", " + cardSecurityCode + ", " + paymentAmount)
			# paymentInsert += (", '" + cardExpirationDate + "', '" + payDate + "', '" + cardName + "');")
			# cursor.execute(paymentInsert)
			# db.commit()

			cursor.close()
			db.close()
		except Exception as e:
			print(e)
			print('There was an error somewhere in processing the booking form.')
		
		# View past pages
		return redirect(url_for('index'))

	return redirect(url_for('index'))


# Handle autocomplete of search for cities
@booking_functions.route('/autocomplete', methods=['POST'])
def autocomplete():
	print('autocomplete')
	suggestionCities = []

	db = MySQLdb.connect(host = db_host, user=db_user, passwd=db_pass, db=db_name)
	cursor = db.cursor()

	# cursor.execute('SELECT * FROM Locations WHERE CityName LIKE \'%' + city + '%\'')
	cursor.execute('SELECT * FROM Locations;')

	for row in cursor.fetchall():
		suggestionCities.append(row[1])
		# if (numCities < 5):
		# 	suggestionCities.append(row[1])
		# else:
		# 	break
		# print(str(row[0]) + ' ' + row[1])


	cursor.close()
	db.close()

	jsonReturn = {}
	jsonReturn['status'] = 'OK'

	jsonReturn['cities'] = suggestionCities
	return jsonify(jsonReturn)
    # return json.dumps(jsonReturn)

class Attraction:
	name = ''
	description = ''
	rating = 0
	location = ''
	attractionType = ''
	Id = -1