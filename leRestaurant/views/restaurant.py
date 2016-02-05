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

@app.route('/restaurants/')
def showRestaurants():
    return redirect('restaurants/public')

@app.route('/restaurants/public')
def publicRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('publicRestaurants.html', restaurants=restaurants)

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    """page to create a new menu item."""

    if 'access_token' not in flask_session:
        return logInRedirect()

    user_id = getUserId(flask_session['email'],flask_session['google_plus_id'])

    if request.method == "POST":
        new_name = request.form['new_name']
        print "\nnewRestaurant POST triggered, name is: ", new_name
        newRestaurant = Restaurant( name=new_name,
                                    user_id = user_id )
        session.add(newRestaurant)
        session.commit()
        flash( "new restaurant '" + new_name + "' created!")
        print "POST worked!"

        return redirect(url_for("showRestaurants"))

    else:
        # pdb.set_trace()
        return render_template('newRestaurant.html')
        # output = render_template('page_head.html', title = "The Menu Manager")
        # output += render_template('newMenuItem.html', restaurant = restaurant)
        # return output
