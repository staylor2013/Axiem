from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):

    # Handle browser opening http://localhost:8000/
    def do_GET(self):
        if self.path == "/":
            try:
                import os

                path = os.path.join(os.getcwd(), "index.html")
                print("Trying to load:", path)

                with open(path, "rb") as f:
                    content = f.read()

                print("File size:", len(content))

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content)

            except Exception as e:
                print("ERROR:", e)
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())

    # Handle frontend POST requests
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body) if body else {}
        except:
            data = {}

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Data received successfully"}).encode())

        try:
            data = json.loads(body) if body else {}
        except:
            data = {}

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Data received successfully"}).encode())

server = HTTPServer(("0.0.0.0", 1234), Handler)
print("Server running at http://localhost:1234/")
server.serve_forever()