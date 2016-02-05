# Webserver Dependencies
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

from leRestaurant import app

# Database Dependencies
from leRestaurant.models import session, Restaurant, MenuItem

# Auth Dependencies
from auth import *

# Debugging Dependencies
import pdb, pprint, inspect

@app.route('/')
def index():
    return redirect('/restaurants/')

# @app.route('/restaurants/new')
# def newRestaurant():
#     if 'access_token' not in flask_session:
#         return logInRedirect()
#     return render_template('newRestaurant.html')

@app.route('/restaurants/')
def showRestaurants():
    return redirect('restaurants/public'))

@app.route('/restaurants/public')
def publicRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('publicRestaurants.html', restaurants=restaurants)
