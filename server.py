from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Axiem Works 🔥</h1>
    <p>Your Render deployment is alive.</p>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
