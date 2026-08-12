"""Shared date helper. Used by billing, reports, scheduler, and invoices."""
import calendar
import datetime


def end_of_month(d: datetime.date) -> datetime.date:
    last_day = calendar.monthrange(d.year, d.month)[1]
    return d.replace(day=last_day)


def days_between(a: datetime.date, b: datetime.date) -> int:
    return (b - a).days
