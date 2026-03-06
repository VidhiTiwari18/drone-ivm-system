from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database path
DB_PATH = "backend/inventory.db"

# Login Page
@app.route("/")
def login():
    return render_template("login.html")

# Dashboard Page
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Table Page
@app.route("/table")
def table():
    return render_template("table.html")

# Charts Page
@app.route("/charts")
def charts():
    return render_template("charts.html")

# API: Get Inventory Data
@app.route("/inventory")
def inventory():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)

# API: Add Item (Scanner)
@app.route("/add_item", methods=["POST"])
def add_item():

    data = request.json
    item_id = data["item_id"]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO inventory (item_id, timestamp) VALUES (?, ?)",
        (item_id, timestamp)
    )

    conn.commit()
    conn.close()

    return {"status": "success"}

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)