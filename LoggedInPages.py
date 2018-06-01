
from flask import Flask
from flask import Blueprint, render_template, redirect, url_for
import MySQLdb
import json
from flask import jsonify


loggedin_functions = Blueprint('loggedin', __name__)

# View cart
@loggedin_functions.route('\Cart')
def cart():
	



# View purchased trips/itineraries
@loggedin_functions.route('\PastTrips')
def trips():
