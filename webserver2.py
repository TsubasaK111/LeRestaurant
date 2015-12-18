from flask import Flask, render_template, url_for

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
    <link rel="stylesheet" type="text/css" href="bootstrap-theme.min.css">
</head>
<body>
"""
# bootstrap links, for future reference
# <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
# <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    print restaurant
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    output = render_template('menu.html', restaurant=restaurant, menuItems=menuItems)
    return output

@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    """page to create a new menu item."""
    output = page_head
    output += """\n
        <form method = 'POST' enctype = 'multipart/form-data' action = '/new'>
            <h1>Add a new Restaurant!</h1>
            <input name = 'new restaurant name' type = 'text' >
            <input type = 'submit' value = 'Submit'>
        </form>
    """
    # return output
    return "page to create a new menu item. Task 1 complete!"

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    """page to edit a menu item."""
    output = page_head
    print "restaurants/restaurant_id/menu_id/edit accessed..."

    print "restaurant_id sez: ", restaurant_id
    restaurant = session.query(Restaurant).\
        filter_by(id = restaurant_id).first()
    print "restaurant query sez: ", restaurant
    restaurant_name = restaurant.name
    print "restaurant_name is: ", restaurant_name

    print "menu_id sez: ", menu_id
    item = session.query(MenuItem).\
        filter_by(id = menu_id).first()
    print "menuItem query sez: ", item
    menu_name = item.name
    print "menu_name is: ", menu_name

    output += """\n
        <form method = 'POST' enctype = 'multipart/form-data' action = '/%s/%s/edited'>
            <h1>Rename your Menu Item</h1>
            <input name = 'edited menu item name' type = 'text' placeholder = '%s'>
            <input type = 'submit' value = 'Submit'>
        </form>
    """ % (restaurant_id, menu_id, menu_name)
    output += "<a href='/restaurants/'>return to listing</a>"
    output += "</body></html>"
    # return output
    return "page to edit a menu item. Task 2 complete!"

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    """page to delete a menu item."""
    output = page_head
    print "restaurants/delete accessed..."

    print "restaurant_id sez: ", restaurant_id
    restaurant = session.query(Restaurant).\
        filter_by(id = restaurant_id).first()
    print "restaurant query sez: ", restaurant
    restaurant_name = restaurant.name
    print "restaurant_name is: ", restaurant_name

    print "menu_id sez: ", menu_id
    item = session.query(MenuItem).\
        filter_by(id = menu_id).first()
    print "menuItem query sez: ", item
    menu_name = item.name
    print "menu_name is: ", menu_name

    output += """\n
        <form method = 'POST' enctype = 'multipart/form-data' action = '/%s/%s/deleted'>
            <h1>Delete your Menu Item</h1>
            <p> Are you sure you want to delete '%s'?</p>
            <input type = 'submit' value = 'Delete'>
        </form>
    """  % (restaurant_id, menu_id, menu_name)
    output += "<a href='/restaurants/'>return to listing</a>"
    output += "</body></html>"
    # return output
    return "page to delete a menu item. Task 3 complete!"

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
