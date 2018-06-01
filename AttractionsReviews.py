
from flask import Flask, session, request
from flask import Blueprint, render_template, redirect, url_for
import MySQLdb
from Utils import *
from urllib.parse import unquote
from datetime import datetime

attractions_reviews_functions = Blueprint('AttractionsReviews', __name__)

@attractions_reviews_functions.route("/AttractionReviews")
def attraction_reviews():
	if 'username' in session:
		return render_template("reviews.html", username=session['username'])

	return render_template("reviews.html")



@attractions_reviews_functions.route("/searchReviews", methods=['POST'])
def searchReviews():

	city = request.form['searchbar']
	print("CITY: " + city)

	try:
		db = MySQLdb.connect(host = db_host, user=db_user, passwd=db_pass, db=db_name)
		cursor = db.cursor()
		cursor2 = db.cursor()

		cursor.execute("SELECT DISTINCT LocationId FROM Locations WHERE CityName='" + city + "';")
		if cursor.rowcount == 1:
			locationId = cursor.fetchone()[0]

		cursor.execute("SELECT * FROM Locations WHERE LocationId=" + str(locationId) + ";")
		row = cursor.fetchone()
		# Don't need to get the city name here becaause we get it from the form.
		country = row[2]
		state = row[3]
		locationString = city + ", " + state
		if state == 'NA':
			locationString = city + ", " + country


		cursor.execute("SELECT * FROM Attractions WHERE LocationId=" + str(locationId) + ";")
		attractions = []
		for row in cursor.fetchall():
			attraction = Attraction()

			attractionId = row[0]
			cursor2.execute("SELECT AVG(Rating) FROM Reviews WHERE AttractionId=" + str(attractionId) + ";")
			averageRating = cursor2.fetchone()[0]

			attraction.name = row[1]
			attraction.location = locationString
			attraction.rating = averageRating
			attraction.descrition = row[3]

			if row[1].find('Zoo') != -1:
				attraction.attractionType = 'Zoo'
			elif row[1].find('Museum') != -1:
				attraction.attractionType = 'Museum'
			elif row[1].find('Restaurant') != -1:
				attraction.attractionType = 'Restaurant'
			elif row[1].find('University') != -1:
				attraction.attractionType = 'University'
			elif row[1].find('Market') != -1:
				attraction.attractionType = 'Market'
			else:
				print("Invalid attraction type.")
				return redirect( url_for('index') )

			attractions.append(attraction)
		
		cursor.close()
		cursor2.close()
		db.close()

		if 'username' in session:
			return render_template("reviews.html", username=session['username'], city=city, attractions=attractions)
		return render_template("reviews.html", city=city, attractions=attractions)
	except Exception as e:
		print('Database failure: \n\n' + str(e))
	return None



