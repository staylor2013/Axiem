from flask import Flask, send_file, request, jsonify
import os
import json

app = Flask(__name__)

DB_FILE = "data.json"


# ---------------------------------
# Create database file if missing
# ---------------------------------
if not os.path.exists(DB_FILE):

    with open(DB_FILE, "w") as f:
        json.dump({"users": []}, f)


# ---------------------------------
# Load database
# ---------------------------------
def load_db():

    with open(DB_FILE, "r") as f:
        return json.load(f)


# ---------------------------------
# Save database
# ---------------------------------
def save_db(data):

    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------------------------------
# Homepage
# ---------------------------------
@app.route("/")
def home():

    return send_file("index.html")


# ---------------------------------
# Register
# ---------------------------------
@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    db = load_db()

    # Check if user exists
    for user in db["users"]:

        if user["username"] == username:

            return jsonify({
                "success": False,
                "message": "Username already exists"
            })

    # Add user
    db["users"].append({
        "username": username,
        "password": password
    })

    save_db(db)

    return jsonify({
        "success": True,
        "message": "Registered successfully"
    })


# ---------------------------------
# Login
# ---------------------------------
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    db = load_db()

    for user in db["users"]:

        if (
            user["username"] == username
            and
            user["password"] == password
        ):

            return jsonify({
                "success": True,
                "message": "Login successful"
            })

    return jsonify({
        "success": False,
        "message": "Invalid username or password"
    })


# ---------------------------------
# Run server
# ---------------------------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
