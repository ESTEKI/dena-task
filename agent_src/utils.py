from datetime import datetime
from dateutil.relativedelta import relativedelta


def calculate_date_offset(time_window: dict) -> dict:
    """
    Subtracts the specified days/months/years from today's date.
    note that the month lengh are not equal and we are using relativedelta to handle this issue.
    Example:
    {"days": 14, "months": 1, "years": 0}
    """

    now = datetime.now()

    result = now - relativedelta(
        years=time_window.get("years", 0),
        months=time_window.get("months", 0),
        days=time_window.get("days", 0),
    )

    return {
        "day": result.day,
        "month": result.month,
        "year": result.year,
    }