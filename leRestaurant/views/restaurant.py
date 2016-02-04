# Webserver Dependencies
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

from leRestaurant import app

# Database Dependencies
from leRestaurant.models import session, Restaurant, MenuItem

# Debugging Dependencies
import pdb, pprint, inspect

@app.route('/')
def index():
    return redirect('/restaurants/')
@app.route('/restaurants/')
def restaurants():
    output = render_template('page_head.html', title = "The Menu Manager")
    restaurants = session.query(Restaurant).all()
    for restaurant in restaurants:
        menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
        output += render_template( 'menu.html',
                                   restaurant=restaurant,
                                   menuItems=menuItems )
        output += "<br>BREAKBREAKBREAK<br>"
    return output


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    print "\nrestaurantMenu triggered: ", restaurant
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    output = render_template('page_head.html', title = "The Menu Manager")
    output += render_template( 'menu.html',
                               restaurant=restaurant,
                               menuItems=menuItems )
    return output
