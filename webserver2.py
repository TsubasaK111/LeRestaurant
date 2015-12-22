from flask import Flask, render_template, url_for, request, redirect

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem

import pdb
import pprint

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DatabaseSession = sessionmaker(bind = engine)
session = DatabaseSession()

#common html code
page_head = """
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>The Menu Manager</title>
    <!-- Bootstrap 3 -->
    <link rel="stylesheet" type="text/css" href="bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="bootstrap-theme.min.css" />
</head>
<body>
"""

# bootstrap links, for future reference
# <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
# <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    print "restaurantMenu triggered: ", restaurant
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    output = render_template('page_head.html', title = "The Menu Manager")
    output += render_template('menu.html', restaurant=restaurant, menuItems=menuItems)
    return output


@app.route('/restaurants/')
def index():
    return redirect(url_for("restaurantMenu", restaurant_id="2"))


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    """page to create a new menu item."""

    if request.method == "POST":
        print "POST triggered, name is: ", request.form['new_name']
        newMenuItem = MenuItem( name=request.form['new_name'],
                                restaurant_id=restaurant_id )
        session.add(newMenuItem)
        session.commit()
        print "POST worked!"
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
        output = render_template('page_head.html', title = "The Menu Manager")
        output += render_template('newMenuItem.html', restaurant = restaurant)
        return output


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    """page to edit a menu item."""

    if request.method == "POST":
        print "POST triggered, name is: ", request.form['edited_name']
        result = session.execute("""
                UPDATE menu_item
                SET name=:edited_name
                WHERE id=:edited_menu_item_id;
            """,
            {"edited_name": request.form['edited_name'],
            "edited_menu_item_id": menu_id}
        )
        print "result is: ", result
        session.commit()
        print "POST worked!"
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
    else:
        output = render_template('page_head.html', title = "The Menu Manager")
        print "restaurants/restaurant_id/menu_id/edit accessed..."

        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
        menuItem = session.query(MenuItem).filter_by(id = menu_id).first()
        print "menuItem name iz: ", menuItem.name

        output += render_template('editMenuItem.html',
                                  restaurant = restaurant,
                                  menuItem = menuItem )
        return output
        # return "page to edit a menu item. Task 2 complete!"


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    """page to delete a menu item."""
    output = render_template('page_head.html', title = "The Menu Manager")
    print "restaurants/delete accessed..."

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    menuItem = session.query(MenuItem).filter_by(id = menu_id).first()
    print "menuItem query sez: ", menuItem

    output += render_template( 'deleteMenuItem.html',
                               menuItem = menuItem,
                               restaurant = restaurant )
    return output
    # return "page to delete a menu item. Task 3 complete!"


if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
