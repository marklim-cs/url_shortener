from flask import Blueprint, render_template, request, redirect
import validators
from src.utils.generate_short_string import generate_short_string
from src.services.short_url_services import get_short_url, get_long_url

short_url_bp = Blueprint("short_url_bp", __name__)

@short_url_bp.route("/")
def index():
    return render_template("index.html")

@short_url_bp.route("/short", methods=["POST"])
def short():
    long_url = request.form.get("long_url")

    if not validators.url(long_url):
        return render_template("invalid_url.html")

    short_url = generate_short_string()

    return get_short_url(long_url, short_url)

@short_url_bp.route("/<short_url>")
def redirect_to_long_url(short_url):
    result = get_long_url(short_url)
    if result:
        long_url = result[0]
        return redirect(long_url)
    else:
        return redirect("/not_found.html")