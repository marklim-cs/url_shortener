import os
from dotenv import load_dotenv
from flask import Flask, g
from src.controllers.short_url_controller import short_url_bp

app = Flask(__name__)
app.register_blueprint(short_url_bp)

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__=="__main__":
    app.run(debug=True)