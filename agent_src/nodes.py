from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated, Literal, Union, Optional, Dict, Any
from . import llm_definition as llms
import agent_src.basemodels as basemodels
import agent_src.prompts as Prompts
import agent_src.logger as Logger

# APPSTATE
class AppState(TypedDict):
            user_msg: str
            messages: Annotated[list, add_messages]
            user_intent: Optional[Literal["Statistics", "Analytical", "Search", "Operation","None"]]
            search_criteria: Optional[Dict[str, Any]]

logger = Logger.LoggerManager("nodes")

def orchestrator(state: AppState):
        """
        Classifier node that determines the action based on last 3 messages in the conversation history. 
        It uses a structured output llm call to determine the user intent and route to the correct node in the graph.
        """
        llm = llms.llm_openai
        str_llm = llm.with_structured_output(basemodels.OrchestratorClassification)
        messages = state.get("messages", [])

        # Only keep the last 4 messages for context to avoid hitting token limits, and format them for the prompt
        try:
            last_msgs_history = []
            for message in reversed(messages):
                if isinstance(message, HumanMessage):
                    last_msgs_history.append(f"User: {message.content}")
                elif isinstance(message, AIMessage):
                    last_msgs_history.append(f"Assistant: {message.content}")
                if len(last_msgs_history) == 2:
                    break
            last_msgs_history.reverse()

            formatted_prompt = Prompts.orchestrator_prompt.replace("{conversation_history}", str(last_msgs_history))

            logger.log(f"Formatted prompt for orchestrator:\n{formatted_prompt}", level="debug")
            messages = [HumanMessage(content=formatted_prompt)]
        except Exception as e:
            logger.log(f"Exception while building messages: {e}", level="critical")
            formatted_prompt = Prompts.orchestrator_prompt.replace("{conversation_history}", "failed to load history!")
            messages = [HumanMessage(content=formatted_prompt)]

        try:
            response = str_llm.invoke(messages)
        except Exception as e:
            logger.log(f"Error in API call to LLM service. msg: {e}", level="critical")
            return {"user_intent": "None"}
        
        return {"user_intent": response.intent}

def search_node(state: AppState):
        llm = llms.llm_openai
        str_llm = llm.with_structured_output(basemodels.SearchNodeOutput)
        messages = state.get("messages", []) 
        try:            
            last_msgs_history = []
            for message in reversed(messages):
                if isinstance(message, HumanMessage):
                    last_msgs_history.append(f"User: {message.content}")
                elif isinstance(message, AIMessage):
                    last_msgs_history.append(f"Assistant: {message.content}")
                if len(last_msgs_history) == 2:
                    break
            last_msgs_history.reverse()

            formatted_prompt = Prompts.search_node_prompt.replace("{conversation_history}", str(last_msgs_history))

            logger.log(f"Formatted prompt for search node:\n{formatted_prompt}", level="debug")
            messages = [HumanMessage(content=formatted_prompt)]
        except Exception as e:
            logger.log(f"Exception while building messages for search node: {e}", level="critical")
            formatted_prompt = Prompts.search_node_prompt.replace("{conversation_history}", "failed to load history!")
            messages = [HumanMessage(content=formatted_prompt)]
        try:
            response = str_llm.invoke(messages)
        except Exception as e:
            logger.log(f"Error in API call to LLM service for search node. msg: {e}", level="critical")
            return {"search_criteria": {}}
        return {"search_criteria": response.dict(exclude_none=True)}

def chat(state: AppState):
        """
        general chat node that takes in user input and returns a response from the llm.
        """
        messages = state.get("messages", [])
        response = llms.llm_openai.invoke(messages)
        # Normalize response.content to a simple string
        if isinstance(response.content, list):
            extracted = []
            for item in response.content:
                if isinstance(item, dict) and "text" in item:
                    extracted.append(item["text"])
            content_text = " ".join(extracted)
        else:
            content_text = str(response.content).strip()
        return {"messages": [content_text]}

def should_continue(state: AppState):
    """
    Routes the flow based on user_intent produced by the orchestrator node.
    """

    user_intent = state.get("user_intent")

    if not user_intent or user_intent == "None":
        return "end"

    intent_map = {
        "Statistics": "Statistics",
        "Analytical": "Analytical",
        "Search": "Search",
        "Operation": "Operation",
    }
    # returning the corresponding node based on user intent, if intent is not recognized return "end"
    return intent_map.get(user_intent, "end")
        
        


