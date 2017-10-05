import uuid
from datetime import date

from flask import Blueprint, render_template, request, jsonify

from app.validation import validate
from db import db

reception = Blueprint("reception", __name__, template_folder=".")


@reception.route("/")
def index():
    """Index page of reception. User can send own document from this page."""
    return render_template("reception.html")


@reception.route("/accept", methods=["POST"])
def accept():
    """Accepts document been sent by client."""
    key = "document/" + uuid.uuid4().hex  # generate new id for document

    data = request.get_json(force=True)
    data["_id"] = key  # save document with generated key
    data["created"] = date.today().strftime("%Y/%m/%d")
    data["validation"] = validate(data["report"])  # save validation data too
    data["status"] = "valid" if data["validation"]["isValid"] else "invalid"
    db.save(data)

    return jsonify({"status": "ok"})
