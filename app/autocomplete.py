from datetime import date
from flask import Blueprint, request, jsonify

from db import db

autocomplete = Blueprint("autocomplete", __name__)


@autocomplete.route("/locations")
def locations():
    """Provides list of locations to autocomplete based on 'term' argument specified."""
    term = request.args.get("term")
    fetched = db.view("location/name", startkey=term, endkey=term+"\uFFFF")
    names = map(lambda l: l.key, fetched)
    return jsonify(list(names))


@autocomplete.route("/events")
def events():
    """Provides list of events to autocomplete based on 'term' argument specified."""
    term = request.args.get("term")
    year = date.today().year
    fetched = map(lambda x: x["name"], __generate_events(year))
    filtered = filter(lambda n: term in n, fetched)
    return jsonify(list(filtered))


def __generate_events(end_year, start_year=2015):
    names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
             "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    return [{
        "name": "{} {}".format(x, y),
        "date": [y, i + 1]}
        for i, x in enumerate(names)
        for y in range(start_year, end_year+1)
    ]


def __get_date_by_name(name):
    vals = __generate_events(2019)
    evnt = dict((v["name"], v["date"]) for v in vals)
    return evnt.get(name, None)
