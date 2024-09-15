import sqlite3
from flask import render_template, request
from src.db.get_sqlite_db import get_db

def get_short_url(long_url, short_url):
    db = get_db()

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

def get_long_url(short_url):
    db = get_db()
    result = db.execute("SELECT long_url FROM urls WHERE short_url=?", (short_url, )).fetchone()
    db.close()
    return result