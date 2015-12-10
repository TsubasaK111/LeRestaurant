from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DatabaseSession = sessionmaker(bind = engine)
session = DatabaseSession()


#handler code
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        try:

            if self.path.endswith("/supz"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html' )
                self.end_headers()

                output = "<html><body> SUP BROOOO </body><html>"
                self.wfile.write(output)
                print "output is: ", output
                return

            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html' )
                self.end_headers()

                output = "<html><body>"
                output += "<h1>The Franchise Manager</h1>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    print restaurant.name
                    output += "<h2> %s </h2>" % restaurant.name
                    output += "<a href="">edit</a> "
                    output += "<a href="">delete</a>"
                # output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What wouldja like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                print "output is: ", output
                return

        except:

            self.send_error(
                404,
                "NOOOES! File not found! :( %s" %  self.path
                )

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header( self.headers.getheader('content-type') )
            if ctype == 'multipart/form-data':
                fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What wouldja like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output
            # output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What wouldja like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"

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
