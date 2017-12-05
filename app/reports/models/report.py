from app.queries import query


class Report:
    def __init__(self, view, db_options, books_offset=0):
        self.__db_view_name = view
        self.__db_options = db_options
        self._books_offset = books_offset
        self._rows = list(map(
            lambda x: self._view(x),
            self.__fetch()))

    @property
    def rows(self):
        return self._rows

    def __fetch(self):
        return query(self.__db_view_name, **self.__db_options)

    def _view(self, record):
        bo = self._books_offset
        return {
            "key": record.key,
            "huge": record.value[bo+0],
            "big": record.value[bo+1],
            "medium": record.value[bo+2],
            "small": record.value[bo+3],
            "books": self._books(record.value),
            "scores": self._scores(record.value),
        }

    def _books(self, record):
        bo = self._books_offset
        return record[bo+0] + record[bo+1] + record[bo+2] + record[bo+3]

    def _scores(self, record):
        bo = self._books_offset
        return 2 * record[bo+0] + 1 * record[bo+1] + 0.5 * record[bo+2] + 0.25 * record[bo+3]