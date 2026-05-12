from datetime import date

# Reference Indian holiday calendar.
# You can edit this list every year based on your company policy.
INDIAN_HOLIDAYS_2026 = {
    date(2026, 1, 1): "New Year",
    date(2026, 1, 14): "Makar Sankranti / Pongal",
    date(2026, 1, 26): "Republic Day",
    date(2026, 3, 3): "Holi",
    date(2026, 3, 20): "Ugadi / Gudi Padwa",
    date(2026, 3, 27): "Good Friday",
    date(2026, 3, 31): "Eid-ul-Fitr",
    date(2026, 5, 1): "May Day",
    date(2026, 8, 15): "Independence Day",
    date(2026, 8, 28): "Onam",
    date(2026, 9, 4): "Janmashtami",
    date(2026, 10, 2): "Gandhi Jayanti",
    date(2026, 10, 20): "Dussehra",
    date(2026, 11, 8): "Diwali",
    date(2026, 12, 25): "Christmas",
}


def is_weekend(day: date) -> bool:
    return day.weekday() in (5, 6)  # Saturday=5, Sunday=6


def get_holiday_name(day: date):
    return INDIAN_HOLIDAYS_2026.get(day)


def is_non_working_day(day: date):
    if is_weekend(day):
        return True, "Weekend"
    holiday = get_holiday_name(day)
    if holiday:
        return True, holiday
    return False, None
