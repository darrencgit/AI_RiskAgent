from flask import Flask, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("articles.db")
    conn.row_factory = sqlite3.Row  # Returns rows as dictionaries
    return conn

@app.route("/summaries/<period>", methods=["GET"])
def get_summaries(period):
    conn = get_db_connection()
    c = conn.cursor()

    # Define time range
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
