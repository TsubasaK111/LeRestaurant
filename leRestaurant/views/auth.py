# Webserver Dependencies
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from leRestaurant import app

# Database Dependencies
from leRestaurant.models import session, User, Restaurant, MenuItem

# Authentication Dependencies
from flask import session as flask_session
import random, string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Debugging Dependencies
import pdb, pprint, inspect

# Open json file containing secrets obtained from Google API Manager and
# store the client ID inside. CLIENT_ID and other secrets generated at:
# https://console.developers.google.com/apis/credentials?project=restaurant-menu-appp
CLIENT_ID = json.loads(
    open("leRestaurant/client_secrets.json", "r").read()
)["web"]["client_id"]


@app.route('/login/')
def login():
    """ login page.
        * generates a random "state" string and
        * pushes state when authorizing with OAuth (google_connect)."""
    def random_string():
        return ( random.choice(string.ascii_uppercase + string.digits)
            for x in xrange(32) )
    print random_string()
    state = ''.join(random_string())
    flask_session['state'] = state
    output = render_template( 'login.html',
                              state = flask_session['state'] )
    return output


@app.route('/google_connect', methods=['POST'])
def google_connect():
    """ responds to /login/'s login attempt with OAuth (google_connect).
        * checks if 'state' is concurrent.
        * kicks you out if not concurrent.
        * attempts to upgrade/exchange 'authorization code'(aka secrets) with credentials object, which has access token. """

    if request.args.get('state') != flask_session['state']:
        response = make_response(json.dumps('Invalid state detected!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        # create flow object and add secrets.
        oauth_flow = flow_from_clientsecrets('leRestaurant/client_secrets.json', scope='')
        # declares this as the one-time-code flow (via postmessage) that server will send.
        oauth_flow.redirect_uri = 'postmessage'

        # initiate exchange with flow and code (aka state and secrets info)
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade authorization code!'), 401 )
        response.headers['Content-Type']='application/json'
        return response

    # Check if access token is valid by sending url with token to google.
    access_token = credentials.access_token
    access_token_validation_url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token )
    connection = httplib2.Http()
    result = json.loads(connection.request(access_token_validation_url, 'GET')[1])

    # Check if error in access token info. If so, abort!
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

    # Verify that client ID in token matches that of this web app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID doesn't match app's ID... (inquisitive face)"), 401 )
        response.headers['Content-Type']='application/json'
        return response

    # Check if user already logged in.
    stored_access_token = flask_session.get('access_token')
    stored_google_plus_id = flask_session.get('google_plus_id')

    if stored_access_token is not None and google_plus_id == stored_google_plus_id:
        print "stored_access_token"
        response = make_response(
            json.dumps('Current user is already connected.'), 200 )
        response.headers['Content-Type']='application/json'

    # Store access token in session for later use.
    flask_session['access_token']=credentials.access_token
    flask_session['google_plus_id']=google_plus_id

    # Get user info
    userinfo_url="https://www.googleapis.com/oauth2/v1/userinfo"
    parameters = { 'access_token':credentials.access_token, 'alt':'json' }
    answer = requests.get(userinfo_url, params = parameters)

    data = answer.json()

    flask_session['username'] = data['name']
    flask_session['picture'] = data['picture']
    try:    flask_session['link'] = data['link']
    except: flask_session['link'] = ""

    try:
        flask_session['email'] = data['email']
        user_id = getUserIdFromEmail(flask_session['email'])
    except:
        flask_session['email'] = ""
        try:    user_id = getUserIdFromLink(flask_session['link'])
        except: user_id = createUser(flask_session)

    user_info_from_db = getUserInfo(user_id)

    # Render user info
    output = render_template("page_head.html", title= "Login Results")
    output += """ <h1>Welcome, {username}!</h1>
                   <img src="{picture}">
              """.format( username = flask_session['username'],
                          picture  = flask_session['picture'] )
    output += "</body></html>"
    flash("You are now logged in as: {username}".\
            format(username = flask_session['username'] ))

    return output

@app.route('/google_disconnect')
def google_disconnect():
    # Only disconnect a connected user.
    access_token = flask_session.get('access_token')
    if access_token is None:
        response = make_response(
                    json.dumps('This user is not connected.'), 401 )
        response.headers['Content-Type'] =  'application/json'
        return response
    # Send GET request to revoke current token
    url = 'https://accounts.google.com/o/oauth2/revoke?token={access_token}'.\
        format( access_token =  access_token )
    result = httplib2.Http().request(url, 'GET')[0]
    if result['status'] == '200':
        del flask_session['access_token']
        del flask_session['google_plus_id']
        del flask_session['username']
        del flask_session['picture']
        del flask_session['link']
        del flask_session['email']

        response = make_response(json.dumps('Goodbye! Till Next Time!!'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # If this session's token was invalid
        response = make_response(
                    json.dumps("!!! Unable to revoke user's token !!!"), 400 )
        response.headers['Content-Type'] = 'application/json'
        return response


def logInRedirect():
    """redirect routes to the login page."""
    thisFunction = inspect.stack()[1][3]
    flash("It appears you're not logged in. Log in to access " + thisFunction + ".")
    return redirect('/login')


def createUser(flask_session):
    newUser = User( name = flask_session['username'],
                    picture = flask_session['picture'],
                    link = flask_session['link'],
                    email = flask_session['email'] )
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(link = flask_session['link']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user


def getUserIdFromEmail(email):
    user = session.query(User).filter_by(email = email).one()
    return user.id


def getUserIdFromLink(link):
    user= session.query(User).filter_by(link = link).one()
    return user.id