@attractions_reviews_functions.route("/Attraction/<AttractionName>")
def view_attraction(AttractionName):

	print(AttractionName)
	attrName = unquote(AttractionName)
	AttractionName = attrName.replace("'", "\\'") # Use this variable for database queries and anything that requires "\" for special characters.
	attractionType = ''
	print(AttractionName)

	try:

		if attrName.find('Zoo') != -1:
			attractionType = 'Zoo'
		elif attrName.find('Museum') != -1:
			attractionType = 'Museum'
		elif attrName.find('Restaurant') != -1:
			attractionType = 'Restaurant'
		elif attrName.find('University') != -1:
			attractionType = 'University'
		elif attrName.find('Market') != -1:
			attractionType = 'Market'
		else:
			print("Invalid attraction type.")
			return redirect( url_for('index') )


		db = MySQLdb.connect(host = db_host, user=db_user, passwd=db_pass, db=db_name)
		cursor = db.cursor()
		cursor2 = db.cursor()

		cursor.execute("SELECT * FROM Attractions WHERE Name='" + AttractionName + "';")
		if cursor.rowcount <= 0:
			print("Valid attraction type but not a valid full attraction name.")
			return redirect( url_for('index') )
		row = cursor.fetchone()
		attractionId = row[0]
		locationId = row[2]
		description = row[3]
		cursor.execute("SELECT * FROM Locations WHERE LocationId=" + str(locationId) + ";")
		row = cursor.fetchone()
		city = row[1]
		country = row[2]
		state = row[3]
		locationString = city + ", " + state

		if state == 'NA':
			locationString = city + ", " + country

		cursor.execute("SELECT AVG(Rating) FROM Reviews WHERE AttractionId=" + str(attractionId) + ";")
		averageRating = cursor.fetchone()[0]

		cursor.execute("SELECT * FROM Reviews WHERE AttractionId=" + str(attractionId) + ";")

		reviews = []
		for row in cursor.fetchall():
			cursor2.execute("SELECT Username FROM WritesReview WHERE ReviewId=" + str(row[0]) + ";")
			username = cursor2.fetchone()[0]
			rating = row[1]
			reviewText = row[3]
			postDate = row[4]
			
			r = Review()
			r.username = username
			r.rating = rating
			r.reviewText = reviewText
			r.postDate = postDate
			reviews.append(r)

		
		cursor.close()
		cursor2.close()
		db.close()

		if 'username' in session:
			return render_template("attraction.html", username=session['username'], attrType=attractionType, avgRating = averageRating, name = attrName, city = locationString, locationId = locationId, description = description, reviews=reviews, attractionId = attractionId)
		return render_template("attraction.html", attrType=attractionType, avgRating = averageRating, name = attrName, city = locationString, locationId = locationId, description = description, reviews=reviews, attractionId = attractionId)
	except Exception as e:
		print('Database failure: \n\n' + str(e))

	print("Error Displaying Reviews")
	return redirect(url_for('index'))
	

@attractions_reviews_functions.route("/PostReview", methods=['POST'])
def post_review():
	if 'username' not in session:
		print("Not logged in. Shouldn't be allowed to post a review.")
		return redirect( url_for('index') )
	print("HERE 1")
	attractionId = request.form['AttractionId']
	reviewText = request.form['reviewtext']
	username = session['username']
	rating = request.form['review']
	attractionName = ""

	print("HERE 2")
	try:
		db = MySQLdb.connect(host = db_host, user=db_user, passwd=db_pass, db=db_name)
		print("HERE 3")
		cursor = db.cursor()

		cursor.execute("SELECT Name FROM Attractions WHERE AttractionId=" + str(attractionId) + ";")
		attractionName = cursor.fetchone()[0]

		cursor.execute("SELECT COUNT(*) FROM Reviews;")
		numReviews = cursor.fetchone()[0]
		numReviews += 1

		insertDate = datetime.now().strftime('%Y-%m-%d')
		print("HERE4")
		insertCommand = "INSERT INTO Reviews VALUES (" + str(numReviews) + ", " + str(rating) + ", " + str(attractionId)
		insertCommand += (", '" + reviewText + "', '" + insertDate + "');")
		cursor.execute(insertCommand);
		db.commit()
		print("HERE 5")
		cursor.execute("INSERT INTO WritesReview VALUES (" + str(numReviews) + ", '" + username + "');")
		db.commit()
		print("HERE 6")
		cursor.close()
		db.close()

		if 'username' in session:
			return redirect(url_for('AttractionsReviews.view_attraction', username = username, AttractionName = attractionName))
#			return render_template("attraction.html", username=session['username'], attrType=attractionType, avgRating = averageRating, name = attrName, city = locationString, locationId = locationId, description = description, reviews=reviews)
#		return render_template("attraction.html", attrType=attractionType, avgRating = averageRating, name = attrName, city = locationString, locationId = locationId, description = description, reviews=reviews)
	except Exception as e:
		print('Database failure: \n\n' + str(e))
	
	return redirect(url_for('AttractionsReviews.view_attraction'), AttractionName = attractionName)



class Review:
	username = ''
	rating = 0
	reviewText = ''
	postDate = ''

class Attraction:
	name = ''
	description = ''
	rating = 0
	location = ''
	attractionType = ''