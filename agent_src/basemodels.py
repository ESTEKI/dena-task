from typing import List,Set
from enum import Enum
from pydantic import BaseModel, Field, RootModel
from typing import Literal, Optional, Union

class OrchestratorClassification(BaseModel):
    """
    Represents the structured output for a LLM to extract intent from  user conversation.
    Classifies user input into one of the following categories:

    - Statistics, Analytical, Search, Operation
    
    """
    intent: Literal["Statistics", "Analytical", "Search", "Operation"] = Field(
        ...,
        description="The classified intent of the user input."
    )
