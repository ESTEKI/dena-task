from langchain_core.tools import tool
from datetime import datetime


# @tool
# def time_tool(user_input_timeframe: str) -> Dict[str, str]:
#     """
#     Returns current day/date/time: {'day': 'Wednesday', 'date': '2025-11-12', 'time': '14:03:21'}
#     """
#     now = datetime.now()
    
#     return {
#         "day": now.strftime("%A"),
#         "date": now.strftime("%Y-%m-%d"),
#         "time": now.strftime("%H:%M:%S"),
#     }

#     #     Output: {
#     # "start_date": "2026-01-01",   
#     #     "end_date": "2026-01-07"
#     # }