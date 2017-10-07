from app.queries import query


class Report:
    def __init__(self, view, db_options):
        self.__db_view_name = view
        self.__db_options = db_options
        self._rows = list(map(
            lambda x: self._view(x),
            self.__fetch()))

    @property
    def rows(self):
        return self._rows

    def __fetch(self):
        return query(self.__db_view_name, **self.__db_options)

    def _view(self, record):
        return {
            "key": record.key,
            "huge": record.value[0],
            "big": record.value[1],
            "medium": record.value[2],
            "small": record.value[3],
            "books": self.__books(record.value),
            "scores": self.__scores(record.value),
        }

    @staticmethod
    def __books(record):
        return record[0] + record[1] + record[2] + record[3]

    @staticmethod
    def __scores(record):
        return 2 * record[0] + 1 * record[1] + 0.5 * record[2] + 0.25 * record[3]