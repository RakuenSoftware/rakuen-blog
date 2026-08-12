"""Shared date helpers."""
import calendar
import datetime

def end_of_month(d: datetime.date) -> datetime.date:
    return d.replace(day=calendar.monthrange(d.year, d.month)[1])

def days_between(a: datetime.date, b: datetime.date) -> int:
    return (b - a).days
