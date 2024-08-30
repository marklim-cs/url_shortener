import random 
import string
import sqlite3
import os
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, url_for, request, session, g
from flask_session import Session

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