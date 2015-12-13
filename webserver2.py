from flask import Flask

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
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
</head>
<body>
"""


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def displayIndex(restaurant_id):
    output = page_head
    output += "<h1>The Menu Manager</h1>\n"
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    print restaurant
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    for item in items:
        output += """
            <h2> %s </h2>
            <a href="/restaurant/%s/edit">edit</a>
            <a href="/restaurant/%s/delete">delete</a>
        """ % (item.name, item.id, item.id,)
    output += "</body></html>"
    return output

# @app.route('/

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 8000)
