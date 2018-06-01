from flask import Flask, render_template, session, request, Blueprint
from Accounts import accounts_functions
from cities import city_functions
from Booking import booking_functions
from ViewPastTrips import trips_functions
from AttractionsReviews import attractions_reviews_functions
from AccountUpdates import account_update_functions

import MySQLdb

app = Flask(__name__, static_url_path = '/static')

app.register_blueprint(accounts_functions)
app.register_blueprint(city_functions)
app.register_blueprint(booking_functions)
app.register_blueprint(trips_functions)
app.register_blueprint(attractions_reviews_functions)
app.register_blueprint(account_update_functions)


@app.route("/index")
@app.route("/")
def index():

	#session['username'] = 'username'

	if 'username' in session:
		return render_template('index.html', username=session['username'])
	"""
	try:
		db = MySQLdb.connect(host = "localhost", user="Dan", passwd="", db="testdb")
		cursor = db.cursor()

		cursor.execute("SELECT * FROM people")
		for row in cursor.fetchall():
			print(str(row[0]) + ' ' + row[1])

		cursor.close()
		db.close()
	except:
		pass
	"""


	return render_template('index.html')


# 404 Error: Display our own custom error page
@app.errorhandler(404)
def page_does_not_exit(e):
	page = '<!DOCTYPE html>\n<html>\n<body>\n'
	page += '<p>This is not a valid URL.</p>\n'
	page += '</body>\n</html>'
	return page

# 400 Error: Bad request page
@app.errorhandler(400)
def bad_request_page(e):
	page = '<!DOCTYPE html>\n<html>\n<body>\n'
	page += '<p>You made a bad URL request.</p>\n'
	page += '</body>\n</html>'
	return page


if __name__ == "__main__":
	# Took this secret key from the 'Quick Start' guide on the Flask website.
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run()