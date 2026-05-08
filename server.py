from flask import Flask, send_file, request, jsonify
import os

app = Flask(__name__)


# -----------------------------
# Homepage
# -----------------------------
@app.route("/")
def home():
    return send_file("index.html")


# -----------------------------
# Register endpoint
# -----------------------------
@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    return jsonify({
        "message": "Registered successfully",
        "received": data
    })


# -----------------------------
# Login endpoint
# -----------------------------
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    return jsonify({
        "message": "Logged in successfully",
        "received": data
    })


# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
