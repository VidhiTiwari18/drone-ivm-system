from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime

# Create Flask application object
app = Flask(__name__)

# Allow frontend / other programs to access backend APIs
CORS(app)

# Path where SQLite database file will be stored
DB_PATH = "backend/inventory.db"

# This function runs once when server starts
# It makes sure database and table exist
def init_db():
    conn = sqlite3.connect(DB_PATH)   # Connect to database file
    cursor = conn.cursor()            # Cursor is used to run SQL queries
    
    # Create inventory table if it is not already created 
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS inventory ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "item_id TEXT, "
        "timestamp TEXT)"
    )
    
    conn.commit()   # Save changes permanently
    conn.close()    # Close database connection

# Initialize database when app starts
init_db()

# Website route
# This runs when user opens http://127.0.0.1:5000/
# It loads index.html from templates folder
@app.route("/")
def home():
    return render_template("index.html")

# API to add inventory item
# This API is called by scanner / app / frontend
@app.route("/add_item", methods=["POST"])
def add_item():
    # Read JSON data sent to backend
    data = request.get_json()
    item_id = data.get("item_id")

    # If item_id is missing, return error
    if item_id is None:
        return jsonify({"error": "item_id required"}), 400

    # Get current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store data in database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO inventory (item_id, timestamp) VALUES (?, ?)",
        (item_id, timestamp)
    )
    conn.commit()
    conn.close()

    # Send success response
    return jsonify({
        "status": "added",
        "item": item_id
    })

# API to fetch inventory data
# This API is used by website to display inventory
@app.route("/inventory", methods=["GET"])
def inventory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all inventory records (latest first)
    cursor.execute("SELECT * FROM inventory ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    # Return data in JSON format
    return jsonify(rows)

# Start Flask server
# This runs only when file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
    