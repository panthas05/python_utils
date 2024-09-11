from datetime import date


def get_next_month_first_day() -> date:
    """
    Returns the first day of the next month as a date instance
    """
    today = date.today()
    if today.month == 12:
        return today.replace(
            year=today.year + 1,
            month=1,
            day=1,
        )
    else:
        return today.replace(
            month=today.month + 1,
            day=1,
        )
