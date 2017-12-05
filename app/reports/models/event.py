from app.reports.models.report import Report


class EventReport(Report):
    __DB_VIEW_NAME = "report/byEvent"

    def __init__(self, event):
        """Initializes new instance of EventReport class."""
        db_options = self.__db_options(event=event)
        super().__init__(self.__DB_VIEW_NAME, db_options, books_offset=1)
        self.__event = event
        self._rows.sort(key=lambda x: x["scores"] or x["count"], reverse=True)

    @property
    def event(self):
        return self.__event

    def _view(self, record):
        """Converts DB record to view."""
        view = super(EventReport, self)._view(record)
        view["event"] = record["key"][0]
        view["location"] = record["key"][1]
        view["name"] = record["value"][0]
        view["details"] = record["value"][5:]
        view["count"] = sum(record["value"][5:])
        return view

    @staticmethod
    def __db_options(event):
        return {"startkey": [event, ""], "endkey": [event, "\uFFFF"]}
