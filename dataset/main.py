from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd

app = FastAPI()

# Load CSV once
df = pd.read_csv("merged_data_seperate_time.csv", index_col=0)




class TimeWindow(BaseModel):
    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None


class SearchRequest(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    fullname: Optional[str] = None
    department: Optional[str] = None
    assignee_id: Optional[int] = None
    time_window: Optional[TimeWindow] = None


@app.post("/search")
def search_tasks(request: SearchRequest):

    result = df.copy()

    # Column filters
    if request.status:
        result = result[result["status"] == request.status]

    if request.priority:
        result = result[result["priority"] == request.priority]

    if request.fullname:
        result = result[result["fullname"] == request.fullname]

    if request.department:
        result = result[result["department"] == request.department]

    if request.assignee_id:
        result = result[result["assignee_id"] == request.assignee_id]

    # Time filters
    if request.time_window:
        if request.time_window.year:
            result = result[result["year"] == request.time_window.year]

        if request.time_window.month:
            result = result[result["month"] == request.time_window.month]

        if request.time_window.day:
            result = result[result["day"] == request.time_window.day]

    return {
        "count": len(result),
        "data": result.to_dict(orient="records")
    }