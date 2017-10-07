from more_itertools import unique_everseen

from app.reports.models.report import Report
from app.reports.utils import months_between


class LocationReport(Report):
    __DB_VIEW_NAME = "report/byLocation"
    OVERALL = 1
    BY_YEAR = 2
    BY_MONTHS = 3

    def __init__(self, location=None, kind=None):
        """Initializes new instance of LocationReport class."""
        self.__kind = kind or (self.BY_YEAR if location is None else self.BY_MONTHS)
        db_options = self.__db_options(self.__kind, name=location)
        super().__init__(self.__DB_VIEW_NAME, db_options)

        self.__location = location
        self.__scores = self.__calculate_scores()
        self.__overall = self.__calculate_overall()

        self._rows.sort(key=lambda x: x["scores"], reverse=True)

    @property
    def location(self):
        """Returns name of location if report created for specific location."""
        return self.__location

    @property
    def years(self):
        """Returns list of years present in report."""
        return sorted(unique_everseen([r["year"] for r in self._rows]))

    @property
    def locations(self):
        """Returns list of locations present in report."""
        return unique_everseen([r["location"] for r in self._rows])

    @property
    def chart(self):
        """Returns data for chart."""
        months = months_between(min(self.years), max(self.years))
        chart_labels = list(map(lambda x: "{}/{}".format(x.year, x.month), months))
        chart_values = [self.scores(d.year, d.month) for d in months]
        return chart_labels, chart_values

    def scores(self, key1, key2):
        """Returns scores using specified keys (depends on type of report).
        If name of location is not specified: key1 = location, key2 = year.
        If name of location is specified: key1 = year, key2 = month."""
        return self.__scores.get((key1, key2), 0)

    def overall_scores(self, key):
        """Returns overall scores for specified key (location or year)."""
        return self.__overall.get((key, "scores"), 0)

    def overall_books(self, key):
        """Returns overall books for specified location (location or year)."""
        return self.__overall.get((key, "books"), 0)

    def _view(self, record):
        """Converts DB record to view."""
        view = super(LocationReport, self)._view(record)
        view["location"] = record["key"][0]
        if len(record["key"]) >= 2:
            view["year"] = record["key"][1]
        if len(record["key"]) >= 3:
            view["month"] = record["key"][2]

        view["scores_map"] = \
            (view["location"]) if self.__kind == 1 else \
            (view["location"], view["year"]) if self.__kind == 2 else \
            (view["year"], view["month"])

        return view

    def __calculate_scores(self):
        """Calculates scores."""
        return {
            key: value.get("scores", 0) for (key, value) in
            map(lambda x: (x["scores_map"], x), self._rows)
        }

    def __calculate_overall(self):
        """Calculates overall scores/books."""
        overall = {}
        for r in self._rows:
            if (r["location"], "scores") not in overall:
                overall[(r["location"], "scores")] = 0
                overall[(r["location"], "books")] = 0
            overall[(r["location"], "scores")] += r["scores"]
            overall[(r["location"], "books")] += r["books"]

            if self.__kind is not self.OVERALL:
                if (r["year"], "scores") not in overall:
                    overall[(r["year"], "scores")] = 0
                    overall[(r["year"], "books")] = 0
                overall[(r["year"], "scores")] += r["scores"]
                overall[(r["year"], "books")] += r["books"]

        return overall

    @staticmethod
    def __db_options(kind, name=None):
        if kind == 1:
            return {"group": True, "group_level": 1}
        if kind == 2:
            return {"group": True, "group_level": 2}
        elif kind == 3:
            return {"group": True, "group_level": 3, "startkey": [name, 0, 0], "endkey": [name, 9999, 9999]}
