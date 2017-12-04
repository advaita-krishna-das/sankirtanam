from app.reports.models.report import Report


class EventOverallReport(Report):
    __DB_VIEW_NAME = "report/byEventOverall"

    def __init__(self):
        """Initializes new instance of EventReport class."""
        db_options = self.__db_options()
        super().__init__(self.__DB_VIEW_NAME, db_options)
        self._rows.sort(key=lambda x: x["scores"], reverse=True)

    def _view(self, record):
        """Converts DB record to view."""
        view = super(EventOverallReport, self)._view(record)
        view["event"] = record["key"][0]
        return view

    @staticmethod
    def __db_options():
        return {"group": True, "group_level": 1}
