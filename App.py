from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from utils.Performance import calculate_performance

app = Flask(__name__)

# DATABASE
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS interns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        domain TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# ROUTES
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        domain = request.form["domain"]

        conn = get_db()
        conn.execute("INSERT INTO interns (name,email,domain) VALUES (?,?,?)",
                     (name,email,domain))
        conn.commit()
        conn.close()

        return redirect("/interns")

    return render_template("add_intern.html")

@app.route("/interns")
def interns():
    conn = get_db()
    data = conn.execute("SELECT * FROM interns").fetchall()
    conn.close()
    return render_template("view_intern.html", interns=data)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM interns WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/interns")

@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    conn = get_db()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        domain = request.form["domain"]

        conn.execute("UPDATE interns SET name=?, email=?, domain=? WHERE id=?",
                     (name,email,domain,id))
        conn.commit()
        conn.close()
        return redirect("/interns")

    intern = conn.execute("SELECT * FROM interns WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit_intern.html", intern=intern)

# API
@app.route("/api/interns")
def api():
    conn = get_db()
    data = conn.execute("SELECT * FROM interns").fetchall()
    conn.close()
    return jsonify([dict(x) for x in data])

if __name__ == "__main__":
    app.run(debug=True)