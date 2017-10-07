from app.reports.models.report import Report


class PersonReport(Report):
    __DB_VIEW_NAME = "report/byPerson"

    def __init__(self, location=None, name=None):
        """Initializes new instance of PersonReport class."""
        db_options = self.__db_options(location=location, name=name)
        super().__init__(self.__DB_VIEW_NAME, db_options)

        self._rows.sort(key=lambda x: x["scores"], reverse=True)

    def _view(self, record):
        """Converts DB record to view."""
        view = super(PersonReport, self)._view(record)
        view["location"] = record["key"][0]
        view["name"] = record["key"][1]
        return view

    @staticmethod
    def __db_options(location=None, name=None):
        if not location and not name:
            return {"group_level": 2}
        if location and not name:
            return {"group": True, "group_level": 2, "startkey": [location, ""], "endkey": [location, "\uFFFF"]}
