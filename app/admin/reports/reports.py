from flask import Blueprint, jsonify, render_template
from flask_login import login_required

from app.autocomplete import __get_date_by_name
from app.parser import parse
from db import db

reports = Blueprint("admin/reports", __name__, template_folder=".")


@reports.route("/")
@login_required
def index():
    """Displays list of reports."""
    f = db.view("report/all")  # fetch all the reports
    r = map(lambda x: __view(x.value), f)  # map each doc to view
    return render_template("rpt_list.html", reports=r)


@reports.route("/<string:key>")
@login_required
def view(key):
    """Displays report."""
    d = db["report/" + key]
    return render_template("rpt_view.html", **__view(d))


@reports.route("/<string:key>/delete", methods=["POST"])
@login_required
def delete(key):
    doc = db["report/" + key]
    db.delete(doc)
    return jsonify({"status": "ok"})


def __save_report(key, doc):
    """Saves report using data from specified document."""
    rpt_id = "report/" + key
    rpt = db.get(rpt_id, {})  # get report or create new one
    rpt["_id"] = key
    rpt["location"] = doc["location"]
    rpt["event"] = doc["event"]
    rpt["date"] = __get_date_by_name(doc["event"])
    rpt["data"] = parse(doc["report"])
    db[rpt_id] = rpt


def __view(doc):
    """Converts document to view."""
    key = doc.get("id", None) or doc.get("_id", None)
    return {
        "key": key.replace("report/", ""),
        "event": doc.get("event", ""),
        "location": doc.get("location", ""),
        "date": doc.get("date", ""),
        "data": doc.get("data", "")
    }
