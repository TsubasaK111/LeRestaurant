from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


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
        except:
            self.send_error(
                404,
                "NOOOES! File not found! :( %s" %  self.path
                )

#main() code
def main():
    try:
        port = 8080
        server = HTTPServer( ('',port), webserverHandler )
        print "Yo, web server running on port %s !" % port
        server.serve_forever()

    except KeyboardImterrupt:
        print "Righty ho, captain! Stopping web server..."
        server.socket.close()

# Run only when run as script, NOT when imported.
if __name__ == '__main__':
    main()
