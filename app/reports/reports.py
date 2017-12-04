from flask import Blueprint, render_template

from app.reports.models import LocationReport
from app.reports.models.event import EventReport
from app.reports.models.event_overall import EventOverallReport
from app.reports.models.person import PersonReport

reports = Blueprint("reports", __name__, template_folder="./templates")


@reports.route("/overall")
def reports_overall():
    """Overall report."""
    return render_template("rpt_overall.html",
                           locations_report=LocationReport(kind=LocationReport.OVERALL),
                           persons_report=PersonReport())


@reports.route("/location")
def reports_locations():
    """Report for all locations."""
    return render_template("rpt_all_locations.html",
                           report=LocationReport())


@reports.route("/location/<string:location>")
def reports_location(location):
    """Index page of reports."""
    return render_template("rpt_location.html",
                           report=LocationReport(location=location),
                           persons=PersonReport(location=location))


@reports.route("/event")
def reports_events():
    """Index page of reports."""
    return render_template("rpt_events.html",
                           report=EventOverallReport())


@reports.route("/event/<string:event>")
def reports_event(event):
    """Index page of reports."""
    return render_template("rpt_event.html",
                           report=EventReport(event=event))
