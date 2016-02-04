# Webserver Dependencies
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from leRestaurant import app

# Database Dependencies
from leRestaurant.models import session, User, Restaurant, MenuItem

#Another attempt at an API endpoint (GET Req)
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).filter_by(id = menu_id).one()
    return jsonify(MenuItem = menuItem.serialize)


#A first attempt at an API endpoint (GET Req)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [menuItem.serialize for menuItem in menuItems])
