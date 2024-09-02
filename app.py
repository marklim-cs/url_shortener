import random 
import string
import sqlite3
import os
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, request, session, g
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_table():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY, long_url TEXT UNIQUE, short_url TEXT UNIQUE)''')
    db.commit()
    db.close()

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/short", methods=["POST", "GET"])
def short():
    db = get_db()
    if "short" not in session:
        session["short"] = []

    #POST
    if request.method == "POST":
        long_url = request.form.get("long_url")
        short_url = generate_short_url()
        if long_url:
            db.execute("INSERT INTO urls (url, short_url) VALUES (?, ?)", (long_url, short_url))
            db.commit()
            session["short"].append(short_url)
            return redirect("short")

    #GET
    urls = []
    for shorts in session["short"]:
        current_url = db.execute("SELECT * FROM urls WHERE id = ?", (shorts,)).fetchone()
    if current_url:
        urls.append(current_url)
    return render_template("short.html", urls=urls)



if __name__=="__main__":
    app.run()