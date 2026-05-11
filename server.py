from flask import Flask, send_file, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# =========================
# CREATE DATABASE
# =========================

with sqlite3.connect("data.db") as conn:
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return send_file("index.html")


@app.route("/forum")
def forum():
    return send_file("forum.html")


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Fill in all fields"
        })

    try:
        with sqlite3.connect("data.db", timeout=5) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

            conn.commit()

        return jsonify({
            "success": True,
            "message": "Registered successfully"
        })

    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "message": "Username already exists"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    with sqlite3.connect("data.db", timeout=5) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()

    if user:
        return jsonify({
            "success": True,
            "message": "Login successful"
        })

    else:
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        })


# =========================
# START SERVER
# =========================

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
