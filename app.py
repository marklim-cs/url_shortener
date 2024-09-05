import random
import string
import sqlite3
import os
from dotenv import load_dotenv
import validators

from flask import Flask, render_template, redirect, request, g

app = Flask(__name__)

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

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/short", methods=["POST"])
def short():
    db = get_db()

    #POST
    long_url = request.form.get("long_url")
    if not validators.url(long_url):
        return render_template("invalid_url.html")

    short_url = generate_short_url()
    if long_url:
        try:
            db.execute(
                    "INSERT INTO urls (long_url, short_url) VALUES (?, ?)",
                    (long_url, short_url)
                    )
            db.commit()
            return render_template("short.html", long_url=long_url,
                                    short_url=short_url, url_root=request.url_root
                                    )

        # long_url exists in db
        except sqlite3.IntegrityError:
            result = db.execute(
                "SELECT short_url FROM urls WHERE long_url=?", 
                (long_url, )).fetchone()

            if result:
                short_url = result[0]
                return render_template("short.html", long_url=long_url,
                                        short_url=short_url, url_root=request.url_root
                                        )
            else:
                return "An unexpected error occured!", 500


@app.route("/<short_url>")
def redirect_to_long_url(short_url):
    db = get_db()
    result = db.execute("SELECT long_url FROM urls WHERE short_url=?", (short_url, )).fetchone()
    if result:
        long_url = result[0]
        db.close()
        return redirect(long_url)
    else:
        db.close()
        return redirect("/not_found.html")

if __name__=="__main__":
    app.run(debug=True)