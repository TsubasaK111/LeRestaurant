from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Restaurant, MenuItem

import pdb

import pprint


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DatabaseSession = sessionmaker(bind = engine)
session = DatabaseSession()

#common html code
page_head = """
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>The Franchise Manager</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
</head>
<body>
"""

new_restaurant_form = """\n
    <form method = 'POST' enctype = 'multipart/form-data' action = '/new'>
        <h1>Add a new Restaurant!</h1>
        <input name = 'new restaurant name' type = 'text' >
        <input type = 'submit' value = 'Submit'>
    </form>
"""

edit_restaurant_form = """\n
    <form method = 'POST' enctype = 'multipart/form-data' action = '%s/edited'>
        <h1>Rename your Restaurant</h1>
        <input name = 'edited restaurant name' type = 'text' >
        <input type = 'submit' value = 'Submit'>
    </form>
"""

#request handler code
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        try:

            if self.path.endswith("/restaurant"):
                print 'serving restaurant! '
                self.send_response(200)
                self.send_header('Content-type', 'text/html' )
                self.end_headers()
                output = page_head
                output += "<h1>The Franchise Manager</h1>\n"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += """
                        <h2> %s </h2>
                        <a href="restaurant/%s/edit">edit</a>
                        <a href="restaurant/%s/delete">delete</a>
                    """ % (restaurant.name, restaurant.id, restaurant.id,)
                output += new_restaurant_form
                output += "</body></html>"
                self.wfile.write(output)
                return

            restaurants = session.query(Restaurant).all()
            print "restaurants query is: "
            pprint.pprint(restaurants)
            for restaurant in restaurants:
                print "self.path is...: ", self.path
                print "that string concat thing: ", "/restaurant/%s/edit" % restaurant.id
                if self.path.endswith("/restaurant/%s/edit" % restaurant.id):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = page_head
                    print "iterating throught restaurants..."
                    print restaurant.id, restaurant.name
                    output += edit_restaurant_form % restaurant.id
                    output += "</body></html>"
                    print "'output' for restaurant/id/edit is: ", output
                    self.wfile.write(output)
                    # pdb.set_trace()
                    return

        except:

            self.send_error(404,
                            " NOOOES! File not found! :(  %s" %  self.path
                            )

    def do_POST(self):

        try:
            self.send_response(301)
            self.end_headers()

            content_type, parameter_dictionary = cgi.parse_header( self.headers.getheader('content-type') )
            print "content_type is: ", content_type
            print "parameter_dictionary is: ", parameter_dictionary

            if content_type == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, parameter_dictionary)
                print "FORM POST! YAYS!"
                print "self.path is: ", self.path
                print "fields are: ", fields
                output = page_head

                if 'new restaurant name' in fields:
                    print 'new restaurant name!'
                    new_restaurant_name = fields.get('new restaurant name')
                    new_restaurant = Restaurant(name = new_restaurant_name[0])
                    print "session add!"
                    print session.add(new_restaurant)
                    session.commit()
                    output += "<h1> Restaurant Added! : </h1>"
                    output += "<h3> %s </h3>\n" % new_restaurant_name[0]
                    output += new_restaurant_form
                    output += "<a href='/restaurant'>return to listing</a>"
                    output += "</body></html>"

                if 'edited restaurant name' in fields:
                    print "edited restaurant name!"
                    edited_name = fields.get('edited restaurant name')[0]
                    restaurant_id = self.path.split('/')[2]
                    print "restaurant_id is: ", restaurant_id
                    result = session.execute("""
                            UPDATE restaurant
                            SET name=:edited_name
                            WHERE id=:edited_restaurant_id;
                        """,
                        {"edited_name": edited_name,
                        "edited_restaurant_id": restaurant_id}
                    )
                    print "result is: ", result
                    session.commit()
                    # pdb.set_trace()
                    output += "<h1> Restaurant Edited! : </h1>"
                    output += "<h3> %s </h3>\n" % edited_name
                    output += "<a href='/restaurant'>return to listing</a>"
                    output += "</body></html>"

            self.wfile.write(output)
            # print output

        except:
            pass

#main() code
def main():
    try:
        port = 8080
        server = HTTPServer( ('',port), webserverHandler )
        print "Yo, web server running on port %s !" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print " Righty ho, captain! Stopping web server... "
        server.socket.close()

# Run only when run as script, NOT when imported.
if __name__ == '__main__':
    main()
