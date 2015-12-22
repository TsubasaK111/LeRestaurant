from flask import Flask, render_template, url_for, request, redirect, flash

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


@app.route('/restaurants/')
def index():
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


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    """page to create a new menu item."""

    if request.method == "POST":
        new_name = request.form['new_name']
        print "\nnewMenuItem POST triggered, name is: ", new_name
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
        newMenuItem = MenuItem( name=new_name,
                                restaurant_id=restaurant.id )
        session.add(newMenuItem)
        session.commit()
        flash( "new item '" + new_name + "' created!")
        print "POST worked!"
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant.id))

    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
        output = render_template('page_head.html', title = "The Menu Manager")
        output += render_template('newMenuItem.html', restaurant = restaurant)
        return output


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    """page to edit a menu item."""

    if request.method == "POST":
        edited_name = request.form['edited_name']
        print "\neditMenuItem POST triggered, name is: ", edited_name
        old_name = session.query(MenuItem).filter_by(id = menu_id).first().name

        result = session.execute("""
                UPDATE menu_item
                SET name=:edited_name
                WHERE id=:edited_menu_item_id;
            """,
            {"edited_name": edited_name,
            "edited_menu_item_id": menu_id}
        )
        session.commit()
        flash( "item '" +  old_name + "' edited to '" + edited_name + "'. Jawohl!")
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))

    else:
        output = render_template('page_head.html', title = "The Menu Manager")
        print "\nrestaurants/restaurant_id/menu_id/edit accessed..."
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
        menuItem = session.query(MenuItem).filter_by(id = menu_id).first()
        output += render_template('editMenuItem.html',
                                  restaurant = restaurant,
                                  menuItem = menuItem )
        return output


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=["GET","POST"])
def deleteMenuItem(restaurant_id, menu_id):
    """page to delete a menu item."""

    if request.method == "POST":
        print "\ndeleteMenuItem POST triggered!, menu_id is: ", menu_id
        deletedMenuItem = session.query(MenuItem).filter_by(id = menu_id).first()
        session.delete(deletedMenuItem)
        session.commit()
        flash( "item '" + deletedMenuItem.name + "' deleted. Auf Wiedersehen!")
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))

    else:
        print "restaurants/delete accessed..."
        output = render_template('page_head.html', title = "The Menu Manager")
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
        menuItem = session.query(MenuItem).filter_by(id = menu_id).first()
        output += render_template( 'deleteMenuItem.html',
                                   menuItem = menuItem,
                                   restaurant = restaurant )
        return output


if __name__ == "__main__":
    app.secret_key = "ZUPA_SECRET_KEY!!!"
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
