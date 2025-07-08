from flask import Flask, jsonify, send_from_directory
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__, static_folder="static")

def get_db_connection():
    conn = sqlite3.connect("articles.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/summaries/<period>", methods=["GET"])
def get_summaries(period):
    conn = get_db_connection()
    c = conn.cursor()
    if period == "weekly":
        date_limit = datetime.now() - timedelta(days=7)
    elif period == "monthly":
        date_limit = datetime.now() - timedelta(days=30)
    elif period == "quarterly":
        date_limit = datetime.now() - timedelta(days=90)
    else:
        return jsonify({"error": "Invalid period"}), 400
    c.execute("SELECT * FROM articles WHERE pub_date > ? ORDER BY pub_date DESC", (date_limit,))
    articles = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify({"articles": articles})

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
