from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required

from app.autocomplete import __get_date_by_name
from app.parser import parse
from app.validation import validate
from db import db

documents = Blueprint("admin/documents", __name__, template_folder=".")


@documents.route("/")
@login_required
def index():
    """Displays list of incoming documents."""
    f = db.view("document/all")  # fetch all the documents
    d = map(lambda x: __view(x.value), f)  # map each doc to view
    return render_template("ad_list.html", documents=d)


@documents.route("/<string:key>")
@login_required
def view(key):
    """Displays form to edit incoming document."""
    d = db["document/" + key]
    return render_template("ad_view.html", **__view(d))


@documents.route("/<string:key>/validate", methods=["POST"])
@login_required
def validate_doc(key):
    """Validates document."""
    j = request.get_json(force=True)
    d = db["document/" + key]

    d["location"] = j["location"]
    d["event"] = j["event"]
    d["report"] = j["report"]
    status = validate(d["report"])

    return jsonify(status)


@documents.route("/<string:key>/save", methods=["POST"])
@login_required
def save(key):
    """Saves changes."""
    j = request.get_json(force=True)
    d = db["document/" + key]

    d["location"] = j["location"]
    d["event"] = j["event"]
    d["report"] = j["report"]

    status = validate(d["report"])
    d["validation"] = status
    d["status"] = "valid" if status["isValid"] else "invalid"
    db.save(d)

    return jsonify(status)


@documents.route("/<string:key>/accept", methods=["POST"])
@login_required
def accept(key):
    """Creates report from document using key specified."""
    doc = db["document/" + key]
    is_valid = validate(doc["report"])["isValid"] is True

    if is_valid:
        doc["status"] = "accepted"
        db.save(doc)
        __save_report(key, doc)

    return jsonify({"status": is_valid})


@documents.route("/<string:key>/delete", methods=["POST"])
@login_required
def delete(key):
    doc = db["document/" + key]
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
        "key": key.replace("document/", ""),
        "event": doc.get("event", ""),
        "location": doc.get("location", ""),
        "name": doc.get("name", ""),
        "contacts": doc.get("contacts", ""),
        "report": doc.get("report", ""),
        "created": doc.get("created", ""),
        "validation": doc.get("validation", ""),
        "status": doc.get("status", "")
    }
