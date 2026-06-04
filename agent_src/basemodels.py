from typing import List,Set
from enum import Enum
from pydantic import BaseModel, Field, RootModel
from typing import Literal, Optional, Union

class OrchestratorClassification(BaseModel):
    """
    Represents the structured output for a LLM to extract intent from  user conversation.
    Classifies user input into one of the following categories:

    - Statistics, Analytical, Search, Operation
    It is used in the orchestrator node to determine the user's intent and route to the appropriate node in the graph.
    """
    intent: Literal["Statistics", "Analytical", "Search", "Operation","None"] = Field(
        ...,
        description="The classified intent of the user input."
    )


class SearchNodeOutput(BaseModel):
    """
    Represents the structured output for a LLM to extract search parameters from user conversation.
    It is used in the search node to determine what information the user wants to search for in the ticketing system database.
    """
    create_time: Optional[str] = Field(
        None,
        description="If the user wants to search by create_time field in the database."
    )

    status: Optional[Literal["Done", "In Progress", "Review", "Open"]] = Field(
        None,
        description="If the user wants to search by status field in the database."
    )

    priority: Optional[Literal["High", "Medium", "Critical", "Low"]] = Field(
        None,
        description="If the user wants to search by priority field in the database."
    )

    due_time: Optional[str] = Field(
        None,
        description="If the user wants to search by due_time field in the database."
    )

    fullname: Optional[str] = Field(
        None,
        description="If the user wants to search by fullname field in the database."
    )

    department: Optional[Literal["فنی", "محصول", "مالی", "پشتیبانی", "مدیریت", "استقرار"]] = Field(
        None,
        description="If the user wants to search by department field in the database."
    )

class StatisticsNodeOutput(BaseModel):
    """
    Represents the structured output for a LLM to extract statistics parameters from user conversation.
    It is used in the statistics node to determine what information the user wants to analyze in the ticketing system database.
    """
    time_window: Optional[str] = Field(
        None,
        description="If the user wants to search by time_window field in the database."
    )

    status: Optional[Literal["Done", "In Progress", "Review", "Open", "all"]] = Field(
        None,
        description="If the user wants to search by status field in the database."
    )

    priority: Optional[Literal["High", "Medium", "Critical", "Low"]] = Field(
        None,
        description="If the user wants to search by priority field in the database."
    )

    fullname: Optional[str] = Field(
        None,
        description="If the user wants to search by fullname field in the database."
    )

    department: Optional[Literal["فنی", "محصول", "مالی", "پشتیبانی", "مدیریت", "استقرار"]] = Field(
        None,
        description="If the user wants to search by department field in the database."
    )


    