# Webserver Dependencies
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

from leRestaurant import app

# Database Dependencies
from leRestaurant.models import session, Restaurant, MenuItem

# Auth Dependencies
from auth import *

# Debugging Dependencies
import pdb, pprint, inspect


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    """page to create a new menu item."""

    if 'access_token' not in flask_session:
        return logInRedirect()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    user_id = getUserId(flask_session['email'],flask_session['google_plus_id'])
    if not restaurant.user_id == user_id:
        flash("Only restaurant owners can add new items.")
        return redirect(url_for("publicMenu",restaurant_id = restaurant_id))

    if request.method == "POST":
        new_name = request.form['new_name']
        print "\nnewMenuItem POST triggered, name is: ", new_name
        newMenuItem = MenuItem( name=new_name,
                                restaurant_id=restaurant.id )
        session.add(newMenuItem)
        session.commit()
        flash( "new item '" + new_name + "' created!")
        print "POST worked!"
        return redirect(url_for("showMenu", restaurant_id=restaurant.id))

    else:
        return render_template('newMenuItem.html', restaurant = restaurant)


@app.route('/restaurants/<int:restaurant_id>/public')
def publicMenu(restaurant_id):
    """ displays all menu items for a restaurant id, read-only."""

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    creator = getUserInfo(restaurant.user_id)

    return render_template( 'publicMenu.html',
                            menuItems = menuItems,
                            restaurant = restaurant,
                            creator= creator )


@app.route('/restaurants/<int:restaurant_id>/')
def showMenu(restaurant_id):
    """ displays all menu items for a restaurant id, with all CRUD options."""

    if 'access_token' not in flask_session:
        return logInRedirect()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    user_id = getUserId(flask_session['email'],flask_session['google_plus_id'])
    if not restaurant.user_id == user_id:
        return redirect(url_for("publicMenu",restaurant_id = restaurant_id))

    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    creator = getUserInfo(restaurant.user_id)

    return render_template( 'showMenu.html',
                            restaurant = restaurant,
                            menuItems = menuItems,
                            creator = creator )


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    """page to edit a menu item."""

    if 'access_token' not in flask_session:
        return logInRedirect()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    user_id = getUserId(flask_session['email'],flask_session['google_plus_id'])
    if not restaurant.user_id == user_id:
        return redirect(url_for("publicMenu",restaurant_id = restaurant_id))
        flash("Only restaurant owners can edit items.")

    if request.method == "POST":
        edited_name = request.form['edited_name']
        print "\neditMenuItem POST triggered, name is: ", edited_name
        old_name = session.query(MenuItem).filter_by(id = menu_id).first().name

        result = session.execute(""" UPDATE menu_item
                                     SET name=:edited_name
                                     WHERE id=:edited_menu_item_id; """,
                                 { "edited_name": edited_name,
                                   "edited_menu_item_id": menu_id}
                                 )
        session.commit()
        flash( "item '" +  old_name + "' edited to '" + edited_name + "'. Jawohl!")
        return redirect(url_for("showMenu", restaurant_id=restaurant_id))

    else:
        menuItem = session.query(MenuItem).filter_by(id = menu_id).first()
        return render_template('editMenuItem.html',
                                  restaurant = restaurant,
                                  menuItem = menuItem )


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=["GET","POST"])
def deleteMenuItem(restaurant_id, menu_id):
    """page to delete a menu item."""

    if 'access_token' not in flask_session:
        return logInRedirect()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    user_id = getUserId(flask_session['email'],flask_session['google_plus_id'])
    if not restaurant.user_id == user_id:
        flash("Only restaurant owners can delete items.")
        return redirect(url_for("publicMenu",restaurant_id = restaurant_id))

    if request.method == "POST":
        print "\ndeleteMenuItem POST triggered!, menu_id is: ", menu_id
        deletedMenuItem = session.query(MenuItem).filter_by(id = menu_id).first()
        session.delete(deletedMenuItem)
        session.commit()
        flash( "item '" + deletedMenuItem.name + "' deleted. Auf Wiedersehen!")
        return redirect(url_for("showMenu", restaurant_id=restaurant_id))

    else:
        print "restaurants/delete accessed..."
        menuItem = session.query(MenuItem).filter_by(id = menu_id).first()
        return render_template( 'deleteMenuItem.html',
                                   menuItem = menuItem,
                                   restaurant = restaurant )
