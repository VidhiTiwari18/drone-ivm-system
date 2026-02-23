from flask import Flask, request, jsonify   # Flask for backend, request to read data, jsonify to send JSON
from flask_cors import CORS                 # Allows frontend / other programs to access backend
import sqlite3                              # SQLite database
from datetime import datetime               # To store date and time

app = Flask(__name__)                       # Create Flask app
CORS(app)                                  # Enable CORS for all routes

DB_PATH = "backend/inventory.db"            # Database file path

# Create database and table if not already present
def init_db():
    conn = sqlite3.connect(DB_PATH)         # Connect to database (creates file if not exists)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY AUTOINCREMENT, item_id TEXT, timestamp TEXT)"
    )
    conn.commit()                           # Save changes
    conn.close()                            # Close database connection

init_db()                                   # Run once when server starts

# API to add a new inventory item
@app.route("/add_item", methods=["POST"])
def add_item():
    data = request.get_json()               # Read JSON data from request
    item_id = data.get("item_id")           # Extract item_id

    if item_id is None:                     # Validation check
        return jsonify({"error": "item_id required"}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO inventory (item_id, timestamp) VALUES (?, ?)",
        (item_id, timestamp)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "added", "item": item_id})  # Response after insertion

# API to fetch all inventory data
@app.route("/inventory", methods=["GET"])
def inventory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory ORDER BY id DESC")  # Latest entries first
    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows)            # Send data to frontend

# Start the backend server
if __name__ == "__main__":
    app.run(debug=True)