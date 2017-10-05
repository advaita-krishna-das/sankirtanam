from flask import Blueprint, render_template

from db import db

admin = Blueprint("admin", __name__, template_folder=".")


@admin.app_template_global(name="incoming_count")
def incoming_count():
    f = db.view("document/count", group=True, group_level=0)
    r = list(f)
    return r[0].value if r else 0


@admin.route("/")
def index():
    return render_template("a_index.html")
