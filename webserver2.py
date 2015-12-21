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
        print "POST triggered, name is: ", request.form['name']
        newMenuItem = MenuItem( name=request.form['name'],
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
    output = render_template('page_head.html', title = "The Menu Manager")
    print "restaurants/restaurant_id/menu_id/edit accessed..."
    item = session.query(MenuItem).filter_by(id = menu_id).first()
    print "menuItem query sez: ", item

    output += render_template('editMenuItem.html',
                              restaurant_id = restaurant_id,
                              menu_id = item.id )
    return output
    # return "page to edit a menu item. Task 2 complete!"


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    """page to delete a menu item."""
    output = render_template('page_head.html', title = "The Menu Manager")
    print "restaurants/delete accessed..."

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
    return output
    # return "page to delete a menu item. Task 3 complete!"


if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
