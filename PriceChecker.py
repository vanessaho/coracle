from flask import Flask, session, request
from flask import Blueprint, render_template, redirect, url_for
from flask import jsonify
import MySQLdb
from Utils import *
import hashlib

price_check_functions = Blueprint('PriceChecker', __name__)


@price_check_functions.route('/get_price', methods=['POST'])
def get_price():
	accommodationType = request.form['accommodation']
	numPeople = request.form['tickets']
	transportationType = request.form['transportation']
	db = connect()
	cursor = db.cursor()
	cursor.execute('SELECT RatePerNight FROM Accommodation WHERE AccommodationType = \'' 
		+ accommodationType + '\'')
	nightlyRate = cursor.fetchone()[0]
	cursor.execute('SELECT Cost FROM Transportation WHERE TransportationId = \'' + 
		transportationType + '\'')
	cost = cursor.fetchone()[0]
	totalCost = cost * numPeople + nightlyRate
	return jsonify({'price': totalCost})


@price_check_functions.route('/show_facilities')
def show_facilities():
	db = connect()
	cursor = db.cursor()
	cursor.execute('SELECT Facilities FROM Accommodation WHERE AccommodationId = 1')
	hotelFacilities = cursor.fetchone()[0]
	print(hotelFacilities)
	cursor.execute('SELECT Facilities FROM Accommodation WHERE AccommodationId = 2')
	airbnbFacilities = cursor.fetchone()[0]
	print(airbnbFacilities)
	return render_template('booking.html', hotelFacilities = hotelFacilities, 
		airbnbFacilities = airbnbFacilities)


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
