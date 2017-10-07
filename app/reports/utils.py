import datetime

from dateutil.rrule import rrule, MONTHLY


def months_between(min_year, max_year):
    start_date = datetime.date(min_year, 1, 1)
    end_date = datetime.date(max_year, 12, 31)
    dates = [dt for dt in rrule(MONTHLY, dtstart=start_date, until=end_date)]
    return dates


def min_and_max(list):
    return min(list), max(list)
