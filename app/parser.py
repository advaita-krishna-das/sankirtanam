from bs4 import BeautifulSoup


def parse(html):
    parser = BeautifulSoup(html, "html5lib")
    tables = parser.select("table")
    if len(tables) != 1:
        return None

    rows = parser.table.find_all("tr")  # gets all rows from table

    def _pc(cell):
        value = str.join("", cell.stripped_strings)
        if value.isnumeric():
            return int(value)
        return value

    def _pr(row):
        return list(map(lambda y: _pc(y), row.find_all("td")))

    return list(map(lambda row: _pr(row), rows))
