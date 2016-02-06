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
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('showRestaurants.html', restaurants=restaurants)

@app.route('/restaurants/public')
def publicRestaurants():
    if 'access_token' not in flask_session:
        return logInRedirect()
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
        return render_template('newRestaurant.html')

@app.route("/restaurants/<int:restaurant_id>/delete", methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    """page to delete a restaurant (authorized only for creators)."""

    if 'access_token' not in flask_session:
        return logInRedirect()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    user_id = getUserId(flask_session['email'],flask_session['google_plus_id'])
    if not restaurant.user_id == user_id:
        flash("Only restaurant owners can delete restaurants.")
        return redirect(url_for("publicMenu",restaurant_id = restaurant_id))

    if request.method == "POST":
        print "\ndeleteRestaurant POST triggered!"
        deletedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
        session.delete(deletedRestaurant)
        session.commit()
        flash( "item '" + deletedRestaurant.name + "' deleted. Auf Wiedersehen!")
        return redirect(url_for("showRestaurants"))

    else:
        print "restaurants/id/delete accessed..."
        return render_template( "deleteRestaurant.html",
                                restaurant = restaurant )
