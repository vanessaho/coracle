from flask import Flask
from flask import Blueprint, render_template, redirect, url_for
from Utils import *
import MySQLdb
import csv
from Utils import *

# Just for future reference, the string passed into the constructor of Blueprint() (in this case 'regFile')
# needs to be different for all blueprints. Otherwise, there is a collision in naming and an error.
city_functions = Blueprint('city', __name__)

# This is meant for displaying the actual signup page.
@city_functions.route("/load_cities")
def load():
	# connect to database
	db = connect();
	if db is None:
		return
	cursor = db.cursor()
	data = csv.reader(open("cities.csv"))
	#cursor.execute('DROP TABLE Attractions')
	#cursor.execute('DROP TABLE Locations')
	cursor.execute('CREATE TABLE Locations (LocationId INT,CityName CHAR(50),Country CHAR(30) NOT NULL,State CHAR(20),PRIMARY KEY (LocationId),CHECK (LocationId > 0));')
	cursor.execute('CREATE TABLE Attractions (AttractionId INT,Name CHAR(100),LocationId INT,Description VARCHAR(2500),PRIMARY KEY (AttractionId),FOREIGN KEY (LocationId) REFERENCES Locations(LocationId),CHECK (Cost >= 0));')
	counter = 0;
	for row in data:
		if(counter == 0):
			counter += 1
			continue
		#for n in range(4):
		#	print(row[n])
		#row[0] = int(row[0])
		#row[3] = row[3][:len(row[3]) - 1]
		cursor.execute('INSERT INTO Locations VALUES (%s,%s,%s,%s);', row)
		db.commit()
		names = []
		descriptions = []
		names.append(row[1] + '\'s Museum')
		descriptions.append('A fun place to look at old stuff')
		names.append(row[1] + '\'s Zoo')
		descriptions.append('Come here to see cool animals')
		names.append(row[1] + '\'s Restaurant')
		descriptions.append('One of the best places to eat in ' + row[1])
		names.append(row[1] + '\'s University')
		descriptions.append('A world famous and prestigous university')
		names.append(row[1] + '\'s Market')
		descriptions.append('A vibrant place to look at and buy local products')
		for i in range(5):
			cursor.execute('INSERT INTO Attractions VALUES (%s,%s,%s,%s);', (counter,names[i],row[0],descriptions[i]))
			db.commit()
			counter += 1
		counter += 1
		

	close_connection(db, cursor);
	return 'added cities and attractions'

def connect():
	try:
		db = MySQLdb.connect(host = db_host, user=db_user, passwd=db_pass, db=db_name)
		return db
	except Exception as e:
		print('Database failure: \n\n' + e)
		success = False
		return;

def close_connection(db, cursor):
	cursor.close()
	db.close()












	