from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading


class _MidasServlet(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(
            "<html><head><title>Midas</title></head>" +
            ("<p>Request: %s</p>" % self.path) +
            "<body>" +
            "<p>This is an example web server.</p>" +
            "</body></html>", "utf-8"))



class MidasServer:
    def __init__(self, hostName="localhost", serverPort=8080):
        self.hostName = hostName
        self.serverPort = serverPort
        self.webServer = HTTPServer((hostName, serverPort), _MidasServlet)
        self.thread = None

    def run_in_background(self):
        if not self.thread:
            self.thread = threading.Thread(target=lambda : self.run())
            self.thread.start()
        return self

    def stop(self):
        if self.thread:
            self.webServer.shutdown()
            self.thread.join()

    def run(self):
        print("Starting server http://%s:%s" % (self.hostName, self.serverPort))

        try:
            self.webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        self.webServer.server_close()
        print("Server http://%s:%s stopped." % (self.hostName, self.serverPort))

        