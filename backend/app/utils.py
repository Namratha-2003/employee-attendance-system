from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


def now_ist() -> datetime:
    """Return current Indian Standard Time as timezone-naive datetime for DB storage."""
    return datetime.now(IST).replace(tzinfo=None)


def today_ist():
    return now_ist().date()


def format_date_indian(value) -> str:
    if not value:
        return ""
    return value.strftime("%d-%m-%Y")


def format_datetime_indian(value) -> str:
    if not value:
        return ""
    return value.strftime("%d-%m-%Y %I:%M:%S %p")
