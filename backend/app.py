from http.server import HTTPServer, BaseHTTPRequestHandler

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("Hello from Effective Mobile!".encode('utf-8'))

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

hostName = "0.0.0.0"
serverPort = 8080

webServer = HTTPServer((hostName, serverPort), GetHandler)
print(f"Server started at http://{hostName}:{serverPort}")

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    print("Server stoping ...")

webServer.server_close()
print("Server stoped.")