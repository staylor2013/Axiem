from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

# Render gives the app a port automatically
PORT = int(os.environ.get("PORT", 10000))


class Handler(BaseHTTPRequestHandler):

    # ---------------------------
    # GET requests
    # ---------------------------
    def do_GET(self):

        # Homepage
        if self.path == "/":
            try:
                path = os.path.join(os.getcwd(), "index.html")

                with open(path, "rb") as f:
                    content = f.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()

                self.wfile.write(content)

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()

                self.wfile.write(str(e).encode())

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()

            self.wfile.write(b"404 Not Found")

    # ---------------------------
    # POST requests
    # ---------------------------
    def do_POST(self):

        # Read request body
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        # Convert JSON -> Python dict
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}

        # Example responses
        if self.path == "/register":

            response = {
                "message": "Registered successfully",
                "received": data
            }

        elif self.path == "/login":

            response = {
                "message": "Logged in successfully",
                "received": data
            }

        else:

            response = {
                "message": "Unknown endpoint"
            }

        # Send response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())


# ---------------------------
# Start server
# ---------------------------
server = HTTPServer(("0.0.0.0", PORT), Handler)

print(f"Server running on port {PORT}")

server.serve_forever()
