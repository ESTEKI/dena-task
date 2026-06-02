from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated, Literal, Union, Optional, Dict, Any
from . import llm_definition as llms

# APPSTATE
class AppState(TypedDict):
            user_msg: str
            messages: Annotated[list, add_messages]

def orchestrator(state: AppState):
        pass

def chat(state: AppState):
        """
        general chat node
        """
        response = llms.llm_openai.invoke(state.get("messages"))
        
        return {"messages": [response]}


        
        


