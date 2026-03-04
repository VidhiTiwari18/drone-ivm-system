from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_PATH = "backend/inventory.db"


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/table")
def table():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory ORDER BY id DESC")

    items = cursor.fetchall()

    conn.close()

    return render_template("table.html", items=items)


@app.route("/charts")
def charts():
    return render_template("charts.html")


@app.route("/inventory")
def inventory():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory ORDER BY id DESC")

    rows = cursor.fetchall()

    conn.close()

    return rows


if __name__ == "__main__":
    app.run(debug=True)