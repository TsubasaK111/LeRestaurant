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
    output = render_template('page_head.html', title = "The Menu Manager")
    restaurants = session.query(Restaurant).all()

    for restaurant in restaurants:
        menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
        output += render_template( 'menu.html',
                                   restaurant=restaurant,
                                   menuItems=menuItems )
        output += "<br>BREAKBREAKBREAK<br>"
    return output

@app.route('/restaurants/public')
def publicRestaurants():
    output = render_template('page_head.html', title = "The Menu Manager")
    restaurants = session.query(Restaurant).all()

    for restaurant in restaurants:
        menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
        creator = getUserInfo(restaurant.user_id)
        output += render_template('publicMenu.html', menuItems = menuItems, restaurant = restaurant, creator= creator)
        output += "<br>JANKJANKJANK<br>"
    print "publicRestaurants!"
    return output
