from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests

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
#def call_database_api(search_criteria, time_window):

def call_database_api(search_criteria):
    url = "http://127.0.0.1:8008/search"
    
    payload = search_criteria
    # {
    #     "search_criteria": search_criteria,
    #     #"time_window": time_window
    # }
    print("-----api call----------------")
    print("PAYLOAD:")
    print(payload)
    #print(type(time_window))
#     payload = {
#     "status": search_criteria.get("status"),
#     "priority": search_criteria.get("priority"),
#     "fullname": search_criteria.get("fullname"),
#     "department": search_criteria.get("department"),
#     "assignee_id": search_criteria.get("assignee_id"),
#     "time_window": time_window
# }

    response = requests.post(url, json=payload, timeout=10)
    print(response.status_code)
    print(response.text)
    response.raise_for_status()
    print("-----api call----------------")

    
    return response.json()