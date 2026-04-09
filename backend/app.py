from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "secret123"

# database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "inventory.db")


# login page
@app.route("/")
def login():
    return render_template("login.html")


# login check
@app.route("/login", methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    if username == "vidhi logistic" and password == "grant acess":
        session["user"] = username
        return redirect("/dashboard")
    else:
        return render_template("login.html", error="Invalid username or password")


#dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")


# table page
@app.route("/table")
def table():
    if "user" not in session:
        return redirect("/")
    return render_template("table.html")


# charts page
@app.route("/charts")
def charts():
    if "user" not in session:
        return redirect("/")
    return render_template("charts.html")


# logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# inventory api (get data)
@app.route("/inventory")
def get_inventory():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM inventory")
        data = cursor.fetchall()

        conn.close()
        return jsonify(data)

    except Exception as e:
        return {"error": str(e)}


# add item api (from yolo/scanner)
@app.route("/add_item", methods=["POST"])
def add_item():
    try:
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

    except Exception as e:
        return {"error": str(e)}


# run app
if __name__ == "__main__":
    app.run(debug=True)