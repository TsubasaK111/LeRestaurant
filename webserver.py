from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


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
        <input name = 'restaurant name' type = 'text' >
        <input type = 'submit' value = 'Submit'>
    </form>
"""


#request handler code
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        try:

            if self.path.endswith("/supz"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html' )
                self.end_headers()

                output = page_head
                output += "SUP BROOOO </body><html>"
                self.wfile.write(output)
                print "output is: ", output
                return

            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html' )
                self.end_headers()

                output = page_head
                output += "<h1>The Franchise Manager</h1>\n"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    print restaurant.name
                    output += """<h2> %s </h2>
                                 <a href="">edit</a> "
                                 <a href="">delete</a>
                              """ % restaurant.name
                output += new_restaurant_form
                output += "</body></html>"

                self.wfile.write(output)
                print "output is: ", output
                return

            # if self.path.endswith("/restaurant/new"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_header()
            #
            #     output = "<html><body>"
            #     output += "<form method = 'POST' "
            #     output += "enctype = 'multipart/form-data' "
            #     output += "action = '/new'>"
            #     output += "<h1>Add A New Restaurant!</h1>"
            #     output += "<input name = 'message' type = 'text' >"
            #     output += "<input type = 'submit' value = 'Submit'>"
            #     output += "</form>"

        except:

            self.send_error(
                404,
                "NOOOES! File not found! :( %s" %  self.path
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
                new_restaurant_name = fields.get('restaurant name')
                new_restaurant = Restaurant(name = new_restaurant_name[0])
                session.add(new_restaurant)
                session.commit()
                output = page_head
                output += "<h1> Restaurant Added! : </h1>"
                output += "<h3> %s </h3>\n" % new_restaurant_name[0]
                output += new_restaurant_form
                output += "<a href='/restaurant'>return to listing</a>"
                output += "</body></html>"

            self.wfile.write(output)
            print output

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
        print "Righty ho, captain! Stopping web server..."
        server.socket.close()

# Run only when run as script, NOT when imported.
if __name__ == '__main__':
    main()
