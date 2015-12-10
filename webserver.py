from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

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

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html' )
                self.end_headers()

                output = "<html><body> &#161HOLA SENOR! <a href='/supz'>Return to SUPZ</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What wouldja like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
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
