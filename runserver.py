# Webserver Dependencies
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify

# Database Dependencies
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Authentication Dependencies
from flask import session as flask_session
import random, string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Debugging Dependencies
import pdb
import pprint


app = Flask(__name__)

# Open json file containing secrets obtained from Google API Manager and
# store the client ID inside. CLIENT_ID and other secrets generated at:
# https://console.developers.google.com/apis/credentials?project=restaurant-menu-appp
CLIENT_ID = json.loads(
    open("client_secrets.json", "r").read()
)["web"]["client_id"]


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DatabaseSession = sessionmaker(bind = engine)
session = DatabaseSession()


@app.route('/login/')
def login():
    """ login page.
        * generates a random "state" string and
        * pushes state when authorizing with OAuth (gconnect)."""
    def random_string():
        return (random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    print random_string()
    state = ''.join(random_string())
    flask_session['state'] = state
    output = render_template( 'login.html',
                              state = flask_session['state'] )
    return output


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """ responds to /login/'s login attempt with OAuth (gconnect).
        * checks if 'state' is concurrent.
        * kicks you out if not concurrent.
        * attempts to upgrade/exchange 'authorization code'(aka secrets) with credentials object. """
    if request.args.get('state') != flask_session['state']:
        response = make_response(json.dumps('Invalid state detected!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # create flow object and add secrets.
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        # declares this as the one-time-code flow (via postmessage) that server will send.
        oauth_flow.redirect_uri = 'postmessage'
        # initiate exchange with flow and code (aka state and secrets info)
        credentials = oauth_flow.setup2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade authorization code!'), 401 )
        response.headers['Content-Type']='application/json'
        return response

    # Check if access token is valid by sending url with token to google.
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token )
    connection = httplib2.Http()
    result = json.loads(connection.request(url, 'GET')[1])
    # If error in access token info, abort!
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 50)
        response.headers['Content-Type']='application/json'
    # Verify that access token is used for intended user.
    google_plus_id = credentials.id_token['sub']
    if result['user_id'] != google_plus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID. WUDDAYA DOIN!?!?!?"), 401 )
        response.headers['Content-Type']='application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID doesn't match app's ID... (inquisitive face)"), 401 )
        print "Token's client ID doesn not match app's ID."
        response.headers['Content-Type']='application/json'
        return response



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




if __name__ == "__main__":
    app.secret_key = "ZUPA_SECRET_KEY!!!"
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
