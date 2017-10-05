from flask import Blueprint, render_template

from app.queries import by_location, top_persons

reports = Blueprint("reports", __name__, template_folder=".")


@reports.route("/")
def index():
    """Index page of reports."""
    l = by_location()
    p = top_persons(count=15)
    return render_template("reports.html", locations=l, persons=p)


@reports.route("/location/<string:name>")
def location(name):
    """Index page of reports."""
    l = by_location(group_level=3, start=[name, 0, 0], end=[name, 9999, 9999],
                    sort_func=lambda x: [x["year"], x["month"]], reverse=False)
    labels = map(lambda x: "{}/{}".format(x["year"], x["month"]), l)
    values = map(lambda x: x["scores"], l)

    return render_template("location.html", data=l, labels=list(labels), values=list(values), name=name)
