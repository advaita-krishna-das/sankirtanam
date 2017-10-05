from db import db


def query(view, map_func=None, sort_func=None, reverse=False, count=None, **kwargs):
    options = {k: v for k, v in kwargs.items() if v is not None}
    result = db.view(view, **options)

    if map_func:
        result = map(lambda x: map_func(x), result)
    if sort_func:
        result = sorted(result, key=sort_func, reverse=reverse)
    if count:
        result = result[:count]
    return list(result)


def by_location(count=None, group_level=1, start=None, end=None, sort_func=None, reverse=False):
    def __map(x):
        z = __view(x)
        z["name"] = x["key"][0]
        if len(x["key"]) >= 2:
            z["year"] = x["key"][1]
        if len(x["key"]) >= 3:
            z["month"] = x["key"][2]
        return z

    sf = lambda x: x["scores"]
    if sort_func:
        sf = sort_func

    return query("report/byLocation",
                 group=True, group_level=group_level,
                 startkey=start, endkey=end,
                 map_func=__map, sort_func=sf,
                 reverse=reverse, count=count)


def top_persons(count=15):
    def __map(x):
        z = __view(x)
        z["name"] = x["key"][0]
        z["location"] = x["key"][1]
        return z

    r = db.view("report/byPerson", group=True, group_level=2)  # fetch all the records
    v = map(lambda x: __map(x), r)  # map each doc to view
    s = sorted(v, key=lambda x: x["scores"], reverse=True)  # sort by scores
    return s[:count]  # get top 15 elements


def __view(record):
    return {
        "key": record.key,
        "huge": record.value[0],
        "big": record.value[1],
        "medium": record.value[2],
        "small": record.value[3],
        "books": __books(record.value),
        "scores": __scores(record.value),
    }


def __books(record):
    return record[0] + record[1] + record[2] + record[3]


def __scores(record):
    return 2 * record[0] + 1 * record[1] + 0.5 * record[2] + 0.25 * record[3]
